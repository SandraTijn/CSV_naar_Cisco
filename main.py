from classes.CSVtoTXT import CSVtoTXT
from classes.SSHCisco import SSHCisco

csvToTxt = CSVtoTXT()
sshCisco = SSHCisco("192.168.100.100", "cisco", "cisco")

csvToTxt.make_L3_file(input_file=".//data//input//inputcsv-L3.csv", output_file=".//data//output//cisco_commands-L3.txt")
csvToTxt.make_L2_file(input_file=".//data//input//inputcsv-L2.csv", output_file=".//data//output//cisco_commands-L2.txt")

# command = input("voer commando in (default None = \"show version\")")
# if not command:
#     command = "show version"
# sshCisco.execute_command(command)

# sshCisco.execute_command_file("cisco_commands.txt")
# sshCisco.execute_command_file("testcommandossh.txt")