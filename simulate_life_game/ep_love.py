# -*- coding:utf-8 -*-

"""
定义Love类，主要实现主角认识初恋以及遇到对手的情节
"""

import role
import settings
import time

class Love(object):
    def __init__(self):
        pass

    def love(self,target,rival):
        """
        主角恋爱的情节实现
        :param expression:target -主角色对象，rival -对手角色对象
        :return:
        """
        if target.sex=="男":
            lover_name="小美"
            lover_sex="女"
        else:
            lover_name="韩非"
            lover_sex="男"

        lover=role.BasicRole(lover_name,lover_sex,target.job,money=3000,position=3000,personal_charm=3000)
        target.talk("Hi, 我叫%s,能认识下吗？" %target.name)
        target.wait(1)
        lover.talk("你好, 我叫%s" %lover.name)
        lover.wait(1)
        print("...谈话进行的非常愉快....\n")
        target.talk("%s, 你愿意和我交往吗？" %lover.name)
        target.wait(1)
        lover.talk("嗯，我愿...")
        lover.wait(1)
        print("%s话还没说完，突然从旁边走来一个人\n" %lover.name)
        rival.talk("就你这样的，也想癞蛤蟆吃天鹅肉啊。。。哈哈")
        rival.wait(1)
        target.talk("你谁啊。。。关你什么事")
        target.wait(1)
        rival.talk("%s可是我的人，我的人你也敢碰？" %lover.name)
        rival.wait(1)
        rival.talk("怎么，不服？要不和我比比，看看你有多low？")
        user_choice=input("是否接受挑战【1是 2否】:")
        if user_choice.strip()=="1":
            target.talk("比就比，谁怕谁啊")
            result=target.receive_challenge(rival)  # 和 rival初次交手
            target.wait(1)
            if sum(result)>=2:   # result为list[money,position,personal_charm]。都为0表示主角在各个方面都比对手强
                rival.talk("真是不自量力，没钱，没地位，你这颜值也很low啊...")
                rival.wait(1)
                lover.talk("%s 不要理他，我们走..."%target.name)

            else:
                rival.talk("看不出啊，居然还有点料，不过你确定要惹我？")
            target.personal_charm += 1000
        else:
            rival.wait(1)
            target.talk("我...，为什么要和你比，%s我们走"%lover.name)
            target.wait(1)
            rival.talk("哈哈...，看到没%s，这就是你要找的人"%lover.name)
            rival.wait(1)
            lover.talk("%s你太让我失望了，%s我们走"%(target.name,rival.name))
            target.personal_charm -= 1000