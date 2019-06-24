from sqlalchemy import Table, Column, Enum,Integer,String,DATE, ForeignKey,UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

user_m2m_group_bind_host = Table('user_m2m_group_bind_host', Base.metadata,
                        Column('id',Integer,autoincrement=True,primary_key=True),
                        Column('user_id', Integer, ForeignKey('user.id')),
                        Column('group_bind_host_id', Integer, ForeignKey('group_bind_host.id')),
                        )

user_m2m_group = Table('user_m2m_group', Base.metadata,
                               Column('user_id', Integer, ForeignKey('user.id')),
                               Column('group_id', Integer, ForeignKey('group.id')),
                               )


class Host(Base):
    __tablename__ = 'host'
    id = Column(Integer,primary_key=True)
    hostname = Column(String(64),unique=True)
    ip = Column(String(64),unique=True)
    port = Column(Integer,default=22)

    def __repr__(self):
        return self.hostname

class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    login_passwd=Column(String(64))
    bind_hosts = relationship("Host",secondary='group_bind_host',backref="groups")
    users=relationship('User',secondary='user_m2m_group',backref='groups')

    def __repr__(self):
        return self.name


class Group_Bind_Host(Base):
    __tablename__ = "group_bind_host"
    __table_args__ = (UniqueConstraint('group_id','host_id', name='_host_remoteuser_uc'),)
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('group.id'))
    host_id = Column(Integer,ForeignKey('host.id'))

    users=relationship('User',secondary='user_m2m_group_bind_host',backref='group_bind_hosts')

    #host = relationship("Host")
    #host_group = relationship("Group",backref="bind_hosts")
    #group = relationship("Group")


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer,autoincrement=True,primary_key=True)
    username = Column(String(32))
    password = Column(String(128))
    #groups = relationship("Group",secondary="user_m2m_group")
    bind_hosts = relationship("Group_Bind_Host", secondary='user_m2m_group_bind_host')

    def __repr__(self):
        return self.username


# class AuditLog(Base):
#     pass

# if __name__ == "__main__":
#     engine=create_engine('mysql+pymysql://ywq:qwe@192.168.0.71/jpserver?charset=utf8',
#                      encoding='utf-8')
#     Base.metadata.create_all(engine)  # 创建表结构

    # Session_class = sessionmaker(bind=engine) #创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
    # session = Session_class() #生成session实例
    #
    # h1=Host(hostname='nginx',ip='192.168.0.68',port=22)
    # h2=Host(hostname='mysql',ip='192.168.0.71',port=22)
    # h3=Host(hostname='python',ip='192.168.0.158',port=22)
    #
    # g1=Group(name='view',login_passwd='view123456')
    # g2=Group(name='app',login_passwd='app123456')
    # g3=Group(name='dba',login_passwd='dba123456')
    # g4=Group(name='admin',login_passwd='admin123456')
    #
    # u1=User(username='alice',password='a123456')
    # u2=User(username='bob',password='b123456')
    # u3=User(username='jack',password='j123456')
    # u4=User(username='slade',password='s123456')
    #
    # # u1.groups=[g1]
    # # u2.groups=[g2]
    # # u3.groups=[g2,g3]
    # # u4.groups=[g1,g4]
    # g1.users=[u1,u4]
    # g2.users=[u2,u3]
    # g3.users=[u3]
    # g4.users=[u4]
    #
    # g1.bind_hosts=[h1,h2,h3]
    # g2.bind_hosts=[h1]
    # g3.bind_hosts=[h2]
    # g4.bind_hosts=[h1,h2,h3]
    #
    #
    # session.add_all([h1,h2,h3,g1,g2,g3,g4,u1,u2,u3,u4])
    # session.commit()

    # g1_bind_host_objlist=session.query(Group_Bind_Host).filter(Group_Bind_Host.group_id==g1.id).all()
    # g2_bind_host_objlist=session.query(Group_Bind_Host).filter(Group_Bind_Host.group_id==g2.id).all()
    # g3_bind_host_objlist=session.query(Group_Bind_Host).filter(Group_Bind_Host.group_id==g3.id).all()
    # g4_bind_host_objlist=session.query(Group_Bind_Host).filter(Group_Bind_Host.group_id==g4.id).all()
    #
    # print('---------------------->1',g1_bind_host_objlist,'\n',
    #       '---------------------->2',g2_bind_host_objlist,'\n',
    #       '---------------------->3',g3_bind_host_objlist,'\n',
    #       '---------------------->4',g4_bind_host_objlist,'\n',
    #       )

    # for g1_obj in g1_bind_host_objlist:
    #     g1_obj.users=[u1,u4]
    #     print('---------------------->1',g1_obj.users)
    # for g2_obj in g1_bind_host_objlist:
    #     g2_obj.users=[u2,u3]
    #     print('---------------------->2',g2_obj.users)
    # for g3_obj in g1_bind_host_objlist:
    #     g3_obj.users=[u3]
    #     print('---------------------->3',g3_obj.users)
    # for g4_obj in g1_bind_host_objlist:
    #     g4_obj.users=[u4]
    #     print('---------------------->4',g4_obj.users)
    #session.commit()

