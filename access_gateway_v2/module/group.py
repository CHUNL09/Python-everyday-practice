def query(cmd_dict): # 查某一台主机信息，或者某个组的信息
    group_list=cmd_dict['group']
    config=cmd_dict['group_config']
    for group_item in group_list:
        if config.has_section(group_item):
            print('---%s---'%group_item)
            print(config.options(group_item))
        else:
            print('Error: group %s cannot found...'%group_item)

def addgroup(cmd_dict):
    # gate 'group1,group2' group.addgroup
    group_list=cmd_dict['group']
    config=cmd_dict['group_config']
    for group_item in group_list:
        if config.has_section(group_item):
            print('Warning: group %s exist...'%group_item)
        else:
            config.add_section(group_item)
            print('Group %s added successfully...'%group_item)
    config.write(open(cmd_dict['config_file'][0],'w'))

def delgroup(cmd_dict):
    # gate 'group1,group2' group.delgroup
    group_list=cmd_dict['group']
    config=cmd_dict['group_config']
    for group_item in group_list:
        if config.has_section(group_item):
            config.remove_section(group_item)
            print('Group %s deleted successfully...'%group_item)
            print('Warning: group %s exist...'%group_item)
    config.write(open(cmd_dict['config_file'][0],'w'))

def rename(cmd_dict):
    """
    修改组名，这个还没做
    :param expression: 传入cmd_dict
    :return:
    """
    # gate 'old_group' group.rename 'new_group'
    pass

def addserver(cmd_dict):
    # gate 'group' group.addserver 'server1,server2...'
    group=str(cmd_dict['group'][0].strip())
    server_list=cmd_dict['argument']
    group_config=cmd_dict['group_config']
    server_config=cmd_dict['server_config']
    config_file=cmd_dict['config_file']
    print('test: ',group_config.sections())
    if group_config.has_section(group):
        for server in server_list:
            if group_config.has_option(group,server):
                pass
            else:
                group_config[group][server]=server
                server_config[server]['group']=group
                print('Server %s has been added to group %s' %(server,group))
        group_config.write(open(config_file[0],'w'))
        server_config.write(open(config_file[1],'w'))
    else:
        print('Error: group %s not found...'%group)

def delserver(cmd_dict):
    # gate 'group' group.delserver 'server1,server2...'
    group=cmd_dict['group'][0]
    server_list=cmd_dict['argument']
    group_config=cmd_dict['group_config']
    server_config=cmd_dict['server_config']
    config_file=cmd_dict['config_file']
    if group_config.has_section(group):
        for server in server_list:
            if group_config.has_option(group,server):
                group_config.remove_option(group,server)
                server_config.remove_option(server,'group')
                print('Server %s has been deleted to group %s' %(server,group))
            else:
                pass
        group_config.write(open(config_file[0],'w'))
        server_config.write(open(config_file[1],'w'))
    else:
        print('Error: group %s not found...'%group)

