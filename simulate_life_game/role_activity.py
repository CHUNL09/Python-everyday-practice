# -*- coding:utf-8 -*-

"""
定义Activity类，主要实现活动的生成
"""
class Activity(object):
    def __init__(self,name,detail,type,price,fame,charm,sp_attr):
        self.name=name
        self.detail=detail
        self.type=type
        self.price=price
        self.fame=fame
        self.charm=charm
        self.sp_attr=sp_attr  # 特殊属性，判断该活动是否有阴谋,>0表示有阴谋

