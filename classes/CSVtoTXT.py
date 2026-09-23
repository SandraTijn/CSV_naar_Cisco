# klasse om csv file om te zetten naar textfile met cisco commando's
import csv

class CSVtoTXT():
    def __init__(self):
        interface = "fa0/"

    def make_L3_file(self, input_file: str, output_file: str=None, hostname: str=None, interface: str="fa"):
        if not output_file:
            output_file = "cisco_commands-L3.txt"

        with open(input_file, "r", encoding="utf-8") as csv_file, \
            open(output_file, "w", encoding="utf-8") as output_file:

            output_file.write(f"ena\n")
            output_file.write(f"conf t\n")
            if hostname:
                output_file.write(f"hostname {hostname}\n")
            else:
                output_file.write(f"hostname L3Switch\n")
            output_file.write(f"ip routing\n")


            csv_reader = csv.reader(csv_file, delimiter=";")
            next(csv_reader, None)
            for line in csv_reader:
                if not line:
                    continue

                vlan_id = line[0]
                description = line[1]
                ip_address = line[2]
                netmask = line[3]
                switch = line[4]
                ports = line[5]

                if switch:
                    interface = f"{interface}{switch}/"
                else:
                    interface = f"{interface}0/"

                if "management" in description.lower():
                    output_file.write(f"vlan {vlan_id}\n")
                    output_file.write(f"name {description}\n")
                    output_file.write(f"int vlan{vlan_id}\n")
                    output_file.write(f"description {description}\n")
                    output_file.write(f"ip address {ip_address} {netmask}\n")
                    output_file.write(f"no shut\n")
                    if ports:
                        output_file.write(f"int {interface}{ports}\n")
                        output_file.write(f"switchport mode access\n")
                        output_file.write(f"switchport access vlan {vlan_id}\n")
                        output_file.write(f"description {description}-interface\n")

                elif "trunk" in description.lower():
                    # vlans
                    vlans = ""
                    vlans_list = vlan_id.split(",")
                    for vlan in vlans_list:
                        vlans += f"{vlan},"
                    vlans = vlans[:-1]
                    # print(vlans)


                    # native vlan
                    output_file.write(f"vlan 999\n")
                    output_file.write(f"name vlan999\n")
                    output_file.write(f"int vlan999\n")
                    output_file.write(f"description vlan999\n")
                    output_file.write(f"no shut\n")

                    # trunk
                    output_file.write(f"int {interface}{ports}\n")
                    output_file.write(f"description {description}\n")
                    output_file.write(f"switchport trunk encapsulation dot1q\n")
                    output_file.write(f"switchport mode trunk\n")
                    output_file.write(f"switchport trunk allowed vlan {vlans}\n")
                    output_file.write(f"switchport trunk native vlan 999\n")
                    output_file.write(f"no shut\n")

                elif vlan_id and description and ip_address and netmask:
                    # normal L3 vlan
                    output_file.write(f"vlan {vlan_id}\n")
                    output_file.write(f"name vlan{vlan_id}\n")
                    output_file.write(f"int vlan{vlan_id}\n")
                    output_file.write(f"description {description}\n")
                    output_file.write(f"ip address {ip_address} {netmask}\n")
                    output_file.write(f"no shut\n")

                    if ports:
                        if "-" in ports:
                            output_file.write(f"int range {interface}{ports}\n")
                        else:
                            output_file.write(f"int {interface}{ports}\n")
                        output_file.write(f"switchport mode access\n")
                        output_file.write(f"spanning-tree portfast\n")
                        output_file.write(f"switchport access vlan {vlan_id}\n")

                else:
                    print(f"line {line} is not supported")
            # copy run start
            output_file.write(f"end\n")
            output_file.write(f"copy r s\n")
            output_file.write(f"\n")

    def make_L2_file(self, input_file:str, output_file: str=None, hostname: str=None, interface :str="gi"):
            if not output_file:
                output_file = "cisco_commands-L2.txt"
    
            with open(input_file, "r", encoding="utf-8") as csv_file, \
                open(output_file, "w", encoding="utf-8") as output_file:
    
                output_file.write(f"ena\n")
                output_file.write(f"conf t\n")
                if hostname:
                    output_file.write(f"hostname {hostname}\n")
                else:
                    output_file.write(f"hostname L2Switch\n")
                output_file.write(f"no ip routing\n")
    
    
                csv_reader = csv.reader(csv_file, delimiter=";")
                next(csv_reader, None)
                for line in csv_reader:
                    if not line:
                        continue
    
                    vlan_id = line[0]
                    description = line[1]
                    ip_address = line[2]
                    netmask = line[3]
                    switch = line[4]
                    ports = line[5]

                    if switch:
                        interface = f"{interface}{switch}/"
                    else:
                        interface = f"{interface}0/"

                    if (ip_address or netmask) and "management" not in description.lower():
                        print(f"Line has IP config, is this L2? : {line}")
    
                    if "management" in description.lower():
                        output_file.write(f"vlan {vlan_id}\n")
                        output_file.write(f"name {description}\n")
                        output_file.write(f"int vlan{vlan_id}\n")
                        output_file.write(f"description {description}\n")
                        output_file.write(f"ip address {ip_address} {netmask}\n")
                        output_file.write(f"no shut\n")
                        if ports:
                            output_file.write(f"int {interface}{ports}\n")
                            output_file.write(f"switchport mode access\n")
                            output_file.write(f"switchport access vlan {vlan_id}\n")
                            output_file.write(f"description {description}-interface\n")
    
                    elif "trunk" in description.lower():
                        # vlans
                        vlans = ""
                        vlans_list = vlan_id.split(",")
                        for vlan in vlans_list:
                            vlans += f"{vlan},"
                        vlans = vlans[:-1]
                        # print(vlans)
    
    
                        # native vlan
                        output_file.write(f"vlan 999\n")
                        output_file.write(f"name vlan999\n")
                        output_file.write(f"int vlan999\n")
                        output_file.write(f"description vlan999\n")
                        output_file.write(f"no shut\n")
    
                        # trunk
                        output_file.write(f"int {interface}{ports}\n")
                        output_file.write(f"description {description}\n")
                        output_file.write(f"switchport trunk encapsulation dot1q\n")
                        output_file.write(f"switchport mode trunk\n")
                        output_file.write(f"switchport trunk allowed vlan {vlans}\n")
                        output_file.write(f"switchport trunk native vlan 999\n")
                        output_file.write(f"no shut\n")
    
                    elif vlan_id and description:
                        # normal L2 vlan
                        output_file.write(f"vlan {vlan_id}\n")
                        output_file.write(f"name vlan{vlan_id}\n")
                        output_file.write(f"int vlan{vlan_id}\n")
                        output_file.write(f"description {description}\n")
                        output_file.write(f"no ip address\n")
                        output_file.write(f"no shut\n")
    
                        if ports:
                            if "-" in ports:
                                output_file.write(f"int range {interface}{ports}\n")
                            else:
                                output_file.write(f"int {interface}{ports}\n")
                            output_file.write(f"switchport mode access\n")
                            output_file.write(f"spanning-tree portfast\n")
                            output_file.write(f"switchport access vlan {vlan_id}\n")

                    else:
                        print(f"line {line} is not supported")

                # copy run start
                output_file.write(f"end\n")
                output_file.write(f"copy r s\n")
                output_file.write(f"\n")


