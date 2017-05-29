import os
BASEDIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOMEDIR="%s/home" %BASEDIR
BIND_IP='192.168.59.129'
BIND_PORT=1555
REQUEST_QUEUE_SIZE = 5
Initial_Signal=1000
Ack_Signal=1001
FILE_BUFFER=4096    # 用于传输文件
SIGNAL_BUFFER=2048   # 用于传输信号


USER_ACCOUNT = {
    'alex': {
        'password': 'alex123',
        'quotation': 1000000,   # 需要扩大
    },
    'gll': {
        'password': 'gll123',
        'quotation': 2000000,
    },
    'john': {
        'password': 'john123',
        'quotation': 2000000,
    },
}