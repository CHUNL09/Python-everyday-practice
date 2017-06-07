# -*- coding:utf-8 -*-
import sys,os
from conf import sys_config
import gevent
from module import log_generate
import configparser

class command_handle(object):
    def __init__(self):
        self.help_msg='''
        gate '<target>' <function> [arguments]
        e.g: gate '*' sys.doc test.fib
    '''
        '''
        self.server=configparser.ConfigParser()
        self.group=configparser.ConfigParser()
        self.server.read(sys_config.SERVER_CONF)
        self.server.read(sys_config.GROUP_CONF)
        '''

    def print_help_msg(self):  # 打印帮助信息
        print(self.help_msg)

    def generate_config(self,config_file):
        config=configparser.ConfigParser()
        config.read(config_file)
        return config

    def format(self,str1):
        tmp=str1
        if '\'' in tmp:
            tmp=tmp.strip('\'')
        tmp_list=list(tmp.split(','))
        return tmp_list

    def parse_cmd(self,user_cmd):
        """
        解析用户输入的原始命令
        :param expression: 传入user_cmd为用户输入的命令
        :return: 返回命令字典
        """
        cmd_dict={'server':[],
                  'group':[],
                  'function':'',
                  'argument':[],
                  'server_config':'',
                  'group_config':'',
                  'config_file':[sys_config.GROUP_CONF,sys_config.SERVER_CONF]
        }
        cmd_dict['server_config']=self.generate_config(sys_config.SERVER_CONF)
        cmd_dict['group_config']=self.generate_config(sys_config.GROUP_CONF)
        cmd_list=list(user_cmd.split())
        if cmd_list[0]=='gate' and len(cmd_list)>=3:
            tmp_list=self.format(cmd_list[1])
            cmd_dict['server'].extend(tmp_list)
            cmd_dict['group'].extend(tmp_list)
            cmd_dict['function']=cmd_list[2]
            if len(cmd_list)>=4:
                tmp_list=self.format(cmd_list[3])
                cmd_dict['argument'].extend(tmp_list)
            return cmd_dict
        else:
            print("Wrong input command!")
            self.print_help_msg()
            return False

    def process_cmd(self,cmd_dict):  #处理命令
        if '.' in cmd_dict['function']:
            module_name,function=cmd_dict['function'].split('.')
            module_file='%s/module/%s'%(sys_config.BASE_DIR,module_name)
            if os.path.isfile('%s.py'%module_file):
                module_imported='module.%s' %module_name
                module_im=__import__('module', globals(), locals(), [module_name,], 0)
                new_module=getattr(module_im,module_name)
                if hasattr(new_module,function):
                    func=getattr(new_module,function)
                    if module_name in ['server','group']:  # 定义一个 sys_ops_list
                        gevent.joinall([gevent.spawn(func,cmd_dict),])
                    else:
                        cmd_dict=self.transform_group(cmd_dict)
                        tasks=[]
                        for server in cmd_dict['server']:
                            para_dict=cmd_dict
                            para_dict['server']=server
                            task=gevent.spawn(func,para_dict)
                            tasks.append(task)
                        gevent.joinall(tasks)
                else:
                    print('No function %s found...' %function)
            else:
                print('No module file %s found...' %module_file)

    def transform_group(self,cmd_dict):
        command_dict=cmd_dict
        server_list=command_dict['server']
        group_list=command_dict['group']
        new_group=group_list
        new_server=[]
        for item in server_list:
            if self.server.has_section(item):
                new_server.append(item)
            elif self.group.has_sections(item):
                new_group.append(item)
            else:
                print('Error: cannot find server %s' %item)
        for group_item in new_group:
            if self.group.has_sections(group_item):
                for item in self.group[group_item]:
                    new_server.append(item)
            else:
                print('Error: cannot find group %s' %item)
        command_dict['server']=new_server
        command_dict['group']=new_group
        return command_dict

class Main(object):
    def __init__(self):
        self.login_user=None
        logger_obj=log_generate.logger()
        logger_ins=logger_obj.log()
        self.logger=logger_ins

    def main(self):
        login_user=input('username: ').strip()
        login_pass=input('password: ').strip()
        self.login_auth(login_user,login_pass)
        if self.login_user==None:
            sys.exit()
        else: #登录成功后继续执行
            while True:
                user_command=input('%s>' %self.login_user)
                if user_command!='quit':
                    cmd_handle=command_handle()
                    command_list=cmd_handle.parse_cmd(user_command)
                    cmd_handle.process_cmd(command_list)
                    self.logger.info('Process command %s' %user_command)
                else:
                    print('Exit system...')
                    sys.exit()

    def login_auth(self,user,password):   # 管理员登录验证
        """
        登录验证
        :param expression: 传入用户名和密码
        :return: 返回conn对象
        """
        if user in sys_config.USER_ACCOUNT:
            if password==sys_config.USER_ACCOUNT[user]:
                self.login_user=user
                self.logger.info("[%s] login successful" %user)
                print("[%s] login successful" %user)
        if self.login_user==None:
            print("login failed")
            self.logger.info("login failed")

