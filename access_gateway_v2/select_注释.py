#_*_coding:utf-8_*_
import select
import socket
import sys
import queue

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # 创建TCP/IP的socket
server.setblocking(False)  # 设置socket 不阻塞
server_address=('localhost',10000)
print(sys.stderr,'starting up on %s port %s' % server_address)
server.bind(server_address)   # 绑定 server_address
server.listen(5)   # 监听地址和端口，允许最多5个连接
inputs=[server]  # 初始化inputs列表，用于放置文件描述符FD
outputs=[]   # 写列表，用于放置可写的文件描述符,在本例中，为outputs列表中的FD有数据要发送
message_queues={}  # 文件描述符的消息队列，在本例中，理解为不同socket的消息队列

while inputs:  # 循环处理inputs列表
    print('\nwaiting for the next event')
    readable,writeable,exceptional=select.select(inputs,outputs,inputs)  # select来获取readable,writeable,exceptional的文件描述符的集合

    for s in readable:  # 循环readable 的FD的集合
        if s is server:  # 如果文件描述符为server
            # 表示 server可读，即可以接受一个连接
            connection,client_address=s.accept()   # 接受一个新的连接
            print('new connection from ', client_address)
            inputs.append(connection)      # 把新的连接放到 inputs列表中，待下一次循环处理
            message_queues[connection]=queue.Queue()  # 给新的连接创建一个消息队列
        else:   # 文件描述符不是server，即为正常的连接 connection
            data=s.recv(1024)   # 接收客户端发送的数据
            if data:   # 如果数据不为空
                print(sys.stderr,'received %s from %s' %(data,s.getpeername()))
                message_queues[s].put(data)   # 在connection对象对应的queue中放入接收的数据
                if s not in outputs:    # 如果connection不在outputs列表中，则把connection加入到outputs列表中
                    outputs.append(s)
            else:  # 如果接收的数据为空
                print('closing ',client_address ,'after read no data')   # 关闭连接
                if s in outputs:
                    outputs.remove(s)     # 将 connection从outputs列表中删除
                inputs.remove(s)    # 将 connection从inputs列表中删除
                s.close()
                del message_queues[s]   # 将 connection 的消息队列删除
    for s in writeable:  # 循环writeable 的FD的集合，在本例中，这个集合中的对象可以发送数据
        try:
            next_msg=message_queues[s].get_nowait()   # 从消息队列中获取消息
        except queue.Empty:  # 如果消息队列已空
            print('output queue for ',s.getpeername(),'is empty')
            outputs.remove(s)                     # 如果队列为空，那么在outputs列表中删除这个connection
        else:
            print('sending %s to %s' %(next_msg,s.getpeername()))
            s.send(next_msg)                 # 发送消息给客户端

    for s in exceptional:   # 循环异常的FD集合，在本例中，即出错的 connection
        print('handling exceptional condition for ',s.getpeername())
        inputs.remove(s)      # 将 connection从inputs列表中删除
        if s in outputs:
            outputs.remove(s)   # 将 connection从outputs列表中删除
        s.close()
        del message_queues[s]   # 将 connection 的消息队列删除