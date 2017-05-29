#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import os,sys
import hashlib
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from conf import settings

'''
用来实现客户端的操作，时间比较紧，所以没有按照面向对象写这块
'''

if __name__ == '__main__':

    sk=socket.socket()
    sk.connect((settings.BIND_IP,settings.BIND_PORT))
    sk.send(bytes("conn_signal","utf8"))
    server_ack=sk.recv(settings.SIGNAL_BUFFER)
    if str(server_ack,"utf8")=="ack":
        print("server %s connected" %settings.BIND_IP)
    username=input("User (%s):" %settings.BIND_IP).strip()
    password=input("Password:").strip()
    passd=hashlib.md5()
    passd.update(bytes(password,"utf8"))
    sk.send(bytes("%s|%s" %(username,passd.hexdigest()),"utf8"))
    server_ack=sk.recv(settings.SIGNAL_BUFFER)
    if str(server_ack,"utf8")=="Login successful!":   # 用户验证成功后继续执行，否则socket直接关闭
        print("Login successful!")
    else:
        print(str(server_ack,"utf8"))
        sk.close()

    while True:
        user_cmd=input("ftp>").strip()
        if user_cmd.startswith('cd'):
            sk.send(bytes(user_cmd,"utf8"))
            cmd_res=str(sk.recv(settings.SIGNAL_BUFFER),"utf8")
            print(cmd_res)
        elif user_cmd.startswith('get'):     # 处理get命令，即从服务端下载文件到本地
            file=user_cmd.split()[1].strip()
            if not os.path.isfile(file): # 文件不存在
                data_mark=0
                recv_data_size=0
            else:
                data_mark=os.stat(file).st_size
                recv_data_size=data_mark
            sk.send(bytes("%s %s"%(user_cmd,data_mark),"utf8"))
            file_size=str(sk.recv(settings.SIGNAL_BUFFER),"utf8")
            if file_size=="File not exist!":
                print("File not exist!")
            else:
                sk.send(bytes("ack","utf8"))
                #print("file_size:",file_size)
                with open(file,'ab') as f:
                    while recv_data_size<int(file_size):
                        file_data=sk.recv(settings.FILE_BUFFER)
                        recv_data_size += len(file_data)
                        f.write(file_data)
                        progress=int((recv_data_size/int(file_size))*100)
                        sys.stdout.write("File getting: %s%%\r" %progress)
                        sys.stdout.flush()
                print("\n")

        elif user_cmd.startswith('put'):     # 处理用户put命令，即上传本地文件到服务器端
            file=user_cmd.split()[1].strip()
            file_size=os.stat(file).st_size
            sk.send(bytes("%s %s"%(user_cmd,file_size),"utf8"))
            data_mark=str(sk.recv(settings.SIGNAL_BUFFER),"utf8")
            if data_mark=="not enough quota!":
                print("not enough quota!")
            else:
                with open(file,'rb') as f:
                    f.seek(int(data_mark))
                    sent_data=int(data_mark)
                    while True:
                        file_data=f.read(settings.FILE_BUFFER)
                        if not file_data:
                            break
                        else:
                            sk.send(file_data)
                            sent_data += len(file_data)
                            progress=int((sent_data/file_size)*100)
                            sys.stdout.write("File sending: %s%%\r" %progress)
                            sys.stdout.flush()
                print("\n")
        elif user_cmd=='quit':           # 用户退出
            sk.send(bytes(user_cmd,"utf8"))
            break

        else:
            sk.send(bytes(user_cmd,"utf8"))
            res=str(sk.recv(settings.SIGNAL_BUFFER),"utf8")
            print(res)
    sk.close()