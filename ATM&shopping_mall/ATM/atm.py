#!/usr/bin/env python

"""
version: 1.0
author: liu chun
contact: cedrela_liu@163.com

帐户信息结构
{卡号：[密码，姓名，可用额度,本期欠款，实际还款，欠息，错误登录次数，[[卡号末4位，交易日期，商户名称，交易金额],...]]}
可用额度：用户实际可使用的额度，初始15000
本期欠款：初始为0，必须是本期出账之后才会更新
实际还款：记录用户本账期内实际的还款数，为负值
欠息：为用户迟交还款生成的利息
错误登录次数：大于等于3次即帐户锁定
"""
import json
import logging
import time,datetime
import os,sys
base_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
log_file='atm.log'
card_number=""
log_file="%s\\atm.log" %base_dir
account_file="%s\\account.txt" %base_dir
account_info=json.load(open(account_file,'r'))


def wirte_log(record,log_file):
    """
    写日志（内部配置了日志的格式）
    :param expression:日志record，日志文件
    :return:
    """
    logging.basicConfig(filename=log_file,
                    format='[%(asctime)s %(name)s %(levelname)s %(module)s]:  %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %p',
                    level=10)
    logging.info(record)

def query_account(card_num):
    """
    查询特定的银行卡账户
    :param expression:银行卡号
    :return: 银行卡号
    """
    for card in account_info:
        if card==card_num:
            record="query credit card account [%s] info success..." %card_num
            wirte_log(record,log_file)
            return card
    record="query credit card account info, not found [%s]" %card_num
    wirte_log(record,log_file)
    return

def query_detail(card_num):
    """
    查询特定的银行卡账户的详细信息，包括消费记录等
    :param expression:银行卡号
    :return: 消费记录列表
    """
    detail_list=[]
    for card in account_info:
        if card==card_num:
            record="query credit card account [%s] detailinfo success..." %card_num
            wirte_log(record,log_file)
            print("账户可用额度： %s" %account_info[card_num][2])
            detail_list=account_info[card_num][7]
            return detail_list
    record="query credit card account info, not found [%s]" %card_num
    wirte_log(record,log_file)
    return

def login_auth():
    """
    登录验证功能，3次错误锁定用户
    :param expression:
    :return: 成功返回卡号，锁卡返回"lock", 退出返回 None
    """
    while True:
        card_num=input("请输入信用卡卡号[q 退出]：")
        if card_num.strip('')=='q':
            record="exit login module success..."
            wirte_log(record,log_file)
            return
        password=input("请输入密码：")
        if query_account(card_num)!=None:
            if account_info[card_num][6]>=3:
                print("该卡目前已被锁定！")
                return "lock"
            elif password==account_info[card_num][0]:
                print("账户验证成功！")
                record="login card account [%s] info success..." %card_num
                wirte_log(record,log_file)
                return card_num
            else:
                print("密码输入错误！")
                record="login card account [%s] failed, wrong password..." %card_num
                wirte_log(record,log_file)
                account_info[card_num][6] +=1
                left_account= 3-account_info[card_num][6]
                if left_account>0:
                    print("剩余 %s 次机会!" %left_account)
                else:
                    print("该卡已被锁定！")
                    record="card account [%s] is locked due to 3 failed retry..." %card_num
                    wirte_log(record,log_file)
                    return "lock"
        else:
            print("卡号不存在，请重新输入")

def menu():
    """
    操作菜单
    :param expression:
    :return: 返回用户的输入
    """
    msg='''
    ---------------ATM 操作界面--------------
    1.取现
    2.查询
    3.还款
    4.转账
    5.退出
    -----------------------------------------
    '''
    print(msg)
    user_input=input("请选择：")
    return user_input

def cash_withdraw(card_number):
    """
    现金提取，手续费百分之5
    :param expression: 卡号
    :return:
    """
    user_input=input("请输入要提取的金额：")
    if float(user_input)>(account_info[card_number][2]/2):
        print("您输入的金额超过最大额度，请重新输入！")
    else:
        tmp_total=float(user_input)*1.05  # 手续费百分之5
        consume_record=[card_number[-4:],time.time(),"ATM 取款",float(user_input)]  # 生成交易记录，格式："0001","交易日期","商户名称","交易金额"
        account_info[card_number][7].append(consume_record)
        account_info[card_number][2] -= tmp_total   # 可用余额变更
        json.dump(account_info,open(account_file,'w'))
        record="withdraw cash %s from account [%s] success..." %(float(user_input),card_number)
        wirte_log(record,log_file)
        print(consume_record)
        # 打印输出信息

