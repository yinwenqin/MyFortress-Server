#Author :ywq
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import traceback
from moudle import interactive
# from paramiko.py3compat import input
# from moudle import table_init


import paramiko
# try:
#     import interactive
# except ImportError:
#     from . import interactive



def ssh_conn(user_obj,choose_host,choose_group):
    # now, connect and use paramiko Client to negotiate SSH2 across the connection
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())
        print('*** Connecting...')
        #client.connect(hostname, port, username, password)
        client.connect(choose_host.ip,
                       choose_host.port,
                       choose_group.name,
                       choose_group.login_passwd,
                       timeout=30)

        # cmd_caches = []
        chan = client.invoke_shell()
        # print(repr(client.get_transport()))
        # print('*** Here we go!\n')
        # cmd_caches.append(models.AuditLog(user_id=user_obj.id,
        #                                   bind_host_id=bind_host_obj.id,
        #                                   action_type='login',
        #                                   date=datetime.datetime.now()
        #                                   ))
        # log_recording(user_obj,bind_host_obj,cmd_caches)
        interactive.interactive_shell(chan,user_obj,choose_host,choose_group)
        chan.close()
        client.close()

    except Exception as e:
        print('*** Caught exception: %s: %s' % (e.__class__, e))
        traceback.print_exc()
        try:
            client.close()
        except:
            pass
        sys.exit(1)