# -*- coding:utf-8 -*-
import sys,os
from conf import settings
from module.db_ops import session
from module import db_ops
from module.logger import log_record
from module.shell_terminal import shell_terminal

def data_init():
    h1=db_ops.Host(hostname='hostserver1',ip_addr='192.168.59.131')
    h2=db_ops.Host(hostname='hostserver2',ip_addr='192.168.59.130')
    h3=db_ops.Host(hostname='hostserver3',ip_addr='192.168.111.130')
    g1=db_ops.Group(name='group1')
    g2=db_ops.Group(name='group2')
    gw1=db_ops.GatewayUser(user='admin',password='admin123')
    gw2=db_ops.GatewayUser(user='alex',password='alex123')
    session.add_all([h1,h2,h3,g1,g2,gw1,gw2])
    session.commit()
    hu1=db_ops.HostUser(user='root',password='aircool',host_id=h1.id)
    hu2=db_ops.HostUser(user='liuchun',password='aircool',host_id=h1.id)
    hu3=db_ops.HostUser(user='liuchun',password='aircool',host_id=h2.id)
    session.add_all([hu1,hu2,hu3])
    host_users=session.query(db_ops.HostUser).all()
    g1.host_users=host_users
    g2.host_users=session.query(db_ops.HostUser).filter(db_ops.HostUser.user=='liuchun').all()
    gw1.groups=session.query(db_ops.Group).all()
    gw1.host_users=session.query(db_ops.HostUser).all()
    gw2.group=g2
    gw2.host_users=[hu1,hu2,hu3]
    session.commit()

def main():
    user_input=input("input 'Y' to initial the database: ").strip()
    if user_input in ['Y','y']:
        data_init()
    else:
        pass
    while True:
        username=input('username: ').strip()
        password=input('password: ').strip()
        login_user=session.query(db_ops.GatewayUser).filter(db_ops.GatewayUser.user==username,
                                                            db_ops.GatewayUser.password==password).first()

        if login_user:
            host_list=[]

            for index,host in enumerate(login_user.host_users):
                print("%s. server [%s] account[%s]" %(index,host.host.hostname,host.user))
                host_list.append(host)
            user_choice=int(input("Connect: ").strip())
            shell_terminal(login_user,host_list[user_choice])
        else:
            print("Login failed. wrong username or password...")
