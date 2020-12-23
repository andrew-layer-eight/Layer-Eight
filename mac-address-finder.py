from netmiko import ConnectHandler #connecthandler from netmiko library
import re #regular expressions
#from getpass import getpass #password handler do this later
from threading import Thread # so i can run commands in parallel, this looks overly complicated at the moment... I'll leave it imported but wont use it. 
from datetime import datetime #timestamps for delay factor of ssh, again not used yet. 
starttime = datetime.now() # to do with threading.. not really needed

print("Welcome to MAC finder, this will search all switches in the network for a device MAC")

def cisco_mac(in_item): # convert the MAC address to a format Cisco IOS understands
    my_mac = [] #empty list
    index = 0
    for item in in_item:
        if str(index) in '48': # add a '.' after the 4th and 8th characters
            my_mac.append('.')
            my_mac.append(item)
        else:
            my_mac.append(item)
        index += 1
    return "".join(my_mac) #join the index together

user_mac = input("What is the MAC you're searching for: ").lower() # ask user for mac, make it lower case
in_mac = [letter for letter in user_mac if letter.isalnum()] #  remove all non alphanumeric characters, create a new variable 
mac_cisco = (cisco_mac(in_mac)) # create a variable from the function and user input

# create a dictionary for devices. this can be improved... 
device_a = {
    "device_type": "cisco_ios_telnet",
    "ip": '192.168.1.100',
    "username": "admin",
    "password": "password",
    "port" : 32770, # only included as i was using EVE-NG which does port forwarding on Telnet. 
    "global_delay_factor": 3 # allows 300 seconds for command to complete. 
}
device_b = {
    "device_type": "cisco_ios_telnet",
    "ip": '192.168.1.100',
    "username": "admin",
    "password": "password",
    "port" : 32773, 
    "global_delay_factor": 3
}
all_devices = [device_a, device_b]
""" This section is in progress, to work with above... find out how not to store creds in script and also to reference an IP/port list. 
ipfile = open("ipaddresses.txt")
#ask user for creds to login 
print("I need your credentials to login to the switches, sorry I'm not that clever.")
all_devices["username"] = input("What's your Username? ")
all_devices["password"] = input("What's the Password? ")
"""
for devices in all_devices:
    connect = ConnectHandler(**devices) #ssh to the devices using the dictionary above
    output = connect.send_command("show mac address-table | inc " + str(mac_cisco)) #now look for the MAC on these switches
    if mac_cisco in output: # find the mac, if it's there run this. 
        var_interface = output.split()
        interface = var_interface[7] # get the interface this MAC is on, may need to modify based on device type, tested on NXOS
        # get the hostname from the CORRECT device
        hostname = connect.send_command("show run | i hostname")
        hostname1 = hostname.split()
        cisco_hostname = hostname1[1] 
        print(f"This MAC: {mac_cisco} is on this device: {cisco_hostname} and this port: {interface}")
        break
    else:
        print("sorry can't find this MAC!")

print("MAC Search Engine has now Completed")

#exit from devices.
connect.disconnect()

