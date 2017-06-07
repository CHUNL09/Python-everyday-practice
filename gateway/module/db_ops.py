from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column,Integer,String,ForeignKey,UniqueConstraint,DateTime,Table
from sqlalchemy.orm import relationship,sessionmaker

'''
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
'''
from conf import settings

Base=declarative_base()  # 生成一个sqlORM基类
engine=create_engine(settings.DB['connector'], max_overflow=settings.DB['max_session'],echo=False)
SessionCls=sessionmaker(bind=engine)
session=SessionCls()


HostUserToGroup = Table('hostuser_to_group',Base.metadata,
    Column('host_user_id',ForeignKey('host_user.id'),primary_key=True),
    Column('group_id',ForeignKey('server_group.id'),primary_key=True),
)

GatewayUserToHostUser = Table('gatewayuser_to_hostuser',Base.metadata,
    Column('gatewayuser_id',ForeignKey('gateway_user.id'),primary_key=True),
    Column('hostuser_id',ForeignKey('host_user.id'),primary_key=True),
)

GatewayUserToGroup = Table('gatewayuser_to_group',Base.metadata,
    Column('gatewayuser_id',ForeignKey('gateway_user.id'),primary_key=True),
    Column('group_id',ForeignKey('server_group.id'),primary_key=True),
)


class Host(Base):
    '''
    主机表所在的类Host
    '''
    __tablename__='host'
    id=Column(Integer,primary_key=True,autoincrement=True)
    hostname=Column(String(64),unique=True,nullable=False)
    ip_addr=Column(String(128),unique=True,nullable=False)
    port=Column(Integer,default=22)

    def __repr__(self):
        return "<Host(id=%s,hostname=%s,ip:port=%s:%s)>" %(self.id,self.hostname,self.ip_addr,self.port)


class Group(Base):
    '''
    主机组所在的类ServerSet
    '''
    __tablename__='server_group'
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(64),unique=True,nullable=False)

    def __repr__(self):
        return "<Group(id=%s,name=%s)>" %(self.id,self.name)

class HostUser(Base):
    '''
    主机用户所在的类HostUser
    '''
    __tablename__='host_user'
    id=Column(Integer,primary_key=True,autoincrement=True)
    user=Column(String(32),nullable=False)
    password=Column(String(128))
    host_id=Column(Integer,ForeignKey('host.id'))
    host=relationship('Host')
    private_key=Column(String(128),nullable=True)  #登录使用key

    groups=relationship('Group',secondary=HostUserToGroup,backref='host_users')
    __table_args__= (UniqueConstraint('host_id','user',name='hostid_user_uc'),)

    def __repr__(self):
        return "<HostUser(id=%s,user=%s,host_id=%s)>" %(self.id,self.user,self.host_id)

class GatewayUser(Base):
    __tablename__='gateway_user'
    id=Column(Integer,primary_key=True,autoincrement=True)
    user=Column(String(32),unique=True,nullable=False)
    password=Column(String(128),nullable=False)
    groups=relationship('Group',secondary=GatewayUserToGroup,backref='gateway_users')
    host_users=relationship('HostUser',secondary=GatewayUserToHostUser,backref='gateway_users')
    def __repr__(self):
        return "<User(id=%s,user=%s)>" %(self.id,self.user)

class AuditLog(Base):
    __tablename__='audit_log'
    id=Column(Integer,primary_key=True,autoincrement=True)
    gateway_user_id=Column(Integer,ForeignKey('gateway_user.id'))
    host_user_id=Column(Integer,default=-1)
    date=Column(DateTime)
    log_msg=Column(String(512),nullable=False)

    def __repr__(self):
        return "<User(id=%s,user=%s)>" %(self.id,self.user)

def db_init():
    Base.metadata.create_all(engine) #创建所有表结构

#Base.metadata.create_all(engine)
   #

# print('hello--before---')
# gateway_user = session.query(GatewayUser).filter(GatewayUser.user=='admin').first()
# print('hello--------')
# if not gateway_user:
#     gateway_user_profile = GatewayUser(user='admin', password='admin')
#     session.add(gateway_user_profile)
#     session.commit()
