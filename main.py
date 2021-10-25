import json
import paramiko
import getpass
import re
import os.path
from commands_map import \
    auth_type_cmd, \
    kernel_version_cmd, \
    network_if_cmd, \
    ssh_users_count_cmd, \
    sys_info_cmd, \
    cron_info_cmd, \
    ip_mask_mtu_cmd, \
    speed_cmd

while True:
    val = input("Enter full path to json file (press Enter for use default 'test_pool.json'): ")
    if val != '' and not os.path.isfile(val):
        print("File doesn't exist!")
    else:
        break

DEFAULT_PATH = 'test_pool.json' if not val else val

def get_ssh_client(host, user, secret, port):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, port=port, username=user, password=secret)

    return client

def exec_cmd(command):
    stdin, stdout, stderr = sshClient.exec_command(command)
    data = stdout.read().decode('ascii').strip("\n")

    return data

def get_auth_info():
    result = exec_cmd(auth_type_cmd.replace("uname", getpass.getuser()))

    return {'auth_info': 'by pass' if result == "False" else 'by key'}

def get_kernel_info():
    result = exec_cmd(kernel_version_cmd)

    return {'kernel_info': result}

def get_network_info():
    result = exec_cmd(network_if_cmd)
    net_interface = result.split()
    some_dict = {}

    for net in net_interface:
        result = exec_cmd(ip_mask_mtu_cmd.replace("NI_NAME", net))
        if len(result.split()) == 3:
            ip, mask, mtu = result.split()
        else:
            ip, mask, mtu = [None, None, None]

        result = exec_cmd(speed_cmd.replace("NI_NAME", net))
        speed = re.findall('\d+',result)
        speed = ''.join(speed)

        some_dict[net] = {'ip': ip, 'mask': mask, 'mtu': mtu, 'speed': str(speed) + ' Mb/s'}

    return {'network_info': some_dict}

def get_ssh_users_count():
    result = exec_cmd(ssh_users_count_cmd)

    return {'ssh_users_count': result}

def get_system_info():
    result = exec_cmd(sys_info_cmd)
    uptime, used_memory, load_15 = result.split()

    return {'system_info': {'uptime': uptime + ' min', 'used_memory': used_memory + ' %', 'avg_load_15': load_15}}

def get_cron_exist():
    result = exec_cmd(cron_info_cmd)

    return {'crons_exist': bool(result.split())}


with open(DEFAULT_PATH, 'r+') as json_file:
    json_data = json.load(json_file)
    hosts = json_data['hosts']

    for key, value in hosts.items():
        host = value['host']
        user = secret = value['user']
        port = '2200'

        sshClient = get_ssh_client(host, user, secret, port)

        auth_info = get_auth_info()
        kernel_info = get_kernel_info()
        network_info = get_network_info()
        ssh_users_count = get_ssh_users_count()
        system_info = get_system_info()
        cron_exist = get_cron_exist()

        json_data['hosts'][key]['auth_info'] = auth_info['auth_info']
        json_data['hosts'][key]['kernel_info'] = kernel_info['kernel_info']
        json_data['hosts'][key]['network_info'] = network_info['network_info']
        json_data['hosts'][key]['ssh_users_count'] = ssh_users_count['ssh_users_count']
        json_data['hosts'][key]['system_info'] = system_info['system_info']
        json_data['hosts'][key]['crons_exist'] = cron_exist['crons_exist']

        with open(DEFAULT_PATH, 'w') as f:
            f.write(json.dumps(json_data, sort_keys=False, indent=4, separators=(',', ': ')))

        sshClient.close()
