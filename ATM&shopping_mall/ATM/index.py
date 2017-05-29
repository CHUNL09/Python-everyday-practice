#!/usr/bin/env python

"""
version: 1.0
author: liu chun
contact: cedrela_liu@163.com
date: 20160227

帐户信息结构
{卡号：[密码，姓名，额度,{交易信息:[卡号末4位，交易日期，商户名称，交易金额，额度]}]}
"""
import time
import atm

def main():
    card=atm.login_auth()    # 初始登录验证，要求输入卡号，如：4392600137250004 密码默认为 123
    while card.strip() not in ["lock",None]:
        user_choice=atm.menu()
        if user_choice.strip()=="1":  # 提取现金
            atm.cash_withdraw(card)
        elif user_choice.strip()=="2":  # 账户查询
            detail=atm.query_detail(card)
            print("账户消费信息如下：")
            print("卡号后四位    消费日期    交易类型    金额")
            for item in detail:
                record="%5s %15s %15s %10s元" %(item[0],time.ctime(item[1]),item[2],item[3])
                print(record)
        elif user_choice.strip()=="3":  # 还款
            repay_date=input("请输入还款日期(格式\"YYYY-mm-dd\")：")
            repay_money=input("请输入还款金额：")
            atm.repay(card,repay_date,repay_money)
        elif user_choice.strip()=="4":  # 转账
            atm.tranfer(card)
        elif user_choice.strip()=="5":  # 退出
            exit("退出程序！")
        else:
            pass


if __name__=="__main__":
    main()
