# Copyright (C) 2003-2007  Robey Pointer <robeypointer@gmail.com>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.

import socket
import sys
from paramiko.py3compat import u
import datetime
from moudle import table_init
from moudle.db_conn import session

# windows does not have termios...
try:
    import termios
    import tty
    has_termios = True
except ImportError:
    has_termios = False


def interactive_shell(chan,user_obj,choose_host,choose_group):
    if has_termios:
        posix_shell(chan,user_obj,choose_host,choose_group)
    else:
        windows_shell(chan)


def posix_shell(chan,user_obj,choose_host,choose_group):
    import select

    oldtty = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)
        cmd = ''

        tab_key = False
        while True:
            r, w, e = select.select([chan, sys.stdin], [], [])
            if chan in r:
                try:
                    x = u(chan.recv(1024))
                    if tab_key:
                        if x not in ('\t','\r\n'):
                            #print('tab:',x)
                            cmd += x
                        tab_key = False
                    if len(x) == 0:
                        sys.stdout.write('\r\n*** EOF\r\n')
                        break
                    sys.stdout.write(x)
                    sys.stdout.flush()
                except socket.timeout:
                    pass

            if sys.stdin in r:
                x = sys.stdin.read(1)
                if '\r' != x:
                    cmd +=x      #输入字符不包含回车，则命令还未输入完成，包含回车且输入字符长度大于0，则记录日志
                if '\r' == x and len(cmd)>0:
                    log_item = table_init.Log_audit(user_id=user_obj.id,
                                               user_name=user_obj.username,
                                          host_ip=choose_host.ip,
                                          login_user=choose_group.name,
                                          action_type='cmd',
                                          cmd=cmd ,
                                          date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                                          )
                    session.add(log_item)
                    session.commit()
                    cmd = ''

                if '\t' == x:
                    tab_key = True
                # if len(x) == 0:
                #     break
                chan.send(x)

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)


# thanks to Mike Looijmans for this code
def windows_shell(chan):
    import threading

    sys.stdout.write("Line-buffered terminal emulation. Press F6 or ^Z to send EOF.\r\n\r\n")

    def writeall(sock):
        while True:
            data = sock.recv(256)
            if not data:
                sys.stdout.write('\r\n*** EOF ***\r\n\r\n')
                sys.stdout.flush()
                break
            sys.stdout.write(data)
            sys.stdout.flush()

    writer = threading.Thread(target=writeall, args=(chan,))
    writer.start()

    try:
        while True:
            d = sys.stdin.read(1)
            if not d:
                break
            chan.send(d)
    except EOFError:
        # user hit ^Z or F6
        pass