def tranfer(card_number):
    """
    转账，没有手续费，如果对方卡号是系统内部卡号（即，在account.txt文件中），则会额外添加一条消费记录到对方帐户，
    如果不是系统内部卡号，直接操作本卡号（生成一条转账记录）
    :param expression: 卡号
    :return:
    """
    transferer_card=input("请输入对方的卡号：")
    money=input("请输入要转账的金额：")
    print("您目前的可用额度为： %s" %account_info[card_number][2])
    if float(money)>account_info[card_number][2]:
        print("您没有足够的金额")
        record="transfer cash %s from account [%s] to account [%s] failed, insufficient credit limit..." %(money,card_number,transferer_card)
        wirte_log(record,log_file)
    else:
        if query_account(transferer_card)!=None:  # 如果对方的卡是同系统内，则额外处理对方数据
            consume_record=[transferer_card[-4:],time.time(),"ATM Transfer from %s" %card_number,0-float(money)]
            account_info[transferer_card][7].append(consume_record)
            account_info[transferer_card][2] += float(money)
        print("您已成功向账户[%s]转账 %s" %(transferer_card,money))
        consume_record=[card_number[-4:],time.time(),"ATM Transfer to %s" %transferer_card,money]
        account_info[card_number][7].append(consume_record)
        account_info[card_number][2] -= float(money)
        json.dump(account_info,open(account_file,'w'))
        record="transfer cash %s from account [%s] to account [%s] success..." %(money,card_number,transferer_card)
        wirte_log(record,log_file)

def consume(card,money,merchant):
    """
    消费模块，用来外部调用，如商城调用
    :param expression: 卡号，金额，商户信息
    :return: 成功支付返回"success"
    """
    if float(money)>account_info[card][2]:
        print("您目前卡上的余额为 %s,不足以支付该金额！" %account_info[card][2])
        return
    else:
        print("您已支付 %s" %money)
        consume_record=[card[-4:],time.time(),"%s 消费" %merchant,money]
        account_info[card][7].append(consume_record)
        account_info[card][2] -= float(money)
        record="pay %s from account [%s] success..." %(money,card)
        wirte_log(record,log_file)
        json.dump(account_info,open(account_file,'w'))
        return "success"

def add_consume_record(card_number,data_list):
    """
    添加消费记录，用来配合bill_generate.py来添加用户的消费记录
    :param expression: 消费记录列表
    :return:
    """
    account_info[card_number][2] -=(300.1+300.2+300.3)
    account_info[card_number][7].extend(data_list)
    print("成功添加如下交易记录")
    for item in data_list:
        print(item)
    json.dump(account_info,open('account.txt','w'))

def bill(card_number,transaction_date):
    """
    出账模块，每月22日出账，出账模块需要每个月22日执行一次，目前只对单卡号出账，
    对所有用户的出账后续实现
    :param expression: 卡号
    :return: 成功支付返回"success"
    """
    #user_input=input("请输入出账的日期：")
    current_date=datetime.date(year=int(transaction_date[:4]),month=int(transaction_date[5:7]),day=int(transaction_date[8:]))
    # current_date=datetime.date.today()
    start_day=int(current_date.strftime("%d"))+1
    start_month=int(current_date.strftime("%m"))-1
    start_year=int(current_date.strftime("%Y"))
    if start_month==0:
        start_month=12
        start_year -=1
    start_date="%s-%s-%s" %(start_year,start_month,start_day)
    end_date="%s-%s-%s" %(int(current_date.strftime("%Y")),int(current_date.strftime("%m")),int(current_date.strftime("%d")))
    due_day=10
    due_month=int(current_date.strftime("%m"))+1
    due_year=int(current_date.strftime("%Y"))
    if due_month==13:
        due_month=1
        due_year +=1
    due_date="%s-%s-%s" %(due_year,due_month,due_day)
    if current_date.strftime("%d")=="22": # 出账日出账
        tmp_detail=[]
        for transaction in account_info[card_number][7]:
            if transaction[1]>=time.mktime(time.strptime(start_date,"%Y-%m-%d")) and transaction[1]<time.mktime(time.strptime(end_date,"%Y-%m-%d")):
                tmp_detail.append(transaction)
        print("-----出账前-------")
        print("可用额度：%s 本期欠款：%s 实际还款：%s 欠息：%s" %(account_info[card_number][2],account_info[card_number][3],account_info[card_number][4],account_info[card_number][5]))
        print("-----开始出账-------")
        print("您的总额度为：%s\t可用额度为：%s" %(15000,account_info[card_number][2]))
        print("账单周期： %s -- %s" %(start_date,end_date))
        print("到期还款日： %s" %due_date)
        print("上期欠款： %s" %account_info[card_number][3])
        print("账单明细：")
        print("卡号后四位        交易日期       商户名称       交易金额")
        sum=0
        for item in tmp_detail:
            record="%5s %15s %25s %10s元" %(item[0],time.ctime(item[1]),item[2],item[3])
            print(record)
            sum += item[3]
        total_due=sum+account_info[card_number][3]+account_info[card_number][5]  # 本期还款总额=本期内交易总额+上期欠款+上期欠息
        account_info[card_number][3]= total_due   # 更新本期欠款
        account_info[card_number][5]=0   # 更新本期欠息为0
        account_info[card_number][4]=0   # 更新实际还款为0
        print("本期需要还款的金额为： %s" %total_due)
        record="generate bill for account [%s] success..." %card_number
        wirte_log(record,log_file)
        json.dump(account_info,open(account_file,'w'))
        print("-------出账后------------")
        print("可用额度：%s 本期欠款：%s 实际还款：%s 欠息：%s" %(account_info[card_number][2],account_info[card_number][3],account_info[card_number][4],account_info[card_number][5]))

