#!/usr/bin/env python

"""
version: 1.0
author: liu chun
contact: cedrela_liu@163.com
date: 20160211
"""
import re

# 定义全局变量，expression[0]用来存放修改后的表达式，final_result 用来存放最后的计算结果
expression=['',]
global final_result

# 计算乘法和除法
def mul_div(arg):
    pattern=re.compile("\d+\.*\d*[\*\/][\+\-]?\d+\.*\d*")   # 正则表达式，用来匹配乘法或者除法表达式
    if not pattern.search(arg[0]):
        return
    else:
        content=pattern.search(arg[0]).group()
        if '*' in content:  #乘法运算
            val1,val2=content.split('*')
            result=float(val1)*float(val2)
        elif '/' in content:  #除法运算
            val1,val2=content.split('/')
            result=float(val1)/float(val2)
        else:
            pass
        head,tail=pattern.split(arg[0],1)
        new_arg=["%s%s%s" %(head,result,tail),]  # result 为本轮计算的表达式的值，和原来的表达式拼接成新的表达式。即用结果替换原表达式，如 -8.0 替换 （-40/5）
        expression[0]=new_arg[0]
        mul_div(new_arg)     # 循环计算表达式，直到没有乘除位置

# 计算加减法
def add_sub(arg):
    if '++' in arg[0] or '--' in arg[0] or '+-' in arg[0] or '-+' in arg[0]:  # 如果有++、--、+-、-+ 等符号在表达式中，则分别替换为 +、+、-、-
        arg[0]=re.sub('\+\+','+',arg[0])
        arg[0]=re.sub('\+\-','-',arg[0])
        arg[0]=re.sub('\-\+','-',arg[0])
        arg[0]=re.sub('\-\-','+',arg[0])

    pattern=re.compile("[\+\-]?\d+\.*\d*")
    value_list=pattern.findall(arg[0])  # 将表达式中单个数字和前面符号放入列表中，如 ['-5','+8','-9']
    sum=0
    for i in range(len(value_list)):   # 将 value_list中所有值相加，结果放入sum 中返回
        sum += float(value_list[i])
    return sum

# 计算器函数，用于匹配括号内表达式，进行加减乘除运算
def calculator(arg):
    global final_result
    pattern=re.compile("\(([\+\-\*\/]*\d+\.*\d*){2,}\)")  # 匹配最小括号表达式，如(-40/8)
    if not pattern.search(arg[0]):  # 如果没有括号，则直接进行乘除加减运算
        mul_div(arg)
        final_result=add_sub(expression)
        return final_result
    else:
        content=[pattern.search(arg[0]).group(),]   # 将匹配到的括号及内部表达式放入content中进行乘除和加减的处理
        mul_div(content)
        content_value=add_sub(expression)
        print("计算 %s =%s" %(content[0],content_value))
        head,nothing,tail=pattern.split(arg[0],1)
        new_content=["%s%s%s" %(head,content_value,tail),]  # content_value 为表达式计算完成（加减乘除）的值，和原来的表达式拼接成新的表达式。即用结果替换原表达式，如 (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )
        print("下一步 %s" %new_content)                     # 计算完成的结果是 173545.88095238098，这里拼接后变为1 - 2 * ( (60-30 +(-40/5) * 173545.88095238098) - (-4*3)/ (16-3*2) )
        calculator(new_content)

if __name__=='__main__':
    str1=[input("请输入您要计算的表达式："),]             # 1 - 2 * ( (60-30 +(-40/5) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )
    str1[0]=re.sub('\s*','',str1[0])
    if str1[0].count('(')!= str1[0].count(')'):     # 如果用户输入的表达式中左右括号不匹配，则报错
        print("请检查，表达式中括号数量不匹配...")
    else:                                           # 括号匹配，直接计算
        print("您要计算表达式%s的值" %str1[0])
        print("计算中...")
        calculator(str1)
        print("结果为： %s" %final_result)