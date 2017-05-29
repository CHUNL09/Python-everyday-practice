# -*- coding:utf-8 -*-

"""
定义Menu类，主要实现菜单的生成
"""

class Menu(object):  # menu name, type, option在settings中定义
    def __init__(self,name,type,option):
        self.name=name
        self.type=type
        self.option=option

    def generate_menu(self):
        """
        主要实现菜单的打印和生成
        :param expression:
        :return: 返回一个menu的字典
        """
        menu_dic={}
        for index,item in enumerate(self.option,0):
            print("%s.%s" %(index,item))
            menu_dic[index]=item
        return menu_dic
