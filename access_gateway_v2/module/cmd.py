import paramiko

def run(para_dict):
    """
    用于执行shell命令--时间不够，未调试修改
    :param expression: 传入cmd_dict，
    :return: 返回命令执行结果
    """
    hostname=para_dict['server']
    config=para_dict['server_config']
    ip=config[hostname]['ip']
    port=int(config[hostname]['port'])
    username=config[hostname]['username']
    password=config[hostname]['password']
    shell_cmd=para_dict['argument']
    transport=paramiko.Transport((ip,port))
    transport.connect(username=username,password=password)
    ssh=paramiko.SSHClient()
    ssh._transport=transport
    stdin,stdout,stderr=ssh.exec_command(shell_cmd)
    if len(stderr.read())==0: # 没有错误输出
        cmd_res=stdout.read().decode()
    else:
        cmd_res=stderr.read().decode()
    print("command execution result:")
    print(cmd_res)
    transport.close()
    return cmd_res


def put(para_dict):
    """
    执行upload文件上传命令
    :param expression:
    :return:
    """
    hostname=para_dict['server']
    config=para_dict['server_config']
    ip=config[hostname]['ip']
    port=int(config[hostname]['port'])
    username=config[hostname]['username']
    password=config[hostname]['password']
    local_file,remote_file=para_dict['argument'].split()
    transport=paramiko.Transport((ip,port))
    transport.connect(username=username,password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(local_file,remote_file)
    print("upload file %s successfully" %local_file)
    transport.close()

def get(para_dict):
    """
    执行download文件下载命令
    :param expression:
    :return:
    """
    hostname=para_dict['server']
    config=para_dict['server_config']
    ip=config[hostname]['ip']
    port=int(config[hostname]['port'])
    username=config[hostname]['username']
    password=config[hostname]['password']
    remote_file,local_file=para_dict['argument'].split()
     #本地文件添加后缀名.hostname，主要是为了区分，不同主机下载下来的同一个文件
    local_file="%s.%s" %(local_file,hostname)
    transport=paramiko.Transport((ip,port))
    transport.connect(username=username,password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.get(remote_file,local_file)
    print("download file %s successfully" %local_file)
    transport.close()
