#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pika,sys,local_function


class RpcServer(object):
    '''
    定义RpcServer类
    '''
    def __init__(self,queue_name,binding_key_list):
        '''
        初始化函数
        :param queue_name: 这台server自己的queue的名字
        :param binding_key_list: binding_key的列表，执行时请输入 group1.#  all.#，
                                 group1.# 表示这个server属于group1，那么在client端发命令到group1时候，server会收到
                                 all.# 表示server属于all,那么在client端发命令到all时候，所有server会收到
        '''
        self.connection=pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel=self.connection.channel()
        self.binding_key_list=binding_key_list
        self.queue_name=queue_name
        self.channel.exchange_declare(exchange='cmd_ex',type='topic')
        self.channel.queue_declare(queue=self.queue_name)
        self.channel.basic_qos(prefetch_count=1)
        for binding_key in self.binding_key_list:
            self.channel.queue_bind(exchange='cmd_ex',
                       queue=self.queue_name,
                       routing_key=binding_key)
    def consume(self):
        self.channel.basic_consume(self.on_request,queue=self.queue_name)
        self.channel.start_consuming()

    def on_request(self,channel,method,properties,body):
        cmd=str(body,encoding='utf8')
        print('received cmd: %s' %cmd)
        cmd_func,cmd_para=cmd.split('|')
        if hasattr(local_function,cmd_func):  # 去local_function中查找对应的函数
            func=getattr(local_function,cmd_func)
        else:  # 如果找不到cmd_func,默认的命令是echo命令
            func=getattr(local_function,'echo')
        res=func(cmd_para)
        print('executing result: %s' %res)
        response="%s|%s" %(res,self.queue_name)

        channel.basic_publish(exchange='',
                              routing_key=properties.reply_to,
                              properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                              body=response
                              )
        channel.basic_ack(delivery_tag=method.delivery_tag)

def main():
    queue_name=input('input your queue_name: ')
    binding_key=input('input your binding keys: ')
    # 输入参考： queue的名称取不重复的，binding_key可以自己绑定，建议输入  group1.#  all.#，既属于某个小group1，
    # 同时也属于全部组all
    QUEUE_NAME=queue_name
    BINDING_KEY_LIST=[]
    BINDING_KEY_LIST.extend(list(binding_key.split()))
    print('[info] Your queue is [%s] ' %queue_name)
    print('[info] Your binding_keys are %s'%BINDING_KEY_LIST)
    server_ins=RpcServer(QUEUE_NAME,BINDING_KEY_LIST)
    server_ins.consume()

if __name__=='__main__':
    main()