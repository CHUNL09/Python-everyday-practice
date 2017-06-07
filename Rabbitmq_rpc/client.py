#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pika,sys,uuid,time

class RpcClient(object):
    '''
    定义RpcClient类
    '''
    def __init__(self):
        '''
        初始化函数会定义一个return_queue，所有的返回消息都会返回到这一个queue中。
        :return:
        '''
        self.connection=pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
        self.channel=self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
            res=str(self.response,encoding='utf8')
            cmd_result,remote_queue=res.split('|')
            print('Cmd result from %s [%s]' %(remote_queue,cmd_result))

    def call(self,cmd,routing_key):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.exchange_declare(exchange='cmd_ex',type='topic')
        self.channel.basic_publish(exchange='cmd_ex',
                                   routing_key=routing_key,
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(cmd))
        print('sending cmd [%s] to [%s]...' %(cmd,routing_key))
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:  # 键盘输入 ctrl+c后，会stop掉，然后程序继续
            self.channel.stop_consuming()
        self.connection.close()

def main():
    while True:
        print('Please input routing_key and cmd, format: routing_key cmd')
        user_cmd=input('>>>:').strip()
        if user_cmd=='quit':
            sys.exit('Exiting the system...')
        elif len(user_cmd.split())<2:
            sys.exit('Usage: routing_key cmd')
        else:
            routing_key=user_cmd.split()[0]
            cmd=' '.join(user_cmd.split()[1:])
            print(routing_key,cmd)
            ins=RpcClient()
            ins.call(cmd,routing_key)

            #ins.connection.close()

if __name__=='__main__':
    main()
