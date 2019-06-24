import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from sqlalchemy import Table, Column, Enum,Integer,String, ForeignKey,UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from conf import config


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
    groups=relationship('Group',secondary='group_bind_host')

    def __repr__(self):
        return self.hostname

class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    login_passwd=Column(String(64))
    bind_hosts = relationship("Host",secondary='group_bind_host')
    users=relationship('User',secondary='user_m2m_group')

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
    groups = relationship("Group",secondary="user_m2m_group")
    bind_hosts = relationship("Group_Bind_Host", secondary='user_m2m_group_bind_host')

    def __repr__(self):
        return self.username


class Log_audit(Base):
    __tablename__= 'log_audit'
    id = Column(Integer,autoincrement=True,primary_key=True)
    user_id = Column(Integer)
    user_name = Column(String(32))
    host_ip = Column(String(32))
    login_user = Column(String(32))
    action_type = Column(String(16))
    cmd=Column(String(128))
    date = Column(String(16))

if __name__ == "__main__":
    engine=create_engine(config.engine_param)
    Base.metadata.create_all(engine)  # 创建表结构