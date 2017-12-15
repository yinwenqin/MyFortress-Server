#Author :ywq
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from moudle.table_init import Base
from conf.config import engine_param

engine=create_engine(engine_param)

Session_class = sessionmaker(bind=engine) #创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
session = Session_class() #生成session实例

