#Author :ywq
RDS_type='mysql'
database_name='fortress'
ip='192.168.0.71'
port='22'
user='ywq'
password='qwe'


engine_param='%s+pymysql://%s:%s@%s/%s?charset=utf8'  %(RDS_type,user,password,ip,database_name)

