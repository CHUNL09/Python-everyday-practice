#!/usr/bin/env python

"""
version: 1.0
author: liu chun
contact: cedrela_liu@163.com
date: 20160124

测试用账号可以新注册，也可以从account.txt文件中挑选
"""
import os
import time
import platform
import sys
import getpass

operating_system=platform.platform()     # 获取操作系统类型
path=sys.path[0]
if operating_system[:7]=="Windows":     # 根据操作系统类型不同来设置不同的文件路径格式
    user_account="%s\%s" %(path,'account.txt')
    temp_file="%s\%s" %(path,'temp.txt')
else:
    user_account="%s/%s" %(path,'account.txt')
    temp_file="%s/%s" %(path,'temp.txt')

user_account='account.txt'          #account.txt文件，存放用户名,密码,账户余额
temp_file='temp.txt'                #临时文件
username=''                         #全局变量，用户的账户名
password=''                         #全局变量，用户的密码
money=0.00                             #全局变量，用户的账户余额
cost=0.00                              #全局变量，用户消费的金额
price_list={                        # 定义的商品，用字典存储
    '笔记本':{ 'MacBook Air':6388.00, 'ASUS_Zenbook':4862.27,'Dell_Ins15CR':3199.00,'Toshiba_CB35':1866.17 },
    '平板电脑':{ 'ThinkPad 8':1999.00,'iPad_mini':1888.00,'Nokia':1099.00, '荣耀平板':799.00 },
    '图书':{ 'learning python':32.00, 'python cookbook':76.20, 'machine learning':48.70 },
    '家电':{ '冰箱':2870.35, '电视':1500.87, '剃须刀':380.00 },
    '服装':{ '风衣':1080.00, '皮鞋':699.99,  '内衣':105.76 },
    '食品':{ '牛奶':50.00,'茶叶':239.50, '大米':79.00}
}
shopping_car={}                    #用户的购物车，初始化定义为一个空字典，里面存储格式为： {‘商品’：[单价，购买的个数]}

