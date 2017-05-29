#!/usr/bin/env python

"""
version: 1.0
author: liu chun
contact: cedrela_liu@163.com
date: 20160202
"""

import json
import collections
import os

config_file='haproxy.txt'
temp_file='temp.txt'
content_list=[]    # 存放haproxy文件的列表，haproxy文件的每一行作为一个元素
match_record={}    # 存放匹配到的配置项的index值，以及配置项下面最后一条子记录的index值.比如 backend test.oldboy.org 所在的行index值为35
                   # 下面的最后一条子记录 server 100.1.7.9 100.1.7.9 weight 20 maxconn 3000 所在行的index值为38，那么在match_record
                   # 字典中会有一条记录 35:38
menu_list=['获取ha记录','增加ha记录','删除ha记录','退出']  #用来存放操作菜单

########## clear_content函数，用来清空content_list和match_record内容################
def clear_content():
    match_record.clear()
    content_list.clear()

########## generate_content_list函数，用来读取ha文件内容，并放入content_list中#########
def generate_content_list(clist,config_f):   # 接收两个参数，content_list列表和config_file
    with open(config_f,'r') as f_proxy:
        for line in f_proxy.readlines():
                clist.append(line)


########## print_record函数，用来打印匹配到的配置项和下面的子记录               #########
def print_record(config_f, record_line):     #传入配置文件名，配置项和子记录所在的字典，打印配置项和记录
    for i in record_line.keys():      # 循环配置项
        print(content_list[i])
        j=i
        while j<len(content_list)-1:   # 在每个配置项下去查找是否有子记录，如果找到就打印出来
            j +=1
            if content_list[j].startswith(' ') or content_list[j].startswith('\t'):  # 子记录以空格开头或'\t'开头
                match_record[i]=j
                print(content_list[j])
            else:
                break

########## get_record函数，接收用户输入的配置项，然后查询配置项以及下面的所有子记录 #########
def get_record(input_str):    #传入要查询的配置项，如 backend,www.oldboy.org
    str_temp=input_str
    for line in range(len(content_list)):   # 在content_list列表中查找配置项，如果找到的话在match_record中生成记录
        if str_temp.split(',')[0].strip()==content_list[line].split(' ')[0].strip() and str_temp.split(',')[1].strip()==content_list[line].split(' ')[1].strip():
            match_record[line]=0   # 如果找到匹配的配置项，把配置项的index，和初始化的最后一条子记录的index值0放入match_record中
    if len(match_record)>0:  # 如果找到配置项，调用print_record打印配置项和下面的子记录
        print("找到匹配的记录如下：")
        print_record(config_file,match_record)
        return 1
    else:
        print("没有查询到相关的记录！")
        return 0

########## add_record函数，接收用户输入的配置项和子记录，然后在ha文件中添加记录  #########
def add_record(input_dict):   #接收一个字典进来，如 {"backend": "test.oldboy.org","record":{"server": "100.1.7.9","weight": 20,"maxconn": 30}}
    for key in input_dict.keys():
        if key=='record':  # 把record对应的value格式化
            new_rec="\t\tserver %s %s weight %s maxconn %s\n" %(input_dict['record']['server'],input_dict['record']['server'],input_dict['record']['weight'],input_dict['record']['maxconn'])
        else:        # 把backend 对应的value格式化
            search_key="%s,%s" %(key,input_dict[key])
    result=get_record(search_key)   # 调用get_record去查询配置项
    if result==0:  #表示没有找到匹配的记录，直接在content_list列表最后添加配置项和子记录
        content_list.append("%s %s\n" %(search_key.split(',')[0],search_key.split(',')[1]))
        content_list.append(new_rec)
        print("成功添加一条记录！")
    else: #找到匹配的配置项，查找下面是否有要新增的子记录，没有就新增，有的话就报存在
        for index in match_record.keys():
            if match_record[index]==0:
                insert_index= index+1
                content_list.insert(insert_index,new_rec)
                print("成功添加一条记录！")
            else:
                add_flag=0  # flag位，值为1的时候表示找到匹配的子记录
                i=index+1
                while i<=match_record[index]:
                    if new_rec==content_list[i]: #表示找到匹配的子记录
                        print("子记录已存在配置项中")
                        add_flag=1
                        break
                    else:
                        i +=1
                if add_flag==0: #没有找到匹配的子记录，追加一条新记录
                    content_list.insert(i,new_rec)
                    print("成功添加一条记录！")

