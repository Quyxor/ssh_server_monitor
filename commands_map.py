auth_type_cmd = 'test -f .ssh/authorized_keys && grep uname .ssh/authorized_keys || echo False'
kernel_version_cmd = "uname -r"
network_if_cmd = "/sbin/ip -o link show | awk -F': ' '{print $2}'"
ip_mask_mtu_cmd = "/sbin/ifconfig NI_NAME | awk '/inet / {print $2}'; /sbin/ifconfig NI_NAME | awk '/netmask / {print $4}'; /sbin/ifconfig NI_NAME | awk '/mtu / {print $4}'"
speed_cmd = "/sbin/ethtool NI_NAME | grep -i Speed"
ssh_users_count_cmd = "w | grep pts | wc -l"
sys_info_cmd = """awk '{print $0/60;}' /proc/uptime ; free | awk '/Mem:/ {print $3/$2 * 100}' ; top -bn1 | awk '/average:/ {print $(NF)}'"""
cron_info_cmd = "crontab -l"