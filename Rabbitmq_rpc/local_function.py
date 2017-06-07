#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 这个文件设计是和server.py文件放在一起，作为server的本地function的集合
# client端发送命令到server端后，server会在这里找到对应的函数，并把参数传入执行
# 这里可以扩充多个函数，函数需要接受cmd_para，是函数对应的参数
# 函数执行完成后必须有return值

def echo(cmd_para):
    return cmd_para

def fib(cmd_para):
    n=int(cmd_para)
    if n==0:
        return 0
    elif n==1:
        return 1
    else:
        return fib(n-1)+fib(n-2)