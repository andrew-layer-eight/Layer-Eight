# this script will search internal devices for BGP AS Numbers and print a list of ones in use. 
from netmiko import ConnectHandler #connecthandler from netmiko library
device_a = {
    "device_type": "cisco_ios_telnet",
    "ip": '192.168.1.100',
    "username": "admin",
    "password": "cisco",
    "port" : 32769, # only included as i was using EVE-NG which does port forwarding on Telnet. 
    "global_delay_factor": 3 # allows 300 seconds for command to complete. 
}
device_b = {
    "device_type": "cisco_ios_telnet",
    "ip": '192.168.1.100',
    "username": "admin",
    "password": "cisco",
    "port" : 32776, 
    "global_delay_factor": 3
}
all_devices = [device_a, device_b]

# run commands on devices
for devices in all_devices:
    connect = ConnectHandler(**devices) #ssh to the devices using the dictionary above
    output = connect.send_command("show ip bgp summary") # find the AS numbers
    bgp_sum = output.split()
    as_number = bgp_sum[7]
    hostname = connect.send_command("show run | i hostname") # find the devices hostname
    hostname1 = hostname.split()
    cisco_hostname = hostname1[1]
    print("BGP AS", as_number, "Is on:", cisco_hostname) # print the hostname and BGP AS Correlation

 # add a section to search for a specific AS Number
    print("Are you looking for a specific BGP AS Number?")
    input("Y/N: ")
    if input == 'Y':
        as_num = input("What AS Number? ")
        find_as_number = as_number.find("local AS number", as_num)
        print(find_as_number)
    else:    
    
