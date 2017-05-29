#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
用来初始化account.txt的数据，配合bill_generate.py来验证出账
"""
import json,time


account_info={
              "4392600137250001":["123","user1",15000,0,0,0,0,[]],
              "4392600137250002":["123","user2",15000,0,0,0,0,[]],
              "4392600137250003":["123","user3",15000,0,0,0,0,[]],
              "4392600137250004":["123","user4",13799.4,0,0,0,0,[["0004",time.mktime(time.strptime("2016-01-20","%Y-%m-%d")),"交易1",300],
                                                                    ["0004",time.mktime(time.strptime("2016-01-24","%Y-%m-%d")),"交易2",300.1],
                                                                    ["0004",time.mktime(time.strptime("2016-01-28","%Y-%m-%d")),"交易3",300.2],
                                                                    ["0004",time.mktime(time.strptime("2016-02-03","%Y-%m-%d")),"交易4",300.3],
                                                                    ["0004",time.mktime(time.strptime("2016-02-20","%Y-%m-%d")),"交易5",300]]],
              "4392600137250005":["123","user5",14399.9,0,0,0,0,[["0004",time.mktime(time.strptime("2015-12-19","%Y-%m-%d")),"交易1",300],
                                                                    ["0004",time.mktime(time.strptime("2015-12-21","%Y-%m-%d")),"交易2",300.1]
                                                                    ]]
              }
json.dump(account_info,open('account.txt','w'))
