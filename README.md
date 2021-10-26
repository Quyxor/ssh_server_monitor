# ssh_server_monitor
Tool for collecting information about a remote server. Script parsed json file with hosts and users, connect to hosts by ssh, collecting some info and add it to original json-file:
* What type of authorization can be used
* Version of operating system is on server
* Version of kernel is on server
* Network interfaces are and how they are configured. Сollect ip, mask, mtu, speed
* How many ssh users are currently on server
* How much system is running, how much memory is used in percent, what is average CPU load over last 15 minutes
* Finds out if there are any upcoming scheduled events in cron

Work on Python 3.* only

For start script run:
python main.py

Enter full path for target json file or press 'Enter' and script used test_pool.json, json file example in test_pool.json
