#!/usr/bin/env python

import sys,os
import json
base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
import atm
account_file="%s\\account.txt" %base_dir
log_file="%s\\atm.log" %base_dir
account_info=json.load(open(account_file,'r'))

def add_account():
    """
    添加帐户模块，用来添加帐户信息到account.txt文件中
    输入卡号： 439260013725000x
    初始密码：123
    用户名：userx
    :return:
    """
    card_num=input("请输入您要添加的卡号：")
    res=atm.query_account(card_num)
    if res==None:
        password=input("请输入卡号对应的初始密码：")
        username=input("请输入改卡用户名：")
        account_info[card_num]=[password,username,15000,0,0,0,0,[]]
        print("成功添加帐户 [%s]" %card_num)
        record="Add new credit card account [%s] success..." %card_num
        atm.wirte_log(record,log_file)
        json.dump(account_info,open(account_file,'w'))
    else:
        print("帐户[%s]已存在" %card_num)

def credit_limit_adjust():
    """
    修改用户可用额度
    输入卡号： 439260013725000x 后修改用户可用额度
    :return:
    """
    card_num=input("请输入卡号：")
    res=atm.query_account(card_num)
    if res!=None:
        print("[%s] 目前的额度是 [%s]" %(card_num,account_info[card_num][2]))
        new_credit=input("请输入新的额度：")
        account_info[card_num][2]=float(new_credit)
        print("[%s]的新额度为 [%s]" %(card_num,new_credit))
        record="Adjust credit card limit [%s] success..." %card_num
        atm.wirte_log(record,log_file)
        json.dump(account_info,open(account_file,'w'))
    else:
        print("没有找到帐户[%s]" %card_num)

def lock_account():
    """
    账号状态模块，用来管理用户卡号状态
    输入卡号： 439260013725000x 后根据提示锁定或者解锁用户卡
    :return:
    """
    card_num=input("请输入卡号：")
    res=atm.query_account(card_num)
    if res!=None:
        if account_info[card_num][6]>=3:
            print("帐户[%s] 目前已经是锁定状态" %card_num)
        else:
            print("帐户[%s] 目前未锁定" %card_num)
        user_input=input("锁定帐户L,解锁帐户U:")
        if user_input.strip(' ')=='L' or user_input.strip(' ')=='l':
            account_info[card_num][6]=3
            print("帐户[%s] 目前已经是锁定状态" %card_num)
            record="Lock credit card  [%s] success..." %card_num
            atm.wirte_log(record,log_file)
            json.dump(account_info,open(account_file,'w'))
        elif user_input.strip(' ')=='U' or user_input.strip(' ')=='u':
            account_info[card_num][6]=0
            print("帐户[%s] 目前已经解除锁定状态" %card_num)
            record="Ulock credit card  [%s] success..." %card_num
            atm.wirte_log(record,log_file)
            json.dump(account_info,open(account_file,'w'))
        else:
            print("错误的输入！")
    else:
        print("没有找到帐户[%s]" %card_num)