########## del_record函数，接收用户输入的配置项和子记录，然后在ha文件中删除记录  #########
def del_record(input_dict):   #接收一个字典进来
    for key in input_dict.keys():
        if key=='record':   # 把record对应的value格式化
            new_rec="\t\tserver %s %s weight %s maxconn %s\n" %(input_dict['record']['server'],input_dict['record']['server'],input_dict['record']['weight'],input_dict['record']['maxconn'])
        else:        # 把backend对应的value格式化
            search_key="%s,%s" %(key,input_dict[key])
    result=get_record(search_key)    # 调用get_record去查询配置项
    if result==0:     #表示没有找到匹配的记录
        print("您要删除的配置项和记录不存在!")
    else: #找到匹配的记录，删除记录
        deleted_flag=0   # flag为，值为1的时候表示删除了记录
        for index in match_record.keys():
            i=index+1
            if match_record[index]==i and new_rec==content_list[i]: #表示配置项下只有一条子记录，并且配置项和子记录都匹配，那么直接删除配置项和子记录
                content_list.pop(i)
                content_list.pop(index)
                print("成功删除一条记录！")
                deleted_flag=1
            else:  # 如果配置项下有多条子记录，循环查找每一条子记录，找到匹配的删除
                while i<=match_record[index]:
                    if new_rec==content_list[i]: #表示匹配到记录
                        content_list.pop(i)
                        match_record[index] -= 1
                        print("成功删除一条记录！")
                        deleted_flag=1
                    else:
                        i += 1
        if deleted_flag==0:
            print("没有找到要删除的子记录！")

########## write_config_file函数，用于把content_list中内如写入ha文件中    #########
def write_config_file(clist,config_f,temp_f):
    with open(temp_f,'w') as f_temp:
        for line in clist:
            f_temp.write(line)
    os.remove(config_f)
    os.rename(temp_f,config_f)


############         主程序入口                             ####################
def main():
    while True:
        clear_content()    # 初始化，清空全局字典和列表
        generate_content_list(content_list,config_file)  # 读取配置文件，初始化 content_list
        for i in range(len(menu_list)):   # 打印menu list，用户接收用户输入
            print("%s. %s"%(i,menu_list[i]))
        num=input('请输入操作序号： ')

        if not num.isdigit():  # 输入的非数字
            print("非法输入！")

        elif int(num)==0:   # 0 获取ha记录
            user_input=input("请输入要获取的记录：")      # 输入 backend,www.oldboy.org
            get_record(user_input)         # 查找该记录，并打印获取子记录
        elif int(num)==1:  # 1 增加ha记录
            user_input=input("请输入要增加的记录：")    # {"backend": "test.oldboy.org","record":{"server": "100.1.7.9","weight": 20,"maxconn": 30}}
            input_dict=json.loads(user_input)
            add_record(input_dict)
            write_config_file(content_list,config_file,temp_file)
        elif int(num)==2: # 2 删除ha记录
            user_input=input("请输入要删除的记录：")    # {"backend": "test.oldboy.org","record":{"server": "100.1.7.9","weight": 20,"maxconn": 30}}
            input_dict=json.loads(user_input)
            del_record(input_dict)
            write_config_file(content_list,config_file,temp_file)
        elif int(num)==3:  # 3 退出系统
            break
        else:
            print("非法输入！")

if __name__ == '__main__':
    main()