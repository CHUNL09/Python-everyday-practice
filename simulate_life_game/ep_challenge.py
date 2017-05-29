# -*- coding:utf-8 -*-

"""
定义Challenge类，主要实现主角和rival最终对决的情节，主要是对比各种属性值来实现
"""

class Challenge(object):
    success_times=0
    def __init__(self):
        pass

    def pk(self,target,rival,pk_attr):
        """
        主角和rival最终对决的情节
        :param expression:target -主角色对象，rival-最终BOSS角色，pk_attr-pk相关的参数，在settings中设置
        :return:
        """
        rival.talk("哎，居然是你，这地方难道档次降低了，什么人都能来！")
        rival.wait(1)
        target.talk("哼，你管的着吗？")
        target.wait(1)
        rival.talk("真是没长进，看来还得我教教你怎么做人！！")
        rival.wait(1)
        target.talk("你配吗？")
        target.wait(1)
        rival.talk("你。。。")
        rival.talk("好，敢不敢和我比一下，如果你输了，你就赔我1000万。怎么样。。。。")
        rival.wait(1)
        target.talk("好啊，不过，如果我赢了，以后我出现的地方麻烦你滚的远远的。。。")

        print("=======pk开始=======")
        print(pk_attr['detail'])
        user_choice=input("选择【1继续 2逃跑】:")  # 选择逃跑会直接输
        if user_choice.strip()=="2":
            target.personal_charm -= 3000
            pk_result='lose'
        else:
            user_choice=input("是否使用专属技能【1是 2否】:")
            if user_choice.strip()=="1" and target.skill!=None:
                target.personal_charm += 2000
            else:
                pass
            pk_result=target.receive_challenge(rival)  # 主要是对比money，fame,personal_charm 值
            if sum(pk_result)>=2: # 如果有两项输了的话，则输掉了pk
                pk_result='lose'
            else:
                pk_result='win'
        if pk_result=='win':
            return pk_attr['win_res']
        else:
            return pk_attr['lose_res']

