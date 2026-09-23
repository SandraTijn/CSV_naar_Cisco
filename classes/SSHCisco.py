# klasse om via SSH verbinding te maken met een Cisco switch, en hier commando's op uit te voeren
from netmiko import ConnectHandler

class SSHCisco():
    def __init__(self, host, username, password):
        self.cisco_device = {
            "device_type": "cisco_ios",
            "host": "192.168.100.100",
            "username": "cisco",
            "password": "cisco",

            # Legacy SSH algorithms required by this old Cisco IOS
            "ssh_config_file": None,
            "disabled_algorithms": {},
            "conn_timeout": 10,
        }

    def execute_command(self, command):
        with ConnectHandler(**self.cisco_device) as net_connect:
            output = net_connect.send_command(command)
        print(output)

    def execute_command_file(self, filename):
        file = open(filename).readlines()
        print(file)
        for command in file:
            print(self.execute_command(command))