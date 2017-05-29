#!/usr/bin/env python

"""
用来模拟验证出账和还款功能，特别是欠息的计算
"""

import time
import atm
import json
import time

#  使用测试账号为 4392600137250005，初始数据为 14399.9, 0, 0, 0[数据格式为”可用额度,本期欠款，实际还款，欠息“]

card_number="4392600137250005"
# step 1,执行下面的出账命令 出账日期： 2015-12-22
# time.sleep(1)

atm.bill(card_number,"2015-12-22")     # 出账日期： 2015-12-22
#
# # step 2,执行下面的还款命令
time.sleep(1)
atm.repay(card_number,"2015-12-30",300)   # 输入300元 2015-12-30，执行后 14699.9, 600.1, -300.0, 0

atm.repay(card_number,"2016-01-11",200)    # 输入200元 2016-01-11，执行后 14899.9, 600.1, -500.0, 6.301050000000001
# step 3,执行下面的命令，增加1月份的交易记录
time.sleep(1)
detail_list_01=[["0004",time.mktime(time.strptime("2016-01-14","%Y-%m-%d")),"交易2",300.1],
["0004",time.mktime(time.strptime("2016-01-18","%Y-%m-%d")),"交易3",300.2],
["0004",time.mktime(time.strptime("2016-01-20","%Y-%m-%d")),"交易4",300.3]]
atm.add_consume_record(card_number,detail_list_01)

# step 4,执行下面的命令，出一月份的账
time.sleep(1)
atm.bill(card_number,"2016-01-22")     # 出账前：13999.3, 600.1, -500.0, 6.301050000000001 输入出账日期： 2016-01-22， 出账后： 13999.3, 1007.0010500000001, 0, 0


# step 5,执行下面的命令，模拟逾期还款，欠息的计算
time.sleep(1)
atm.repay(card_number,"2016-02-12",2000)   # 输入2000元 2016-02-12，执行后 15999.3, 1007.0010500000001, -2000.0, 11.07701155


