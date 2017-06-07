def query(cmd_dict):
    # gate 'server1,server2' server.query
    server_list=cmd_dict['server']
    config=cmd_dict['server_config'][1]
    for server_item in server_list:
        if config.has_section(server_item):
            print('---%s---'%server_item)
            for option in config[server_item]:
                print("%s: %s" %(option,config[server_item][option]))
        else:
            print('Error: server %s cannot found...'%server_item)

def addserver(cmd_dict):
    # gate 'server1' server.addserver 'ip xxx port xxx username xxx password xxx group xxx'
    server=cmd_dict['server'][0]
    para_list=list(cmd_dict['argument'].split(''))
    group_config=cmd_dict['group_config']
    server_config=cmd_dict['server_config']
    config_file=cmd_dict['config_file']
    if server_config.has_section(server):
        print('Error: server %s exist...' %server)
    else:
        if len(para_list)%2==0:
            for i in range(len(para_list)):
                if i%2==0:
                    server_config[server][para_list[i]]=para_list[i+1]
            if server_config[server]['group']!='default':
                group_config[server_config[server]['group']][server]=server
            group_config.write(open(cmd_dict['config_file'][0],'w'))
            server_config.write(open(cmd_dict['config_file'][1],'w'))
        else:
            print('Error: wrong argument number...')

def delserver(cmd_dict):
    # gate 'server1,server2' server.delserver
    server_list=cmd_dict['server']
    group_config=cmd_dict['group_config']
    server_config=cmd_dict['server_config']
    config_file=cmd_dict['config_file']
    for server in server_list:
        if server_config.has_section(server):
            if server_config[server]['group']!='default':
                group_config.remove_option(server_config[server]['group'],server)
            server_config.remove_section(server)
    group_config.write(open(cmd_dict[config_file][0],'w'))
    server_config.write(open(cmd_dict[config_file][1],'w'))

def chgrp(cmd_dict):
    # gate 'server1,server2..' server.chgrp 'group'
    server_list=cmd_dict['server']
    group=cmd_dict['argument'][0]
    group_config=cmd_dict['group_config']
    server_config=cmd_dict['server_config']
    config_file=cmd_dict['config_file']
    if group_config.has_section(group):
        for server in server_list:
            if server_config.has_section(server):
                group_name=server_config[server]
                if group_name!='default':
                    group_config.remove_option(group_name,server)
                group_config[group][server]=server
                server_config[server]['group']=group
            else:
                print('Error: server %s not exists...' %server)
        group_config.write(open(cmd_dict[config_file][0],'w'))
        server_config.write(open(cmd_dict[config_file][1],'w'))
    else:
        print('Error: group %s not exists...' %group)
