# -*- coding:utf-8 -*-

"""
定义Upgrade类，主要实现主角通过各种活动升级的情节
如果职业是演员，那么可选活动有：广告代言','参加比赛','公益演出','被潜规则'
如果职业是公务员，那么可选活动有：'党校进修','拉取赞助','下乡调研','收受贿赂'
不同的活动有不同的属性增值或者减值
"""
import role_activity
import role
import settings
import menu

class Upgrade(object):
    def __init__(self):
        pass
    def upgrade(self,target):
        """
        主角升级各种属性的情节
        :param expression:target -主角色对象
        :return:
        """
        job=target.get_job()  #获取角色职业类型
        if job=='Actor':  # 根据不同职业类型，从settings文件中获取对应职业的各种参数
            menu_attr=settings.Actor_menu
        else:
            menu_attr=settings.Officer_menu

        finish_flag=False
        while not finish_flag:   # 循环，可以多次选择不同的活动
            upgrade_menu=menu.Menu(menu_attr['name'],menu_attr['type'],menu_attr['option'])
            upgrade_menu_dic=upgrade_menu.generate_menu() # 生成upgrade_menu对象
            user_choice=input("请选择【q-跳过本次活动】:")   # 输入q跳过升级
            if user_choice.strip()=='q':
                pass
            elif int(user_choice.strip()) in list(upgrade_menu_dic.keys()):
                act_name=upgrade_menu_dic[int(user_choice.strip())]
                #活动的属性有name,detail,type,price,fame,charm,sp_attr，使用这些属性，然后生成activity对象
                activity=role_activity.Activity(act_name,menu_attr[act_name]['detail'],menu_attr[act_name]['type'],
                                                menu_attr[act_name]['price'],menu_attr[act_name]['fame'],
                                                menu_attr[act_name]['charm'],menu_attr[act_name]['sp_attr'])
                target.take_activity(activity)
            else:
                print("输入有误")

            user_choice=input("是否打印角色属性值【Y是N否】:")
            if user_choice.strip()=='Y':
                target.print_attr()
            user_choice=input("是否继续参加其他活动【Y是N否】:")
            if user_choice.strip()=='N':
                finish_flag=True