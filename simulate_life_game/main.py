#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
version: 1.0
author: liu chun
contact: cedrela_liu@163.com
date: 20160305
"""

import role
import role_activity
import menu
import ep_love
import ep_getskill
import ep_upgrade
import ep_challenge
import progress_out
import settings
import sys,time,os

def main():
    """
    main函数，集合了ep_love,ep_getskill,ep_upgrade,ep_challenge 等情节
    :param
    :return:
    """
    p_data=progress_out.Progress_out(settings.PROGRESS_DATA['sign'],settings.PROGRESS_DATA['interval'],settings.PROGRESS_DATA['rang'],settings.PROGRESS_DATA['w_interval'])
    # 生成p_data对象，用来打印进度条，或者一个个字符输出的功能
    print("=================模拟人生=================")
    p_data.generate_progress_bar()  # 打印进度条
    c=os.system('cls')
    # 生成主角色
    input_name=input("请输入角色的名称：")
    input_job=input("请选择角色的职业【1.%s 2.%s】"%(settings.ROLE_LIST[0],settings.ROLE_LIST[1]))
    input_sex=input("请选择角色的性别【1.男 2.女】")
    if input_job.strip()=='1':
        role_job=settings.ROLE_LIST[0]
    else:
        role_job=settings.ROLE_LIST[1]
    if input_sex.strip()=='1':
        role_sex='男'
    else:
        role_sex='女'
    me=role.BasicRole(input_name.strip(),role_sex,role_job)  # 创建完成主角色对象
    # 生成rival角色，在游戏中和主角色是同性别，同职业的对手。同时rival也是最后的BOSS
    rival=role.BasicRole(settings.RIVAL['name'],role_sex,role_job,money=settings.RIVAL['money'],position=settings.RIVAL['position'],personal_charm=settings.RIVAL['charm'])  # 创建完成主角色对象
    me.print_attr()
    welcome_str='''
    欢迎 %s 来到模拟人生游戏，在这个世界中，你的身份是一个刚毕业并且从事初级的 %s.你可以在这里获取金钱、技能、权利...
    游戏开始....
    ''' %(me.name,me.job)
    p_data.generate_progress_sentence(welcome_str)  # 单个字符输出 welcome_str

    ##############生成love_episode对象，并执行love()函数######################
    # love_episode 主要是主角和初恋认识的情节
    love_episode=ep_love.Love()
    love_opening=settings.love_opening
    p_data.generate_progress_sentence(love_opening)
    love_episode.love(me,rival)  # love()函数执行

    ##############生成getskill_episode对象，并执行find_master()函数############
    # getskill_episode 主要是主角奇遇老神仙，并获得特殊技能的情节
    getskill_episode=ep_getskill.Initial_Skill()
    getskill_opening=settings.getskill_opening
    p_data.generate_progress_sentence(getskill_opening)
    getskill_episode.find_master(me)  # 故事开始执行

    ##############生成upgrade_episode对象，并执行upgrade()函数############
    # upgrade_episode 主要是主角升级的情节
    upgrade_episode=ep_upgrade.Upgrade()
    upgrade_opening=settings.upgrade_opening
    p_data.generate_progress_sentence(upgrade_opening)
    upgrade_episode.upgrade(me)  # 故事开始执行

    ##############生成challenge_episode对象，并执行pk()函数############
    # challenge_episode 主要是主角和rival的最终对决的情节
    challenge_episode=ep_challenge.Challenge()
    challenge_opening=settings.challenge_opening
    p_data.generate_progress_sentence(challenge_opening)
    pk_res=challenge_episode.pk(me,rival,settings.PK_ATTR)  # 故事开始执行
    p_data.generate_progress_sentence(pk_res)

if __name__=='__main__':
    main()