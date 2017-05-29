love_opening='''
============love_episode start=============
在偶然的一场晚会上，我们相遇了...

'''
getskill_opening='''
==========getskill_episode start===========
想起之前的一幕幕，我的心里真的难以平复，痛苦么，还是其他...
突然，在眼前浮现出一个人影...

'''
upgrade_opening='''
==========upgrade_episode start============
为了我的未来，为了她/他，为了打败那个家伙，我要开始奋斗了...

'''
challenge_opening='''
==========challenge_episode start==========
这么多年，终于等到了这个时候，是时候做个了结了...

'''
#PROGRESS_DATA 中参数主要用于 progress_out文件中Progress_out类
PROGRESS_DATA={
    'sign':'#',
    'interval':0.1,
    'rang':61,
    'w_interval':0.2
}
RIVAL={
    'name':'老板',
    'money':10000,
    'position':10000,
    'charm':10000
}
ROLE_LIST=['Actor','Officer']
BACKGROUND={
    'Actor':'在这个模拟人生的世界中',
    'Officer':''
}

SKILL={
    '超级模仿':'使用该技能能够轻松模仿对手的能力，感知对手的弱点，从而击败对手',
    '透视眼':'使用该技能可以轻松看透对手的心思，立于不败之地'
}

Actor_menu={
    'name':'演员升级选项菜单',
    'type':'',
    'option':['广告代言','参加比赛','公益演出','被潜规则'],
    '广告代言':{
        'detail':'代言各种广告，可以赚取金钱，地位和魅力值',
        'type':'P',
        'price':5000,
        'fame':3000,
        'charm':2000,
        'sp_attr':0},
    '参加比赛':{
        'detail':'参加演技大赛，可以赚取地位和魅力值',
        'type':'P',
        'price':0,
        'fame':3000,
        'charm':3000,
        'sp_attr':0},
    '公益演出':
        {
        'detail':'参加公益演出，可以赚取地位和魅力值，但要消耗部分金钱',
        'type':'P',
        'price':-1000,
        'fame':6000,
        'charm':6000,
        'sp_attr':0},
    '被潜规则':
        {
        'detail':'xxx的老总对你印象不错，只要你能陪他/她一晚上，就不愁以后的高升啦',
        'type':'P',
        'price':4000,
        'fame':1200,
        'charm':-2000,
        'sp_attr':1}
}
# act_name,detail,type,price,fame,skill,cost,sp_attr
Officer_menu={
    'name':'公务员升级选项菜单',
    'type':'',
    'option':['党校进修','拉取赞助','下乡调研','收受贿赂'],
    '党校进修':{
        'detail':'参加党校进修，可以赚取地位和魅力值',
        'type':'P',
        'price':0,
        'fame':3000,
        'charm':3000,
        'sp_attr':0},
    '拉取赞助':
        {
        'detail':'参加拉取赞助，可以赚取金钱，地位和魅力值',
        'type':'P',
        'price':5000,
        'fame':3000,
        'charm':2000,
        'sp_attr':0},
    '下乡调研':
        {
        'detail':'参加下乡调研，可以赚取地位和魅力值，但要消耗一定金钱',
        'type':'P',
        'price':-1000,
        'fame':6000,
        'charm':6000,
        'sp_attr':0},
    '收受贿赂':
        {
        'detail':'xxx的老总的儿子刚好毕业，也是想考取我们单位。你去负责最后面试的时候，把这件事办好。就不愁以后的高升啦',
        'type':'P',
        'price':4000,
        'fame':1200,
        'charm':-2000,
        'sp_attr':1}
}
PK_ATTR={
    'place':'一家会所中....',
    'detail':'那我们就来比比看谁更有钱，有地位，有魅力...',
    'win_res':'多年之后，我成为了大多数人眼中的成功人士，和我现在的爱人结婚、生子。当初的事情就当作一场年前时的回忆吧...',
    'lose_res':'多年之后，我在很远的一座城市，做着简单地小生意，当初的事情已经彻底被埋在心里，不愿提起...'
}

