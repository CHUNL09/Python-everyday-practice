# -*- coding:utf-8 -*-

"""
version: 1.0
author: liu chun
contact: cedrela_liu@163.com
date: 20160305
定义了基本角色的类BasicRole，以及各种方法
"""
import role_activity
import time
class BasicRole(object):
    def __init__(self,name,sex,job,money=0,skill=None,teacher=None,lover=None,position=0,personal_charm=0):
        self.name=name
        self.sex=sex
        self.money=money
        self.skill=skill
        self.job=job
        self.teacher=teacher
        self.lover=lover
        self.position=position
        self.personal_charm=personal_charm

    def talk(self,sentences):
        print("%s: %s\n"  %(self.name,sentences))

    def wait(self,seconds):
        time.sleep(seconds)

    def get_teacher(self,t_name):
        self.teacher=t_name

    def learn(self,skill):
        self.skill=skill

    def receive_money(self,money):
        self.money +=money

    def get_in_love(self,lover):
        self.lover=lover.name

    def get_job(self):
        return self.job

    def escape(self):
        return "escape"

    def print_attr(self):
        print("=========角色的详细属性值=========")
        attr_dic='''
        角色名称: %s
        角色性别: %s
        金钱 : %s
        技能 : %s
        职业 : %s
        师傅 : %s
        爱人 : %s
        地位 : %s
        魅力 : %s
        '''%(self.name,self.sex,self.money,self.skill,self.job,self.teacher,self.lover,self.position,self.personal_charm)
        print(attr_dic)
        print("==================================")

    def receive_challenge(self,rival):
        """
        实现与对手的Pk
        :param expression: rival-对手角色对象
        :return:
        """
        result_list=[0,0,0] # 结果都为0表示 自己在各个方面(money,position,personal_charm)都比对方强
        if self.money<rival.money:
            result_list[0]=1
        if self.position<rival.position:
            result_list[1]=1
        if self.personal_charm<rival.personal_charm:
            result_list[2]=1
        return result_list

    def take_activity(self,activity):
        """
        参加活动的实现
        :param expression: activity-传入的activity 对象
        :return:
        """
        if activity.sp_attr==0:  # ps_attr 为activity的特殊属性，如果不是0，说明activity带有阴谋
            print("%s: 太好了，获取了 %s 的机会"%(self.name,activity.name))
        else:
            print("%s: %s 对现在的我是个难得的机会，没办法，上吧。。。"%(self.name,activity.name))
        print("%s: %s"%(activity.name,activity.detail))
        self.money += activity.price
        self.position += activity.fame
        self.personal_charm += activity.charm
        self.wait(1)
        print("%s: 终于结束了..."%self.name)
        print("恭喜你，获得了%s的金钱， %s的名气点, %s的魅力值" %(activity.price,activity.fame,activity.charm))

