#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: liuchun
# date: 20160106
# contact: cedrela_liu@163.com
# 3 layer menu--checking province,city,county in China
########################################################
import xlrd   # used to process Excel file
import time
import os,sys,platform
operating_system=platform.platform()           # get operating system type
path=sys.path[0]
if operating_system[:7]=="Windows":          # if os type is windows, then set the win-type path
    list_file=path+"\China_city_list.xls"
else:                                         # if os type is linux, set the linux-type path
     list_file=path+"/China_city_list.xls"
data = xlrd.open_workbook(list_file)                    # open the list_file
table=data.sheets()[0]                                  # get data sheet 1
rows=table.nrows                                        # get data rows

l1_set=set(table.col_values(0))                      # get first column values as province list, use set to reduce repeated values
col=l1_set.remove('')
l1_columns=list(l1_set)        # get province list and put them in l1_columns

l1_l2_combine=[]
l1_l2_match=[]                                       # list to store (province,city)
for i in range(rows):                               # generate 1-to-1 relationship between province and city
    temp=[(table.cell(i,0).value,table.cell(i,1).value)]
    l1_l2_combine.extend(temp)
l1_l2_match=list(set(l1_l2_combine))    # use set() to reduce repeated values in l1_l2_combine list

layer1_flag=False                    # flag for layer 1, if set True, then exit layer1
while layer1_flag==False:                                # loop for layer 1，checking all province
    print("全国省市县查询")
    for i in range(len(l1_columns)):                    # print layer 1 menu
        j=0
        j=i+1
        print(j,l1_columns[i])
    print("请选择输入一个省. 输入'q'退出系统")
    layer1_input=input("请选择一个省： ")
    if layer1_input.strip()=='q':                       # if input a 'q',exit the system
        break
    else:                                                # into the next layer menu
        for i in range(len(l1_columns)):
            if layer1_input==l1_columns[i]:    # if user input province find match in province list,then printing and further process
                layer2_flag=False
                while layer2_flag==False:                             # loop for layer 2
                    print("%s 中有如下市级单位： " %layer1_input)
                    k=1
                    for j in range(len(l1_l2_match)):           # print layer 2 menu
                        if layer1_input==l1_l2_match[j][0]:
                            print(k,l1_l2_match[j][1])
                            k += 1
                    print("请选择输入一个市级单位. 输入'b'返回上一级，输入'q'退出系统！")
                    layer2_input=input("请选择一个市级单位： ")
                    if layer2_input=='b':    # press 'b' to return to layer1
                        break
                    elif layer2_input=='q':   # exit layer2 loop and exit layer1 loop
                        layer2_flag=True
                        layer1_flag=True
                        break
                    else:   # checking and printing counties belong to input city.
                        print("%s 中有如下县级单位: " %layer2_input)
                        k=1
                        for i in range(rows):                     # print layer 3 menu
                            if layer2_input==table.cell(i,1).value.strip():    # compare user_input with city columns
                                print(k,table.cell(i,2).value)                # if match, print counties under this city
                                k +=1
                        if k==1:                    # k=1 means no records find
                            print("没有找到合适的记录，请重新输入！")
                            time.sleep(1)
                        else:
                            layer3_input='c'
                            while layer3_input!='b':          # layer3 loop for user input b or q
                                print("输入'b'返回上一级，输入'q'退出系统！")
                                layer3_input=input("返回上一级或者退出系统： ")
                                if layer3_input=='q':
                                    layer1_flag=True
                                    layer2_flag=True
                                    break
                                elif layer3_input!='b':
                                    print("非法输入，请重新输入！")
                                    time.sleep(1)
print("已退出系统!")







