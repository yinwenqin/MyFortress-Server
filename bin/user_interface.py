#Author :ywq
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from moudle import table_init
from moudle.db_conn import session
from moudle.ssh_conn import ssh_conn
import getpass

current_user=getpass.getuser() #get current login username
def welcome_msg():
    WELCOME_MSG = '''\033[32;1m
    ------------- Welcome to login MyFortress server,[%s] -------------
    Here are all of the groups you belong to
    choose one group(by number),all the hosts in this group will be listed,
    or direct input the specified ip address of the host you want to login.
    \033[0m'''% current_user
    print(WELCOME_MSG)

def start_session():
    # try:
    welcome_msg()
    user_obj=session.query(table_init.User).filter(table_init.User.username==current_user).first()
    assert user_obj

    while True:
        user_groups=user_obj.groups
        print(user_obj,user_groups)
        for index,g_name in enumerate(user_groups):
            print('\033[32;1m %i [%s] \033[0m' %(index+1,g_name))
        choice1=input('\033[32m;1mChoose one group number,or direct input the ip address of your target host:\033[0m \n')
        if len(choice1)==0:continue
        if choice1.isdigit():
            choose_group=user_groups[int(choice1)-1]
            g_obj=session.query(table_init.Group).filter(table_init.Group.name==choose_group.name).first()
            print(g_obj)
            g_to_h_obj=g_obj.bind_hosts
            for index,host_obj in enumerate(g_to_h_obj):
                print(index+1,host_obj.ip)

            choice2=input('\033[32m;1mInput the num or ip of your target host number ,or direct input the ip of target host:\033[0m \n')
            if choice2.isdigit():
                choose_host=g_to_h_obj[int(choice2)-1]
            else:
                choose_host=session.query(table_init.Host).filter(table_init.Host.ip==choice2).first()

            ssh_conn(user_obj,choose_host,choose_group)

        else:

            choose_host=session.query(table_init.Host).filter(table_init.Host.ip==choice1).first()
            host_groups=choose_host.groups
            available_group=[g for g in user_groups if g in host_groups]  #在用户所属group列表内，同时也在选定主机绑定的group列表内的
                                                                          # group对象，即为该用户登陆该主机时可用的所有groupname
            if not available_group:print('\033[42m;1mError,your groups no access to this host\033[0m')
            for index,g in enumerate(available_group):
                print(index+1,g.name)
            choose_group_num=input('\033[32m;1mThe group_name is the login Identification,choose the num :\033[0m \n')
            choose_group=available_group[int(choose_group_num-1)]
            ssh_conn(user_obj,choose_host,choose_group)

    # except  Exception as e:
    #     print('Error:',e)


    #     # h1=session.query(table_init.Host).filter(table_init.Host.ip=='192.168.0.68').first()
    #     # g_obj1=h1.groups
    #     # u1=session.query(table_init.User).filter(table_init.User.username=='alice').first()
    #     # g_obj2=u1.groups
    #     # group=[i for i in g_obj1 if i in g_obj2]
    #     # print(group)
    #     # print(g_obj.bind_hosts,type(g_obj.bind_hosts))
    #     # for i in g_obj.bind_hosts:
    #     #     print(i,type(i),i.ip)


start_session()


