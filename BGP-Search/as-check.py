import requests
import json

#suppress HTTPS warnings
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# print a stream of pretty bytes as pretty JSON
def printBytesAsJSON(bytes):
    #print(json.dumps(json.loads(bytes), indent=2))

#Retreive configuration through RESTCONF
response = requests.get(
    url = "https://ios-xe-mgmt.cisco.com:9443/restconf/data/Cisco-IOS-XE-native:native/api/v1/routing-svc/bgp",
    auth = ("developer", "C1sco12345"),
    headers = {
        'Accept': 'application/yang-data+json'
    },
    verify = False)

#pretty print the JSON response
printBytesAsJSON(response.content)


#/api/v1/routing-svc/bgp

#restconf/data/Cisco-IOS-XE-native:native
