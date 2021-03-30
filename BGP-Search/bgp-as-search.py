from getpass import getpass #password handler do this later
from getpass import getuser
from netmiko import ConnectHandler #connecthandler from netmiko library

#open file for output
target = open("as-path-output.txt", 'w+')

username = getpass()
password = getpass()

# insert dictionary including all IP's you want to check here
all_devices = ["10.1.1.1", "10.208.1.1", "10.11.1.1"] 

 # run commands on devices
for ip in all_devices:
    device = {
    "device_type": "cisco_iosxe",
    "ip": ip,
    "username": username,
    "password": password,
    "global_delay_factor": 3
}
    connect = ConnectHandler(**device) #ssh to the devices using the dictionary above
    output = connect.send_command("show ip bgp summary") # find the AS numbers
    bgp_sum = output.split()
    as_number = bgp_sum[7]
    hostname = connect.send_command("show run | i hostname") # find the devices hostname
    hostname1 = hostname.split()
    cisco_hostname = hostname1[1]
    print("BGP AS", as_number, "Is on:", cisco_hostname) # print the hostname and BGP AS Correlation
    target.write("BGP AS", as_number, "Is on:", cisco_hostname)

# add a section to search for a specific AS Number
print("Are you looking for a specific BGP AS Number?")
input("Y/N: ")
if input == 'Y' or 'y':
    as_num = input("What AS Number? ")
    find_as_number = as_num.find("local AS number", as_num)
    print(find_as_number)
else: 
    print("Ok, I'll get you a list of ALL the AS Numbers i know about")

        
           

#--------------------------------- disconnect ---------------------------------#
connect.disconnect()
