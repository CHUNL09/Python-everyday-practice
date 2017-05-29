#!/usr/bin/env python

import atm_manage_interface
def admin_menu():
    msg='''
    ---------------ATM 管理界面--------------
    1.添加账户
    2.调整用户额度
    3.冻结账户
    4.退出
    -----------------------------------------
    '''
    print(msg)
    user_input=input("请选择：")
    return user_input

def main():
    while True:
        user_choice=admin_menu()
        if user_choice.strip()=="1":  # 添加账户
            atm_manage_interface.add_account()
        elif user_choice.strip()=="2":  # 调整额度
            atm_manage_interface.credit_limit_adjust()
        elif user_choice.strip()=="3":  # 冻结账户
            atm_manage_interface.lock_account()
        elif user_choice.strip()=="4":  # 退出
            exit("退出程序！")
        else:
            pass



if __name__=="__main__":
    main()
