#_*_coding:utf-8_*_
# This is the Twisted Get Poetry Now! client, version 3.0.

# NOTE: This should not be used as the basis for production code.

import optparse

from twisted.internet.protocol import Protocol, ClientFactory


def parse_args():
    '''
    用来解析命令以及参数
    :return: options以及poetry_file的值
    '''
    usage = """usage: %prog [options] [hostname]:port ...

This is the Get Poetry Now! client, Twisted version 3.0
Run it like this:

  python get-poetry-1.py port1 port2 port3 ...
"""

    parser = optparse.OptionParser(usage)  # 生成一个OptionParser的对象parser

    _, addresses = parser.parse_args() # 获取options以及addresses的值，addresses中存放所有的参数[hostname和port信息]
                                       # 由于没有指定option，所以使用'_'来获取，表示这部分值不需要
    if not addresses:  # 如果没有带任何hostname或者port信息，则打印帮助信息
        print parser.format_help()
        parser.exit()

    def parse_address(addr):
        '''
        解析address的函数
        :param addr: 为传入的hostname以及port组成的列表信息
        :return: 返回hostname和对应的port值
        '''
        if ':' not in addr:  # 判断':'是否在addr中，如果不在的话，addr值作为端口号，并默认host ip 为127.0.0.1
            host = '127.0.0.1'
            port = addr
        else:  # ':'在addr中，那么split之后，前半部分为host ip，后半部分为port
            host, port = addr.split(':', 1)

        if not port.isdigit():  # 如果端口号不是数字，那么提示如下错误
            parser.error('Ports must be integers.')

        return host, int(port)

    return map(parse_address, addresses)  # 使用map函数，将addresses列表中的每一对hostname:port值分别
                                          # 放入parse_address中执行，返回的结果是一个列表[('ip',port),('ip',port),..]


class PoetryProtocol(Protocol):
    '''
    定义PoetryProtocol类，继承Protocol类
    '''
    poem = '' # 定义类变量poem,用来存放获取到poem的值

    def dataReceived(self, data):
        # 在收到服务端发送的数据时调用
        self.poem += data   # 把数据存放在poem变量中

    def connectionLost(self, reason):
        # 在连接断开时调用
        self.poemReceived(self.poem)  # 连接断开时调用poemReceived()函数

    def poemReceived(self, poem):
        self.factory.poem_finished(poem)  # 调用factory中定义的poem_finished函数


class PoetryClientFactory(ClientFactory):
    '''
    定义PoetryClientFactory类，继承ClientFactory类
    '''
    protocol = PoetryProtocol  # 将自定义的PoetryProtocol类传给protocol

    def __init__(self, callback):
        self.callback = callback

    def poem_finished(self, poem):
        # poem_finished函数，执行后会调用 callback函数
        self.callback(poem)


def get_poetry(host, port, callback):
    '''
    从指定的host,port来获取poem,获取成功后执行callback回调函数
    '''
    from twisted.internet import reactor
    factory = PoetryClientFactory(callback)  # 生成PoetryClientFactory实例，并传入callback回调函数的值
    reactor.connectTCP(host, port, factory)  # 使用reactor监听host,port，并传入factory实例


def poetry_main():
    addresses = parse_args()  # 调用parse_args()获取address地址列表[(ip,port)为列表的元素]

    from twisted.internet import reactor

    poems = []  # 定义一个poem列表

    def got_poem(poem):  # 定义got_poem函数
        poems.append(poem)  # 如果获取到一个poem,就把它添加到poem列表当中
        if len(poems) == len(addresses):  # 如果所有的poem全部获取完[这里从每个address获取一个poem，所以使用poem列表的长度
                                        #   和addresses列表的长度进行对比 ]，则调用reactor中stop方法来停止获取
            reactor.stop()

    for address in addresses:  # 循环addresses列表，对每一个ip,port执行get_poetry()方法来获取poem
        host, port = address   # 获取具体的host,port的值
        get_poetry(host, port, got_poem) # 调用get_poetry函数获取poem,传入host,port以及get_poem作为回调函数

    reactor.run()   #

    for poem in poems: # 对poems列表中的每一个poem,打印输出
        print poem


if __name__ == '__main__':
    poetry_main()