#Author :ywq
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from moudle import manage,tools
print(BASE_DIR)



def help_msg():
    '''
    print help msgs
    :return:
    '''
    print("\033[31;1mAvailable commands:\033[0m")
    for key in manage.action_register:
        print("\t",key)
    print('Usage:CMD  [-f]  path_to_file')
def excute_from_command_line(argvs):
    if len(argvs) < 3:
        help_msg()
        exit()
    if argvs[1] not in manage.action_register:
        tools.print_err("Command [%s] does not exist!" % argvs[1], quit=True)
    manage.action_register[argvs[1]](argvs[1:])

if __name__=='__main__':
    excute_from_command_line(sys.argv)