def repay(card_number,transaction_date,money):
    """
    还款模块，每月10号是还款截止日期，在上一个出账日（上月22日）到本月10号之间还款，如果逾期还款，欠息为总欠款书的万分之5
    为了模拟特定某天还款，这里会接收输入还款日期
    :param expression: 卡号，还款日期，金额
    :return:
    """
    # 还款记录为负值
    print("------还款前--------")
    print("可用额度：%s 本期欠款：%s 实际还款：%s 欠息：%s" %(account_info[card_number][2],account_info[card_number][3],account_info[card_number][4],account_info[card_number][5]))
    #user_input=input("请输入还款金额：")
    #  0001","交易日期","商户名称","交易金额
    repay_num=0-float(money)
    account_info[card_number][4]+= repay_num    # 实际还款数目更新
    account_info[card_number][2] -= repay_num   # 可用额度更新
    print("成功还款 %s" %money)
    record="repay %s for account [%s] success..." %(repay_num,card_number)
    wirte_log(record,log_file)
    #user_input=input("请输入还款的日期：")   # 为了模拟特定某天还款
    current_date=datetime.date(year=int(transaction_date[:4]),month=int(transaction_date[5:7]),day=int(transaction_date[8:]))
    #current_date=datetime.date.today()
    repay_record=[card_number[-4:],time.mktime(time.strptime(str(current_date),"%Y-%m-%d")),"还款" ,repay_num]
    account_info[card_number][7].append(repay_record)
    tmp_day=22
    tmp_month=int(current_date.strftime("%m"))-1
    tmp_year=int(current_date.strftime("%Y"))
    if tmp_month==0:
        tmp_month=12
        tmp_year -=1
    last_bill_date="%s-%s-%s" %(tmp_year,tmp_month,tmp_day)
    overdue_interest=0
    if abs(account_info[card_number][4])>=account_info[card_number][3]:  # 还款总额大于等于欠款
        if int(current_date.strftime("%d"))>=23 or int(current_date.strftime("%d"))<=10:  #在还款期限内还款
            pass
        else: # 超过期限还款，计算欠息，为欠款总额万分之五每日计息
            overdue_interest=((time.mktime(time.strptime(str(current_date),"%Y-%m-%d"))-time.mktime(time.strptime(last_bill_date,"%Y-%m-%d")))/86400+1)*0.0005*account_info[card_number][3]
    else: # 还款总额小于等于欠款
        if int(current_date.strftime("%d"))<23 and int(current_date.strftime("%d"))>10:  # 超过还款期限
            overdue_interest=((time.mktime(time.strptime(str(current_date),"%Y-%m-%d"))-time.mktime(time.strptime(last_bill_date,"%Y-%m-%d")))/86400+1)*0.0005*account_info[card_number][3]
    account_info[card_number][5]=overdue_interest
    print("------还款后--------")
    print("可用额度：%s 本期欠款：%s 实际还款：%s 欠息：%s" %(account_info[card_number][2],account_info[card_number][3],account_info[card_number][4],account_info[card_number][5]))
    json.dump(account_info,open(account_file,'w'))




