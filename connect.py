import re
import socket
from importlib import reload

from ip_evaluate import get_accessible_ssh_tunnels
from interactive import interactive_shell
import paramiko

def connect_ssh(host, port, username, password, log_file=None):
    if re.match('^\d+(.\d+)+$', host) is not None:
        ip = host
    else:
        ip = get_accessible_ssh_tunnels(host, port, only_best=True)
        assert ip is not None, f'Can not find accessible ip of {host}:{port}'
    print(f'Start connecting to {ip}:{port}')
    # 记录日志
    reload(socket)
    if log_file is not None:
        paramiko.util.log_to_file(log_file)
    # 建立ssh连接
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port=int(port), username=username, password=password, compress=True)
    # 建立交互式shell连接
    channel = ssh.invoke_shell()
    # 建立交互式管道
    interactive_shell(channel)
    # 关闭连接
    channel.close()
    ssh.close()