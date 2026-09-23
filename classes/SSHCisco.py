from netmiko import ConnectHandler


class SSHCisco:
    def __init__(self, host, username, password):
        self.cisco_device = {
            "device_type": "cisco_ios",
            "host": host,
            "username": username,
            "password": password,

            # Legacy SSH algorithms required by this old Cisco IOS
            "ssh_config_file": None,
            "disabled_algorithms": {},
            "conn_timeout": 10,
        }

    def check_connection(self):
        with ConnectHandler(**self.cisco_device) as net_connect:
            print(net_connect.send_command("show version"))

    def execute_command(self, command):
        with ConnectHandler(**self.cisco_device) as net_connect:
            return net_connect.send_command(command)

    def execute_command_file(self, filename):
        with ConnectHandler(**self.cisco_device) as net_connect:
            with open(filename, "r") as file:
                commands = [
                    line.strip()
                    for line in file
                    if line.strip()
                ]

            # Execute configuration commands
            config_commands = []
            save_requested = False

            for command in commands:
                if command.lower() in ("copy r s", "copy run start"):
                    save_requested = True
                else:
                    config_commands.append(command)

            if config_commands:
                net_connect.send_config_set(config_commands)

            # Save if requested in the configuration file
            if save_requested:
                net_connect.save_config()

    def save_config(self):
        with ConnectHandler(**self.cisco_device) as net_connect:
            net_connect.save_config()

    def reload(self):
        with ConnectHandler(**self.cisco_device) as net_connect:
            net_connect.send_command_timing("reload")
            net_connect.send_command_timing(
                "",
                strip_prompt=False,
                strip_command=False
            )