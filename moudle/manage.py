#Author :ywq
from moudle import table_init
from moudle.db_conn import session
from moudle.tools import yaml_parser,print_err
from  sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from conf import config


def create_hosts(argvs):
    '''
    create hosts
    :param argvs:
    :return:
    '''
    if '-f' in argvs:
        hosts_file  = argvs[argvs.index("-f") +1 ]   # -f参数后一位为文件路径
    else:
        print_err("Usage:\ncreate_hosts -f <the host_file path>",quit=True)
    source = yaml_parser(hosts_file)  #文件交由yaml_parser处理，处理完的结果返回
    if source:
        print(source)
        for key,val in source.items():
            print(key,val)
            obj = table_init.Host(hostname=key,ip=val.get('ip'), port=val.get('port') or 22)
            session.add(obj)
        session.commit()



def create_group(argvs):
    if '-f' in argvs:
        groups_file  = argvs[argvs.index("-f") +1 ]
    else:
        print_err("Usage:\ncreate_groups -f <the group_file path>",quit=True)
    source=yaml_parser(groups_file)
    print(source)
    if source:
        for key,val in source.items():
            group_obj=table_init.Group(name=key,login_passwd=val.get('password'))
            session.add(group_obj)
        session.commit()



def create_user(argvs):
    if '-f' in argvs:
        user_file  = argvs[argvs.index("-f") +1 ]
    else:
        print_err("Usage:\ncreate_users -f <the user_file path>",quit=True)

    source = yaml_parser(user_file)
    if source:
        for key,val in source.items():
            print(key,val)
            obj = table_init.User(username=key,password=val.get('password'))
            # session.add(obj)
            # session.commit()
            if val.get('group'):

                groups = session.query(table_init.Group).filter(table_init.Group.name.in_(val.get('group'))).all()
                print(groups)
                if not groups:
                    print_err('Group %s not exist' %val.get('users'),quit=True)
                else:obj.groups=groups
            session.add(obj)
            session.commit()

def create_group_bind_host(argvs):
    if '-f' in argvs:
        bind_file  = argvs[argvs.index("-f") +1 ]
    else:
        print_err("Usage:\ncreate_group_bind_host -f <the group_file path>",quit=True)
    source=yaml_parser(bind_file)
    if source:
        for bind_ins,val in source.items():
            g_obj= session.query(table_init.Group).filter(table_init.Group.name==val.get('groupname')).first()
            assert g_obj
            host_obj=session.query(table_init.Host).filter(table_init.Host.hostname.in_(val.get('hostname'))).all()
            print(host_obj)
            g_obj.bind_hosts=host_obj
            session.commit()
            create_user_bind_host(g_obj)



def create_user_bind_host(g_obj):
    g_obj_bind_hosts_list=session.query(table_init.Group_Bind_Host).filter(table_init.Group_Bind_Host.group_id==g_obj.id).all() #该group的所有bind实例
    for i in g_obj_bind_hosts_list:
        i.users=g_obj.users
    session.commit()


action_register={
    'create_hosts':create_hosts,
    'create_user':create_user,
    'create_group':create_group,
    'create_group_bind_host':create_group_bind_host,
}


# user_groups=session.query(table_init.User.groups).filter(table_init.User.username=='alice')
# print(user_groups)
#
# group_user=session.query(table_init.Group.users).filter(table_init.Group.name=='dba')
# print(group_user)

# g1=session.query(table_init.Group).filter(table_init.Group.name.in_(['app','dba'])).all()
# print(g1)