#_*_coding:utf-8_*_
# This is the Twisted Fast Poetry Server, version 1.0

import optparse, os

from twisted.internet.protocol import ServerFactory, Protocol


def parse_args():
    '''
    用来解析命令以及参数
    :return: options以及poetry_file的值
    '''
    usage = """usage: %prog [options] poetry-file

This is the Fast Poetry Server, Twisted edition.
Run it like this:

  python fastpoetry.py <path-to-poetry-file>

If you are in the base directory of the twisted-intro package,
you could run it like this:

  python twisted-server-1/fastpoetry.py poetry/ecstasy.txt

to serve up John Donne's Ecstasy, which I know you want to do.
"""

    parser = optparse.OptionParser(usage)   # 生成一个对象

    help = "The port to listen on. Default to a random available port."  #--port的帮助信息
    parser.add_option('--port', type='int', help=help)  # 增加参数 --port 用来指定监听的端口

    help = "The interface to listen on. Default is localhost."  # --face 的 帮助信息
    parser.add_option('--iface', help=help, default='localhost')  # 增加参数 --iface 用来指定监听的ip

    options, args = parser.parse_args()  # 获取options 参数以及剩余的参数[此例中为文件名]
    print("--arg:",options,args)

    if len(args) != 1:  # 如果参数不等于1，则表示有多个poetry files
        parser.error('Provide exactly one poetry file.')

    poetry_file = args[0]   # 获取 poetry file的路径和文件名

    if not os.path.exists(args[0]):  # 检查 poetry file是不是存在的，如果不存在，则打印下面的错误信息
        parser.error('No such file: %s' % poetry_file)

    return options, poetry_file  # 返回 options以及poetry_file的值


class PoetryProtocol(Protocol):
    '''
    PoetryProtocol类，继承了Protocol类，作用是重写了connectionMade方法
    '''
    def connectionMade(self):
        '''
        该方法在服务器端建立连接后调用，
        使用transport.write方法发送poem的内容到client端
        之后使用transport.loseConnection断开连接
        '''
        self.transport.write(self.factory.poem)
        self.transport.loseConnection()


class PoetryFactory(ServerFactory):
    '''
    PoetryFactory类，继承了ServerFactory类，在类中把自定义的PoetryProtocol类
    传给protocol.
    属性poem接收传入的poem内容
    '''
    protocol = PoetryProtocol

    def __init__(self, poem):
        self.poem = poem


def main():
    options, poetry_file = parse_args()  # 调用parse_args()函数获取options以及poetry_file[文件路径以及文件名]的值

    poem = open(poetry_file).read() # 读取 poetry_file的内容，并保存在poem中

    factory = PoetryFactory(poem)  # 生成一个PoetryFactory的实例factory

    from twisted.internet import reactor

    port = reactor.listenTCP(options.port or 9000, factory,
                             interface=options.iface)
    # 指定reactor监听的配置--iface传入的ip和--port传入端口，如果不指定端口的话，默认监听9000端口

    print 'Serving %s on %s.' % (poetry_file, port.getHost())

    reactor.run()  # 调用reactor中的run方法


if __name__ == '__main__':
    main()