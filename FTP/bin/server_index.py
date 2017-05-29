#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
version: 1.0
author: liu chun
contact: cedrela_liu@163.com
date:  2016-3-12
"""
import os,sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from conf import settings
from core import function

if __name__ == '__main__':
    server=function.FTP_Server(settings.BIND_IP,settings.BIND_PORT,settings.REQUEST_QUEUE_SIZE)
    conn=server.conn_up()
    server.login_auth(conn)
    server.handle_conn(conn)
