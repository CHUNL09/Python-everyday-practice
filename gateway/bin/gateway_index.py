#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
version: 1.0
author: liu chun
contact: cedrela_liu@163.com
date:
"""
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from module import main
from module import db_ops

if __name__=='__main__':
    db_ops.db_init()
    main.main()