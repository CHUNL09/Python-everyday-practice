# -*- coding:utf-8 -*-

"""
定义了FTP_Server类和Command类
FTP_Server类用于处理server端各种操作
Command类用于处理接收到客户端的不同的命令，如cd, ls等
"""
import socket
import subprocess
import hashlib
from conf import settings
import os
import sys
import time


class FTP_Server(object):
    def __init__(self,ip,port,queue_size):
        self.ip=ip
        self.port=port
        self.queue_size=queue_size
        self.socket=socket.socket()
        self.socket.bind((self.ip,self.port))
        self.socket.listen(self.queue_size)
        self.login_flag=False
        self.work_path=''
        self.user=''
        self.cur_path=''

    def login_auth(self,conn):
        """
        登录验证
        :param expression: 传入conn对象
        :return: 返回conn对象
        """
        inputname,inputpass=str(conn.recv(settings.SIGNAL_BUFFER),"utf8").split('|')
        if inputname in settings.USER_ACCOUNT.keys():
            passd=hashlib.md5()
            passd.update(bytes(settings.USER_ACCOUNT[inputname]['password'],"utf8"))
            if passd.hexdigest()==inputpass: # 密码匹配
                conn.send(bytes("Login successful!","utf8"))
                self.login_flag=True
                self.work_dir(inputname)   # 设置用户家目录
                self.user=inputname
                return conn
            else: # 密码错误
                conn.send(bytes("Wrong password!","utf8"))
                conn.close()
        else:
            conn.send(bytes("User not exist!","utf8"))
            conn.close()

    def work_dir(self,login_user):
        """
        获取用户的家目录，也是初始的工作目录
        :param expression: 传入login_user
        :return:
        """
        work_path="%s/%s" %(settings.HOMEDIR,login_user)
        if not os.path.isdir(work_path):  #目录不存在，则创建用户家目录
            os.mkdir(work_path)
        self.work_path=work_path
        self.cur_path=work_path

    def conn_up(self):
        conn,addr=self.socket.accept()
        client_ini_signal=conn.recv(settings.SIGNAL_BUFFER)  # 客户端会初始发送 conn_signal
        if str(client_ini_signal,"utf8")=="conn_signal":
            conn.send(bytes("ack","utf8"))
        else:
            conn.send(bytes("err","utf8"))
        return conn

    def handle_conn(self,conn):
        """
        处理与客户端之间的交互
        :param expression: 传入conn对象
        :return:
        """
        while True:
            while True:
                client_cmd = conn.recv(settings.SIGNAL_BUFFER)  # command parameter, 比如 cd /home
                if not client_cmd:
                    break
                command=str(client_cmd,"utf8").split()[0]
                cmd_obj=Command(conn,self.work_path,self.cur_path,self.user)
                if hasattr(cmd_obj,command):
                    func = getattr(cmd_obj,command)
                    func(str(client_cmd,"utf8"))
                else:
                    res=cmd_obj.shell_run(str(client_cmd,"utf8"))
                    if res.split('|')[1]=="0": #命令执行成功
                        if len(res.split('|')[0])==0:
                            conn.send(bytes("Command return empty!","utf8"))
                        else:
                            conn.send(bytes(res.split('|')[0],"utf8"))
                    else:
                        conn.send(bytes("Command execution error!","utf8"))
                self.cur_path=cmd_obj.cur_dir
            conn.close()


class Command(object):
    def __init__(self,conn,work_dir,cur_dir,cur_user):
        self.conn=conn
        self.work_dir=work_dir  # 用户家目录
        self.cur_dir=cur_dir  # 当前目录
        self.cur_user=cur_user # 当前用户


    def cd(self,shell_cmd):
        """
        cd 命令的实现
        :param expression: 传入用户的完整shell命令
        :return:
        """
        shell_cmd="%s;pwd" %shell_cmd
        os.chdir(self.cur_dir)
        cmd_result,cmd_result_code=self.shell_run(shell_cmd).split('|')
        cmd_result=cmd_result.strip()
        if cmd_result_code=="0": # 表示执行成功
            if cmd_result.startswith(self.work_dir):
                self.cur_dir=cmd_result
                os.chdir(cmd_result)  # 切换到正确目录
                cur_path=cmd_result
                self.conn.send(bytes(cmd_result,"utf8"))
            else:
                self.conn.send(bytes("Permission denied!","utf8"))
        else:  # 执行失败
            self.conn.send(bytes("Command execution error!","utf8"))

    def get_real_qutation(self):
        """
        获取用户实际的磁盘配额，调用linux系统的du命令
        :param expression:  返回实际使用的额度
        :return:
        """
        shell_cmd="du -sb %s" %self.work_dir
        result,res_code=self.shell_run(shell_cmd).split('|')
        if len(result)==0:
            return 0
        else:
            real_qutation=int(result.split()[0].strip())
        return real_qutation

    def get(self,shell_cmd):  # get filename size  客户端需要传送size,为客户端部分接收的文件大小,客户端输出进度条
        """
        get 命令的实现,从服务器下载文件到本地
        :param expression: 传入用户的完整shell命令
        :return:
        """
        file=shell_cmd.split()[1]
        if not os.path.isfile(file): # 文件不存在
            print("should not go here")
            self.conn.send(bytes("File not exist!","utf8"))
        else:
            file_size=str(os.stat(file).st_size)
            print(file_size)
            self.conn.send(bytes(file_size,"utf8"))  # 给客户端发送文件大小
            client_ack=self.conn.recv(settings.SIGNAL_BUFFER)
            print(str(client_ack,"utf8"))
            mark_point=int(shell_cmd.split()[2])
            with open(file,'rb') as f:
                f.seek(mark_point)
                while True:
                    file_data=f.read(settings.FILE_BUFFER)
                    if not file_data:
                        break
                    else:
                        self.conn.send(file_data)


    def put(self,shell_cmd):  #    put filename size
        """
        put 命令的实现,从本地上传文件到服务器
        :param expression: 传入用户的完整shell命令
        :return:
        """
        os.chdir(self.cur_dir)
        file=shell_cmd.split()[1]
        file_size=int(shell_cmd.split()[2])
        available_quota=settings.USER_ACCOUNT[self.cur_user]['quotation']-self.get_real_qutation()
        if not os.path.isfile(file): # 文件不存在
            data_mark=0
        else:
            data_mark=os.stat(file).st_size

        recv_data_size=data_mark
        if file_size<=available_quota:
            self.conn.send(bytes(str(data_mark),"utf8"))
            with open(file,'ab') as f:
                while recv_data_size<file_size:
                    file_data=self.conn.recv(settings.FILE_BUFFER)
                    recv_data_size += len(file_data)
                    f.write(file_data)
        else:
            self.conn.send(bytes("not enough quota!","utf8"))

    def quit(self):
        self.conn.send(bytes("close"))
        self.conn.close()

    def shell_run(self,shell_cmd):
        """
        其他shell命令的实现
        :param expression: 传入用户的完整shell命令
        :return: 返回 shell结果|shell命令执行状态
        """
        os.chdir(self.cur_dir)
        cmd_call=subprocess.Popen(shell_cmd,shell=True,stdout=subprocess.PIPE)
        cmd_result=cmd_call.stdout.read()
        cmd_result_code=cmd_call.wait()
        # cmd_result_code==0: # 表示执行成功
        return "%s|%s" %(str(cmd_result,"utf8"),cmd_result_code)