while True:
    c=os.system('cls')
    reg_flag=0                    #注册成功的话，设置flag为1
    login_flag=0              #登录成功后flag设置为1
    login_msg="""
--------欢迎使用shopping mall系统--------
    您可以选择登录/注册/或者退出
    登录，请输入l
    注册，请输入r
    退出，请输入q
    """
    print(login_msg)
    user_input=input("请输入： ")
    if user_input.strip()=='q':      #直接退出程序！
        exit("已退出！")

    ######################### 注册模块 ####################
    elif user_input.strip()=='r':    #进入注册页面注册模块！
        print("--------注册页面--------")
        username_r=input("请输入注册的用户名：")
        password_r=getpass.getpass("请输入对应的密码：")
        if username_r.strip()=='' or password_r.strip()=='':   # 输入的用户名或密码为空
            print("用户名或密码为空，请重新输入！")
        else:
            with open(user_account,'r+') as f_append_account:   #读写模式打开account.txt
                find_user_flag=0    #flag位，等于1时表示用户名已经在account.txt文件中存在
                for line in f_append_account.readlines():
                    if username_r.strip()==line.split(',')[0].strip():  #如果用户名存在的话，提示并跳出循环
                        print("用户名已存在！")
                        find_user_flag=1
                        break
                if find_user_flag==0:  #如果是新用户，添加该用户到account.txt文件中，初始账户余额为0
                     newline="\n%s,%s,0" %(username_r,password_r)
                     f_append_account.write(newline)
                     print("用户 %s 已注册成功！" %username_r)
                     reg_flag=1
                     username=username_r         #把用户名赋值给全局变量username
                     password=password_r         #把密码赋值给全局变量password

    ######################### 登录验证模块 ####################
    elif user_input.strip()=='l':   #进入登录验证模块！
        print("--------登录验证页面--------")
        username_l=input("请输入注册的用户名：")
        password_l=getpass.getpass("请输入对应的密码：")
        with open(user_account,'r') as f_read_account:   #以读模式打开account.txt文件
            find_user_flag=0    # flag 为1时表示找到用户！
            for line in f_read_account.readlines():
                if username_l.strip()==line.split(',')[0].strip(): #如果用户名找到
                    find_user_flag=1
                    if password_l.strip()==line.split(',')[1].strip():  #如果密码也匹配，则提示登录成功
                        print("登录成功！欢迎 %s" %username_l)
                        login_flag=1
                        username=username_l                  #把用户名赋值给全局变量username
                        password=password_l                  #把密码赋值给全局变量password
                        money=float(line.split(',')[2].strip())     #把用户账户余额赋值给全局变量money
                        break
                    else:
                        print("密码错误，请重新输入！")
            if find_user_flag==0:   #表示在循环读文件中，没有找到匹配的用户名
                print("用户名不存在，请重新输入！")
    else:
        print("非法输入，请重新输入！")

    ######################### 充值模块 ####################
    if reg_flag==1 or login_flag==1:    # 注册成功或者登录成功后，进入充值模块
        while True:
            time.sleep(1)
            t=os.system('cls')
            print("欢迎%s，你目前的余额为： %0.2f" %(username,money))
            choice=input("请问是否选择充值（Y/N）： ")
            if choice.strip()=='y' or choice.strip()=='Y':    # 表示要充值
                input_money=input("请输入要充值的金额： ")
                if input_money.isnumeric():   # 表示输入的是有效地数字（非负数）
                    money += float(int(input_money))             # 把充值金额加到用户的账户余额上
                    with open(user_account,'r') as f_account:
                        with open(temp_file,'w') as f_temp:
                            newline="%s,%s,%0.2f" %(username,password,money)
                            for line in f_account.readlines():
                                if username==line.split(',')[0].strip():
                                    line=line.replace(line,newline)     # 在account.txt中更新用户的账户余额信息
                                f_temp.write(line)
                    os.remove(user_account)
                    os.rename(temp_file,user_account)
                    print("已经成功充值，您目前的帐户余额是： %0.2f" %money)
                    time.sleep(1)
                else: #输入的充值金额无效
                    print("无效的输入，请重新输入金额！")
            elif choice.strip()=='n' or choice.strip()=='N':  # 选择不充值，退出本模块
                break
            else:   # 非法输入
                print("非法输入，请重新输入！")

        while True:   #用于购物模块和结算模块的循环，比如结算模块选择继续购物后会进入购物模块
            ######################### 购物模块 ####################
            shop_flag=True
            while shop_flag:    # 购物模块-------not finished
                time.sleep(1)
                print("--------欢迎使用购物商城系统--------")
                for i,category in enumerate(price_list,1):   # 打印商品类别的菜单
                    print(i,category)
                user_choice1=input("请选择商品类别(f-完成购物，q-退出系统)：")   # 用户输入商品的类别
                if user_choice1.strip()=='q':           # 输入q退出系统
                    exit('退出系统!')
                elif user_choice1.strip()=='f':         # 输入f完成购物
                    print("您已经完成购物！")
                    break
                else:    # 输入商品类别名称后，进一步操作，选择商品等。。
                    find_category=0             # flag位，值为1表示找到匹配的商品类别
                    for category in price_list:
                        if user_choice1.strip()==category:    #匹配到商品类型后，进入到该商品类别的子目录
                            find_category=1            # 表示找到匹配的商品类别
                            item_flag=True
                            while item_flag:
                                for j,item in enumerate(price_list[category],1):    #打印category下的商品条目
                                    print("%d %s %0.2f" %(j,item,price_list[category][item]))
                                user_choice2=input("请选择商品(b-返回商品类别，f-完成购物)：")
                                if user_choice2.strip()=='b':   # 输入b，退出while循环，返回商品类别的选择
                                    break
                                elif user_choice2.strip()=='f': # 输入f，完成购物，退出while循环和购物模块
                                    print("您已经完成购物！")
                                    shop_flag=False
                                    break
                                else:   # 输入商品条目，如果匹配到的话，加入到购物车里
                                    find_product=0    # flag位，值为1表示找到匹配的商品条目
                                    for item in price_list[category]:
                                        if user_choice2.strip()==item:  #选择商品
                                            find_product=1   # 表示找到匹配的商品条目
                                            if item in shopping_car.keys():  #购买的商品已存在购物车中，则增加其数量
                                                shopping_car[item][1] += 1
                                                print("成功选购： %s" %item)
                                            else:   #购买的商品不在购物车中，添加新物品到购物车,购买次数设置为1
                                                shopping_car[item]=[price_list[category][item],1]
                                                print("成功选购： %s" %item)
                                    if find_product==0:
                                        print("错误的输入，请重新输入！")
                    if find_category==0:  #没有找到匹配的商品类别
                        print("错误的输入，请重新输入！")

            ######################### 结算模块 ####################
            while True:
                time.sleep(1)
                os.system('cls')
                print("--------购物车结算页面--------")
                if len(shopping_car)==0: #购物车中没有任何商品
                    print("您还没有购买任何商品！")
                else:
                    print("您的购物车中有如下商品： ")
                    cost=0.0 #设置cost为0
                    for i,item in enumerate(shopping_car,1):    #打印购物车中已购的商品信息
                        print("%s %s %0.2f %d" %(i,item,shopping_car[item][0],shopping_car[item][1]))
                        cost += float(shopping_car[item][0])*int(shopping_car[item][1])  #计算用户的消费金额
                print("您目前的帐户余额为： %0.2f" %money)
                print("购物车商品总价为： %0.2f" %cost)
                if money<cost:  #余额不够买所选的商品，提供删除或者充值的功能
                    print("您的余额不足，建议删除部分商品或者充值！")
                user_choice3=input("请输入命令继续（s-继续购买，d-删除商品，c-结算，r-充值，q-退出系统）：")

                ###################### 删除购物车中商品条目子模块 ##############
                if user_choice3.strip()=='d':   #删除条目
                    while True:
                        time.sleep(1)
                        os.system('cls')
                        if len(shopping_car)==0: #购物车中没有任何商品
                            print("您的购物车中没有任何商品，不能删除商品！")
                            break
                        else:
                            print("您的购物车中有如下商品： ")
                            for i,item in enumerate(shopping_car,1):   #打印购物车中已购的商品信息
                                print("%s %s %0.2f %d" %(i,item,shopping_car[item][0],shopping_car[item][1]))
                        if money<cost:           #余额不够买所选的商品，提供删除或者充值的功能
                            print("您的余额不足，建议删除部分商品或者充值！")
                        else:                    #余额足够支付提示
                            print("您的余额足够支付以上商品！")
                        user_choice4=input("请输入您要删除的商品名称(q-结束删除)：")
                        if user_choice4.strip()=='q':   #结束删除条目模块
                            break
                        else:   # 如果找到要删除的商品条目
                            find_delete_flag=0   # flag位，值为1时表示在购物车中找到匹配的要删除的商品条目
                            pop_item=''
                            for item in shopping_car.keys():
                                if user_choice4.strip()==item:   # 找到要删除的商品条目
                                    find_delete_flag=1         # 表示已经找到匹配的商品条目
                                    cost -= float(shopping_car[item][0])   #删除条目后，更新用户的消费金额
                                    if shopping_car[item][1]>1:   # 商品条目的购买次数如果大于1，删除的时候修改次数减1
                                        shopping_car[item][1] -= 1
                                    else:   # 商品条目的购买次数如果小于等于1，删除的时候直接从购物车中删除该商品条目的信息
                                        pop_item=item       # 删除的商品条目的名称赋值给pop_item
                            if len(pop_item)>0:          #如果有需要Pop的条目，则从shopping_car中pop
                                shopping_car.pop(pop_item)
                        if find_delete_flag==0:  # 没有匹配到要删除的商品条目，提示非有效的输入
                            print("非法输入，请重新输入！")

                ###################### 结算子模块 ##############
                elif user_choice3.strip()=='c':  #结算
                    time.sleep(1)
                    if money<cost:   # 如果账户余额不足以支付，提示删除或充值
                        print("您的余额不足，建议删除部分商品或者充值！")
                    else:    # 如果账户余额足够，结算生效
                        print("您的余额足够支付以上商品！")
                        money -= cost              # 从用户账户余额扣除消费金额
                        print("结算成功！您已成功购买商品！您的帐户余额为：%0.2f" %money)
                        with open(user_account,'r') as f_account:
                            with open(temp_file,'w') as f_temp:
                                newline="%s,%s,%0.2f" %(username,password,money)
                                for line in f_account.readlines():
                                    if username==line.split(',')[0].strip():
                                        line=line.replace(line,newline)    # 更新account.txt文件中用户的账户余额信息
                                    f_temp.write(line)
                        os.remove(user_account)
                        os.rename(temp_file,user_account)
                        exit("退出系统")

                ###################### 充值子模块 ##############
                elif user_choice3.strip()=='r':  # 充值模块
                    while True:
                        time.sleep(1)
                        t=os.system('cls')
                        print("欢迎%s，你目前的余额为： %0.2f" %(username,money))
                        user_choice5=input("请问是否选择充值（Y/N）： ")
                        if user_choice5.strip()=='y' or user_choice5.strip()=='Y':    # 表示要充值
                            input_money=input("请输入要充值的金额： ")
                            if input_money.isnumeric():   # 表示输入的是有效地数字（非负数）
                                money +=float(input_money)    # 计算充值后用户的账户余额
                                with open(user_account,'r') as f_account:
                                    with open(temp_file,'w') as f_temp:
                                        newline="%s,%s,%0.2f" %(username,password,money)
                                        for line in  f_account.readlines():
                                            if username==line.split(',')[0].strip():
                                                line=line.replace(line,newline)    # 更新account.txt文件中用户的账户余额信息
                                            f_temp.write(line)
                                os.remove(user_account)
                                os.rename(temp_file,user_account)
                                print("已经成功充值，您目前的帐户余额是： %0.2f" %money)
                            else: #输入的充值金额无效
                                print("无效的输入，请重新输入金额！")
                        elif user_choice5.strip()=='n' or user_choice5.strip()=='N':  # 选择不充值，退出本模块
                            break
                        else:   # 非法输入
                            print("非法输入，请重新输入！")
                elif user_choice3.strip()=='q':  # 输入q，退出系统
                    exit("已退出系统")   #考虑退出系统前是否更新用户的帐户余额
                elif user_choice3.strip()=='s': # 输入s，返回购物
                    break
                else:
                    print("非法输入，请重新输入！")
