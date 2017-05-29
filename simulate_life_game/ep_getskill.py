# -*- coding:utf-8 -*-

"""
定义Initial_Skill类，主要实现主角认识师父以及获取特殊技能的情节
"""

import role
import settings
import time

class Initial_Skill(object):
    def __init__(self):
        pass

    def find_master(self,tranee):
        """
        主角认识师父以及获取特殊技能的情节
        :param expression:tranee -主角色对象
        :return:
        """
        if tranee.job=="Actor":
            s_skill="超级模仿"
        else:
            s_skill="透视眼"
        master=role.BasicRole("老头子","N/A",tranee.job,skill=s_skill,money=3000,position=1000,personal_charm=3000)
        master.talk("是否愿意拜我为师啊，我能帮助你更快达成你的目标！")
        master.wait(1)
        user_choice=input("请选择【1是 2否】:")   # 选择2，不会得到技能，但是会得到一定金钱
        receive=False
        if user_choice.strip()=="1":
            tranee.talk("好吧，老头子，希望你能帮到我")
            tranee.wait(1)
            tranee.get_teacher(master.name)
            master.talk("既然你已拜师，为师这里有一本秘籍，好好学习，希望它能帮助你。。。")
            master.wait(1)
            user_choice=input("是否接收【1是 2否】:")   # 选择2，不会得到技能，但是会得到一定金钱
            if user_choice.strip()=="1":
                tranee.talk("谢师傅。。。")
                tranee.wait(1)
                tranee.learn(master.skill)
                tranee.talk("我来看看这到底是什么技能。。。")
                tranee.wait(1)
                print("[%s]: %s\n" %(s_skill,settings.SKILL[s_skill]))  # 打印 skill的具体功能
                tranee.wait(1)
                tranee.talk("赚大发了，有了它，我就能够更快的提升自己。。。")
                receive=True
            else:
                pass
        if not receive:
            tranee.talk("还是算了吧，老头子，我一定是产生了幻觉")
            tranee.wait(1)
            master.talk("哎，好吧。总算是与你有缘，老夫送你一笔钱，你好自为之。。。")
            master.wait(1)
            tranee.talk("骗鬼呢你啊，还给钱呢。。。")
            tranee.wait(1)
            print("%s 已然不见踪影。。。\n" %master.name)
            tranee.talk("靠，地上是什么！！ %s RMB啊。。。。"%master.money)
