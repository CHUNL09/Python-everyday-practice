# -*- coding:utf-8 -*-
import sys
from conf import sys_config
from module import server_operation
from multiprocessing import Process,Pool
from module import log_generate

class command_handle(object):
    def __init__(self):
        self.help_msg='''
        add -r hostname xxx ip xxx port xxx username xxx password xxx group xxx
        add -g groupname hostname1 hostname2 ...
        query -r hostname
        query -g groupname
        update -r hostname ip xxx port xxx username xxx password xxx group xxx
        update -g old_group new_group
        delete -r hostname
        delete -g group
        download file local_path [-r hostname ..] [-g groupname ..]
        upload local_file des_path [-r hostname ..] [-g groupname ..]
        exec_shell other_command [-r hostname ..] [-g groupname ..]
    '''

    def print_help_msg(self):  # 打印帮助信息
        print(self.help_msg)

    def parse_cmd(self,user_cmd):
        """
        解析用户输入的原始命令
        :param expression: 传入user_cmd为用户输入的命令
        :return: 返回命令列表
        """
        cmd_list=['add','query','update','delete','download','upload','exec_shell','quit']
        parameter_list=['-r','-g']
        raw_cmd=user_cmd
        cmd_count=len(cmd_list)
        for cmd in cmd_list:
            if not raw_cmd.startswith(cmd):
                cmd_count-=1
            else:
                para_count=len(parameter_list)
                for para in parameter_list:
                    if para not in raw_cmd:
                        para_count -=1
                if para_count==0 and raw_cmd!='quit':
                    print('Error: lack effective parameter')
                    self.print_help_msg()
                    sys.exit()
                else:
                    command_list=list(raw_cmd.split())    # 生成一个参数list，然后对参数list操作
            if cmd_count==0:
                print('Error: unrecognized command')
                self.print_help_msg()
                sys.exit()
        return command_list

    def run_cmd(self,server,cmd_list):
        """
        反射功能实现
        :param expression: 传入gateway_server对象和命令类表
        :return: 返回函数的地址
        """
        cmd_list=cmd_list
        if hasattr(server,cmd_list[0]):
            func=getattr(server,cmd_list[0])
            return func
        # 如果是 batch_list=['download','upload','exec_shell'],会执行batch_ops
        # 其他函数直接执行

    def batch_ops(self,operation,cmd_list,server_conf):  #接收机器的列表
        """
        批量操作实现，使用线程池，对'download','upload','exec_shell'执行批量操作
        :param expression: 传入operation为函数内存地址，cmd_list为命令类表，server_conf为configparser实例
        :return:
        """
        operation=operation
        cmd_list=cmd_list
        pool=Pool(sys_config.PROCESS_POOL_SIZE)
        para_list=[]
        server_list=[]
        if '-r' in cmd_list: # 操作主机
            server_list.extend(cmd_list[(cmd_list.index('-r')+1):])
            para_list.extend(cmd_list[:cmd_list.index('-r')])
        else: # 操作组
            group_list=cmd_list[(cmd_list.index('-g')+1):]
            para_list.extend(cmd_list[:cmd_list.index('-g')])
            for group in group_list:
                server_list.extend(list(server_conf.options(group)))
        print('Batch command running...')
        for server in server_list:
            if server !='group':
                print('-------------%s------------'%server)
                para_list.insert(0,server)
                operation(para_list)
                pool.apply_async(func=operation,args=(para_list,))
                #p=Process(target=operation, args=(para_list,)).start()
        pool.close()
        pool.join()


    def run(self):
        """
        生成各个实例，并执行，是运行时的主函数
        :param expression:
        :return:
        """
        logger_obj=log_generate.logger()
        logger_ins=logger_obj.log()
        g_server=server_operation.gateway_server(logger_ins)  # 生成一个gateway_server()实例
        login_user=input('username: ').strip()
        login_pass=input('password: ').strip()
        g_server.login_auth(login_user,login_pass)
        if g_server.login_user==None:
            sys.exit()
        else: #登录成功后继续执行
            while True:
                user_command=input('%s>' %g_server.login_user)
                command_list=self.parse_cmd(user_command)
                func=self.run_cmd(g_server,command_list)
                batch_list=['download','upload','exec_shell','test']
                if command_list[0] in batch_list:
                    self.batch_ops(func,command_list,g_server.conf)
                    logger_ins.info('Execute batch command [%s]'%command_list)
                else:
                    func(command_list)
                    logger_ins.info('Execute operation [%s]'%command_list)
