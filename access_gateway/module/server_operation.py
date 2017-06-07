# -*- coding:utf-8 -*-
import configparser
import paramiko
import sys,os
from conf import sys_config

class gateway_server(object):
    def __init__(self,logger):
        """
        gateway_server初始化
        :param expression: 传入logger对象
        :return:
        """
        self.login_user=None
        self.logger=logger
        self.conf_file=sys_config.SERVER_CONF
        self.conf=configparser.ConfigParser()
        self.conf.read(self.conf_file)
        if len(self.conf.sections())==0: #服务器文件为空
            self.conf['DEFAULT']={
                'group':'default'
            }
            with open(self.conf_file, 'w') as configfile:
                self.conf.write(configfile)
                self.logger.info('Initialing server config file...')

    def login_auth(self,user,password):   # 管理员登录验证
        """
        登录验证
        :param expression: 传入用户名和密码
        :return: 返回conn对象
        """
        if user in sys_config.USER_ACCOUNT:
            if password==sys_config.USER_ACCOUNT[user]:
                #print("[%s] login successful" %user)
                self.login_user=user
                self.logger.info("[%s] login successful" %user)
                print("[%s] login successful" %user)
        if self.login_user==None:
            print("login failed")
            self.logger.info("login failed")

    def exec_shell(self,cmd_list):
        """
        执行shell命令
        :param expression: 传入cmd_list，格式为 hostname exec_shell user_command，如 192.168.1.1 exec_shell ls -a
        :return: 返回命令执行结果
        """
        hostname=cmd_list[0]
        ip=self.conf[hostname]['ip']
        port=int(self.conf[hostname]['port'])
        username=self.conf[hostname]['username']
        password=self.conf[hostname]['password']
        shell_cmd=' '.join(cmd_list[2:])
        transport=paramiko.Transport((ip,port))
        transport.connect(username=username,password=password)
        ssh=paramiko.SSHClient()
        ssh._transport=transport
        stdin,stdout,stderr=ssh.exec_command(shell_cmd)
        if len(stderr.read())==0: # 没有错误输出
            cmd_res=stdout.read().decode()
        else:
            cmd_res=stderr.read().decode()
        print("command execution result:")
        print(cmd_res)
        transport.close()
        return cmd_res


    def upload(self,cmd_list):
        """
        执行upload文件上传命令
        :param expression: 传入cmd_list，格式为 hostname upload local_file remote_file，如 upload F:\\IMG_1714.MOV /root/IMG_1714.MOV
        :return:
        """
        hostname=cmd_list[0]
        ip=self.conf[hostname]['ip']
        port=int(self.conf[hostname]['port'])
        username=self.conf[hostname]['username']
        password=self.conf[hostname]['password']
        local_file=cmd_list[2]
        remote_file=cmd_list[3]
        transport=paramiko.Transport((ip,port))
        transport.connect(username=username,password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(local_file,remote_file)
        print("upload file %s successfully" %local_file)
        self.logger.info("upload file %s successfully" %local_file)
        transport.close()

    def download(self,cmd_list):
        """
        执行download文件下载命令
        :param expression: 传入cmd_list，格式为 hostname download remote_file local_path，如 download /root/install.log install.log
        :return:
        """
        hostname=cmd_list[0]
        ip=self.conf[hostname]['ip']
        port=int(self.conf[hostname]['port'])
        username=self.conf[hostname]['username']
        password=self.conf[hostname]['password']
         #本地文件添加后缀名.hostname，主要是为了区分，不同主机下载下来的同一个文件
        local_file="%s.%s" %(os.path.join(sys_config.LOCAL_PATH,cmd_list[3]),hostname)
        remote_file=cmd_list[2]
        transport=paramiko.Transport((ip,port))
        transport.connect(username=username,password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        # 将remote_file 下载到本地 local_path
        print(remote_file)
        print(local_file)
        sftp.get(remote_file,local_file)
        print("download file %s successfully" %local_file)
        self.logger.info("download file %s successfully" %local_file)
        transport.close()

    def print_section(self,secs):  # 查询一个section下面的内容
        """
        打印section下面的option和value值
        :param expression: 传入secs，为section的名称
        :return:
        """
        print("---[%s]---"%secs)
        for option in self.conf[secs]:
            print("%s: %s" %(option,self.conf[secs][option]))

    def query(self,cmd_list): # 查某一台主机信息，或者某个组的信息
        para_list=cmd_list
        if '-r' in para_list: # 查询主机
            query_list=['server',]
            query_list.extend(para_list[2:])
        else:  # 查询组
            query_list=['group',]
            query_list.extend(para_list[2:])

        if len(query_list)==1:
            #print('Error: null parameter')
            self.logger.error('Error: null parameter')
        else:
            for item in query_list[1:]:
                if item in self.conf.sections():
                    self.print_section(item)
                else:
                    #print('WARNING: Not found %s' %item)
                    self.logger.warn('WARNING: Not found %s' %item)

    def add(self,cmd_list):
        """
        add添加主机或者组的信息
        :param expression: 传入cmd_list为用户输入的命令生成的列表
        :return:
        """
        # add -r hostname xxx ip xxx port xxx username xxx password xxx group xxx
        # add -g groupname hostname1 hostname2 ...
        if '-r' in cmd_list: #增加主机信息
            if 'hostname' not in cmd_list:
                print('Error: you need to specify hostname')
            else:
                new_server=cmd_list[cmd_list.index('hostname')+1]
                if self.conf.has_section(new_server):
                    print('Error: %s is exist' %new_server)
                else: # 新增记录
                    self.conf.add_section(new_server)
                    for i in range(len(cmd_list[4:])):
                        if i%2==0:
                            self.conf.set(new_server,cmd_list[i+4],cmd_list[i+5])
                    if 'group' in cmd_list:
                        self.conf.set(cmd_list[cmd_list.index('group')+1],new_server,new_server)
                    print("add server info successfully")
                    self.conf.write(open(self.conf_file,'w'))
        else:  #增加组信息
            if len(cmd_list)<3:
                print('Error: you need to specify groupname')
            else:
                if self.conf.has_section(cmd_list[2]):
                    print('Error: %s is exist' %cmd_list[2])
                else:
                    if len(cmd_list)>3:   # 配置文件中为 hostname = hostname
                        for i in range(len(cmd_list[3:])):
                            self.conf.set(cmd_list[2],cmd_list[i+3],cmd_list[i+3])
                            #self.conf.write(open(self.conf_file,'w'))
                    else:
                        self.conf.add_section(cmd_list[2])
                    print("add group info successfully")
                    self.conf.write(open(self.conf_file,'w'))


    def delete(self,cmd_list):
        """
        delete删除主机或者组的信息
        :param expression: 传入cmd_list为用户输入的命令生成的列表
        :return:
        """
        #delete -r hostname
        #delete -g group

        if '-r' in cmd_list: #删除主机
            del_item='server'
        else:
            del_item='group'
        tmp_server_list=[]
        for i in range(len(cmd_list[2:])):
            if self.conf.has_section(cmd_list[i+2]):
                if del_item=='server' and self.conf.has_section(self.conf[cmd_list[i+2]]['group']):
                    self.conf.remove_option(self.conf[cmd_list[i+2]]['group'],cmd_list[i+2])
                elif del_item=='group': # 处理组
                    tmp_server_list.extend(list(self.conf.options(cmd_list[i+2])))
                    for server_item in tmp_server_list:
                        if server_item!='group':
                            self.conf[server_item]['group']='default'
                else:
                    pass
                self.conf.remove_section(cmd_list[i+2])
                print("delete finished")
                self.conf.write(open(self.conf_file,'w'))

            else:
                print('Error: %s is not exist' %cmd_list[i+2])

    def update(self,cmd_list):
        """
        update修改主机或者组的信息
        :param expression: 传入cmd_list为用户输入的命令生成的列表
        :return:
        """
        #update -r hostname xxx ip xxx port xxx username xxx password xxx group xxx
        #update -g old_group new_group
        if len(cmd_list)<3:
            print('Error: missing necessary parameter' )
        else:
            if '-r' in cmd_list: #更新server记录
                if self.conf.has_section(cmd_list[3]):
                    updated_server=cmd_list[3]
                    old_group=self.conf[updated_server]['group']
                    if 'group' in cmd_list:
                        new_group=cmd_list[cmd_list.index('group')+1]
                    else:
                        new_group=old_group
                    for i in range(len(cmd_list[4:])):
                        if i%2==0:
                            self.conf.set(updated_server,cmd_list[i+4],cmd_list[i+5])
                    if new_group!=old_group:
                        if not self.conf.has_section(new_group):
                            self.conf.add_section(new_group)
                        if old_group!='default':
                            self.conf.remove_option(old_group,updated_server)
                        self.conf.set(new_group,updated_server,updated_server)
                    print("update server info successfully")
                    self.conf.write(open(self.conf_file,'w'))
            else: #更新group记录
                old_group=cmd_list[2]
                new_group=cmd_list[3]
                if old_group==new_group:
                    print('1')
                    pass
                else:
                    server_list=list(self.conf.options(old_group))
                    for server in server_list:
                        if server!='group':
                            self.conf.set(server,'group',new_group)
                    self.conf.remove_section(old_group)
                    self.conf.add_section(new_group)
                    for server in server_list:
                        if server!='group':
                            self.conf.set(new_group,server,server)
                    print("update group info successfully")
                    self.conf.write(open(self.conf_file,'w'))

    def quit(self,cmd_list):
        print('Exit system...')
        sys.exit()




