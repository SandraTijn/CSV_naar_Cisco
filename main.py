from classes.CSVtoTXT import CSVtoTXT
from classes.SSHCisco import SSHCisco

csvToTxt = CSVtoTXT()

which_switch = input("Which type of switch to configure? (2 or 3)")
if which_switch in ("2", "3"):
    # files and hostname
    filepath_input = input(f"Which filepath for input? (leave blank for default in /data/input/inputcsv-L{which_switch}.csv)")
    if not filepath_input:
        filepath_input = f".//data//input//inputcsv-L{which_switch}.csv"
    filepath_output = input(f"Which filepath for output? (leave blank for default in /data/output/cisco_commands-L{which_switch}.txt)")
    if not filepath_output:
        filepath_output = f".//data//output//cisco_commands-L{which_switch}.txt"
    hostname = input(f"What should be the hostname? (leave blank for default = L{which_switch}Switch)")
    if not hostname:
        hostname = f"L{which_switch}Switch"

    # SSH credentials
    ip_address = input("What is the IP address?")
    if not ip_address:
        ip_address = "192.168.100.100" if which_switch == "3" else "192.168.100.101"
    username = input("What is the username (leave blank for default = cisco)")
    if not username:
        username = "cisco"
    password = input("What is the password?")
    if not password:
        password = "cisco"

    # generating config
    print(f"Generating L{which_switch} config...")
    if which_switch == "2":
        csvToTxt.make_L2_file(input_file=filepath_input, output_file=filepath_output, hostname=hostname)
    else:
        csvToTxt.make_L3_file(input_file=filepath_input, output_file=filepath_output, hostname=hostname)
    print(f"L{which_switch} config created!")

    # SSH config
    if not input("Want to apply? (Blank for yes, input for not)"):
        ssh_switch = SSHCisco(ip_address, username, password)
        # ssh_switch.check_connection()
        ssh_switch.execute_command_file(filepath_output)
        print("Config applied!")

        if not input("Want to reload? (Blank for yes, input for not)"):
            ssh_switch.reload()

    else:
        print("Not applied!")

    print("Done!")

    

else:
    print(f"{which_switch} is not recognised")
