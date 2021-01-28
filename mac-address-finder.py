from netmiko import ConnectHandler #connecthandler from netmiko library
import re #regular expressions
from getpass import getpass #password handler do this later
from getpass import getuser

print("Welcome to MAC finder, this will search all switches in the network for a device MAC")

#--------------------------------- Regex ---------------------------------#

interface_regex = re.compile(r"(?:GigabitEthernet|TenGigabitEthernet|FastEthernet|FortyGigabitEthernet|Eth)\d+((/\d+)+(\.\d+)?)?")
access_regex = re.compile(r"(\sOperational\sMode\:\saccess)")

#--------------------------------- Start of Functions ---------------------------------#

# convert the mac address to Cisco standard xxxx.xxxx.xxxx
def cisco_mac(in_item): 
    my_mac = [] 
    index = 0
    for item in in_item:
        if str(index) in '48': 
            my_mac.append('.')
            my_mac.append(item)
        else:
            my_mac.append(item)
        index += 1
    return "".join(my_mac) 

# show commands on switch to get interface, port mode, hostname
def switch_commands():
    for line_item in output.splitlines():
        if mac_cisco in line_item:       
            var_int = interface_regex.search(line_item)
            interface = var_int.group()
            sh_int = connect.send_command("show interface " + interface + " switchport") #look at the interface details
            #access_port = "Operational Mode: access"
            #x = sh_int.splitlines()
            for port_info in sh_int.splitlines():
                var_mode = access_regex.search(port_info)
                if var_mode is not None:
                # get the hostname from the CORRECT device
                    hostname = connect.send_command("show run | i hostname")
                    hostname1 = hostname.split()
                    cisco_hostname = hostname1[1] 
                    print(f"This MAC: {mac_cisco} is on this device: {cisco_hostname} and this port: {interface}") 
                    break
                else: # if port-mode doesn't have access, continue until it finds it - Layer 2 environments
                    continue
            else:
                break
        else:
          print("sorry can't find this MAC! - have you typed it correctly?")

# for threading, connecting to all devices in parallel rather than running through one by one. 
#def connect_devices:

#

#--------------------------------- End of Functions ---------------------------------#

#--------------------------------- File's with IP addresses of devices per region ---------------------------------#
europe_ip_addr_file = open("ip-europe.txt")
europe_ip_addrs = europe_ip_addr_file.read().splitlines()
london_ip_addr_file = open("ip-london.txt")
london_ip_addrs = europe_ip_addr_file.read().splitlines()
denver_ip_addr_file = open("ip-denver.txt")
denver_ip_addrs = europe_ip_addr_file.read().splitlines()
us_ip_addr_file = open("ip-us.txt")
us_ip_addrs = europe_ip_addr_file.read().splitlines()
asia_ip_addr_file = open("ip-asia.txt")
asia_ip_addrs = europe_ip_addr_file.read().splitlines()
aus_ip_addr_file = open("ip-aus.txt")
aus_ip_addrs = europe_ip_addr_file.read().splitlines()

#---------------- Dictionary ------------------#
location = {
    "London": london_ip_addr_file
}

print("valid locations are: London, Denver, Europe, Asia, USA, Australia")
location = input("Which location are you in: ")
user_mac = input("What is the MAC you're searching for: ").lower() # ask user for mac, make it lower case
in_mac = [letter for letter in user_mac if letter.isalnum()] #  remove all non alphanumeric characters, create a new variable 
mac_cisco = (cisco_mac(in_mac)) # create a variable from the function and user input



username = getuser() #this takes the current logged in user - will need changing if using a different account to  log in. 
password = getpass()


# create a dictionary for devices. this can be improved... 
device_a = {
    "device_type": "cisco_ios_telnet",
    "ip": '192.168.1.100',
    "username": username,
    "password": password,
    "port" : 32770, # only included as i was using EVE-NG which does port forwarding on Telnet. 
    "global_delay_factor": 3 # allows 300 seconds for command to complete. 
}
device_b = {
    "device_type": "cisco_ios_telnet",
    "ip": '192.168.1.100',
    "username": username,
    "password": password,
    "port" : 32773, 
    "global_delay_factor": 3
}
all_devices = [device_a] #device_b]
""" This section is in progress, to work with above... find out how not to store creds in script and also to reference an IP/port list. 
ipfile = open("ipaddresses.txt")
"""



#--------------------------------- Start of Job ---------------------------------#
for devices in all_devices:
    connect = ConnectHandler(**devices) #ssh to the devices using the dictionary above
    output = connect.send_command("show mac address-table | inc " + str(mac_cisco)) #now look for the MAC on these switches
    if mac_cisco in output: 
        # Turn this into a function!!! 
        for line_item in output.splitlines():
            if mac_cisco in line_item:       
                var_int = interface_regex.search(line_item)
                interface = var_int.group()
                sh_int = connect.send_command("show interface " + interface + " switchport") #look at the interface details
                #access_port = "Operational Mode: access"
                x = sh_int.splitlines()
                for port_info in sh_int.splitlines():
                    var_mode = access_regex.search(port_info)
                    if var_mode is not None:
                         # get the hostname from the CORRECT device
                        hostname = connect.send_command("show run | i hostname")
                        hostname1 = hostname.split()
                        cisco_hostname = hostname1[1] 
                        print(f"This MAC: {mac_cisco} is on this device: {cisco_hostname} and this port: {interface}") 
                        break
                    else: # if port-mode doesn't have access, continue until it finds it. Layer 2 environments
                        continue
            else:
                break
    else:
        print("sorry can't find this MAC! - have you typed it correctly?")

print("MAC Finder has now completed")

#--------------------------------- disconnect ---------------------------------#
connect.disconnect()

# add search location EUROPE, LONDON etc then use a different list for those locations
