#!/usr/bin/env python

import sys,os

base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
import atm

def pay(money,merchant):
    """
    支付模块，该模块为外部调用接口
    :param expression: 金额，商户信息
    :return: 消费成功返回"success"
    """
    card=atm.login_auth()
    if card not in ["lock",None]:
        res=atm.consume(card,money,merchant)
        if res != None:
            return "success"
    else:
        return

#pay(3500,"京东商城")
