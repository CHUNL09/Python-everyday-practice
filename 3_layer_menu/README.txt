Python package "3_layer_menu"

Purpose: Provide a user 3 layer menu, to check provinces in China, cities in specific province, and counties in specific city

Author: Chun Liu (cedrela_liu@163.com)

Blog: http://www.cnblogs.com/cedrelaliu/

Licence: no

Version: 1.0 -- 2016-01-17

Versions of Python supported: 3.x   //running in 2.x will cause chinese character unreadable

External modules required: xlrd, you can download it from https://pypi.python.org/pypi/xlrd , uninstall the package,and use command "python setup.py install" to install

Files in the package:
   3_layer_menu.py -- python script for you to run
   China_city_list.xls  -- records of provinces, cities, and counties in China, format 'province city county'
   3_layer_menu_flow_chart -- flow chart of the program, illustration of processing logic
   
Function details:
1 this script allow user to query all the provinces in China, all the cities in specific province, and all the counties in specific city ;
2 you can press 'q' to exit the system, and press 'b' to return to parent layer menu';
3 Please enter the name of the province, city, counties. For example, it will print '29 上海市', the number
  before is just for better looking, if you need to choose this one, input '上海市';
4 when province input cannot find exact match, you need to input again;
5 please always use 'q' to exit the system, otherwise it will not exit automatically.

Quick start:
 Before start running the program, you need to make sure that you have xlrd module installed,
 your python is 3.x and your environment has no problem showing Chinese character. If you don't
 have xlrd module, it will not process *.xls file.

1 uninstall the package 3_layer_menu.zip
2 python 3_layer_menu.py
3 the login pages shows, as follows:
  全国省市县查询
  1 甘肃省
  2 新疆
  3 河北省
  ...
  29 上海市
  30 青海省
  31 海南省
  请选择输入一个省. 输入'q'退出系统
  请选择一个省：

4 press 'q' to exit the system!
  请选择输入一个省. 输入'q'退出系统
  请选择一个省： q
  已退出系统!

5 After enter a province, it will show all the cities in this province !
  请选择一个省： 广东省
  广东省 中有如下市级单位：
    1 云浮市
    2 惠州市
    3 潮州市
    ...
    19 河源市
    20 汕尾市
    21 韶关市
    请选择输入一个市级单位. 输入'b'返回上一级，输入'q'退出系统！
    请选择一个市级单位：

6 After enter a city, it will show all the counties in this province:
  请选择一个市级单位： 汕尾市
  汕尾市 中有如下县级单位:
   1     城  区
   2     海丰县
   3     陆河县
   4     陆丰市
   输入'b'返回上一级，输入'q'退出系统！
  返回上一级或者退出系统：

7 You can use b to return to parent layer if you're in city and county layer(in program layer2 and layer3):
  汕尾市 中有如下县级单位:
    1       城  区
    2     海丰县
    3     陆河县
    4     陆丰市
    输入'b'返回上一级，输入'q'退出系统！
    返回上一级或者退出系统： b
    广东省 中有如下市级单位：
    1 云浮市
    2 惠州市
    ...
    19 河源市
    20 汕尾市
    21 韶关市
    请选择输入一个市级单位. 输入'b'返回上一级，输入'q'退出系统！
    请选择一个市级单位：

8 And in each layer, you can always use 'q' to exit the system.

Download URLs: none

[中文简述]
1 特别强调：
       程序运行需要xlrd模块来处理xls文件，请在运行之前保证环境上该模块的正常；
       程序运行后界面显示以及交互主要基于中文，请使用python3.x(最好是最新版)运行，避免中文字符显示以及处理的问题；
       由于需要中文的显示和处理，请确保运行环境（操作系统）可以正常显示中文；
       选择输入时，请输入具体名称(不要在前面加空格输入)，比如'河源市',在目录中显示的列标仅为了美观而存在。
2 本程序包解压后包含3个文件：3_layer_menu.py,Chnia_city_list.xls,README.txt。文件作用以及内部格式说明
请参考 'Files in the package'部分的说明；
3 请仔细阅读'Function details' 中对程序功能的说明，包括输入'q'退出系统，'b'返回上一级目录等。
4 在测试程序前，请仔细阅读'Quick start' 部分，包括运行前你需要安装xlrd模块等。
5 如有意见，通过 Author 部分的邮箱联系我。
6 我的博客地址请参考'Blog'，谢谢。

