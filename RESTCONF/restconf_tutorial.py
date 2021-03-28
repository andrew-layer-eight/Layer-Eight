#!/usr/bin/env python

#filename:                      restconf_tutorial.py
#command to run the program:    python restconf_tutorial.py

import requests
import json

#suppress HTTPS warnings
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# print a stream of pretty bytes as pretty JSON
def printBytesAsJSON(bytes):
    print(json.dumps(json.loads(bytes), indent=2))

#Retreive configuration through RESTCONF
response = requests.get(
    url = "https://ios-xe-mgmt.cisco.com:9443/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet=1",
    auth = ("developer", "C1sco12345"),
    headers = {
        'Accept': 'application/yang-data+json'
    },
    verify = False)

#pretty print the JSON response
printBytesAsJSON(response.content)

#configure an interface through RESTCONF

response = requests.patch(   
    url = "https://ios-xe-mgmt.cisco.com:9443/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet=1",
    auth = ("developer", "C1sco12345"),
    headers = {
        'Accept': 'application/yang-data+json'
    },
    data = json.dumps({
        'Cisco-IOS-XE-native:GigabitEthernet': {
			'ip': {
				'address': {
					'primary': {
						'address': '10.10.10.1',
						'mask': '255.255.255.0'
					}
				}
			}
		}
	}),
	verify = False)

# Print the HTTP response code - Successful is a 204 response code
print('Response Code: ' + str(response.status_code))