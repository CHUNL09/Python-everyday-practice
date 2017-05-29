Python package "process_haproxy_file"

Purpose: 修改haproxy配置文件（查询、增加、删除记录）

Author: Chun Liu (cedrela_liu@163.com)

Blog: http://www.cnblogs.com/cedrelaliu/

Licence: no

Version: 1.0

Versions of Python supported: 3.x 

External modules required: none

Files in the package:
   haproxy.txt -- haproxy的配置文件
   process_haproxy_file.py  -- 主程序文件
   process_haproxy_file_flow_chart -- 流程图，用于描述程序的逻辑

特别说明：
1 查询ha记录时，检索的条件是配置项，如: backend,buy.oldboy.org，而不是具体的子记录
2 增加和删除的时候，需要输入完整的配置项和子记录，如: {"backend": "test.oldboy.org","record":{"server": "100.1.7.9","weight": 20,"maxconn": 30}}.
  必须是这种格式，否则json模块报错
3 程序设计的时候，将backend,buy.oldboy.org 当作了配置项，而 server 100.1.7.90 100.1.7.90 weight 20 maxconn 3000 则是配置项下的子记录

Function details:
1 获取ha记录，输入要查询的配置项，如: backend,buy.oldboy.org，查找该配置项以及下面的子记录并打印 ;
2 增加ha记录，输入完整的配置项和子记录，如: {"backend": "test.oldboy.org","record":{"server": "100.1.7.9","weight": 20,"maxconn": 30}} 在ha配置文件中增加该记录;
3 删除ha记录，输入完整的配置项和子记录，如: {"backend": "test.oldboy.org","record":{"server": "100.1.7.9","weight": 20,"maxconn": 30}} 在ha配置文件中删除该记录;
4 退出，退出系统;


Quick start:

1 初始页面，输入序号选择功能
 0. 获取ha记录
 1. 增加ha记录
 2. 删除ha记录
 3. 退出
 请输入操作序号：

    
2 获取ha记录
  0. 获取ha记录
  1. 增加ha记录
  2. 删除ha记录
  3. 退出
   请输入操作序号： 0
   请输入要获取的记录：backend,buy.oldboy.org
   找到匹配的记录如下：
   backend buy.oldboy.org

           server 100.1.7.90 100.1.7.90 weight 20 maxconn 3000


3 增加ha记录，首先会去查询这条记录存在否，不存在的话添加，添加成功后提示
    0. 获取ha记录
    1. 增加ha记录
    2. 删除ha记录
    3. 退出
    请输入操作序号： 1
    请输入要增加的记录：{"backend": "test.oldboy.org","record":{"server": "100.1.7.9","weight": 20,"maxconn": 30}}
    没有查询到相关的记录！
    成功添加一条记录！


4 删除ha记录，首先会去查询这条记录存在否，存在的话删除，删除成功后提示
    0. 获取ha记录
    1. 增加ha记录
    2. 删除ha记录
    3. 退出
    请输入操作序号： 2
    请输入要删除的记录：{"backend": "test.oldboy.org","record":{"server": "100.1.7.9","weight": 20,"maxconn": 30}}
    找到匹配的记录如下：
    backend test.oldboy.org

            server 100.1.7.9 100.1.7.9 weight 20 maxconn 30

    成功删除一条记录！