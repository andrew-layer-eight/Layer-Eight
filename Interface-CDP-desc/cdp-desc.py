# connect to devices via API, check all CDP neighbors, then based off the CDP information change the interface description to a particular format/standard. 
import requests


# list of devices

# cdp neighbor command

# define the format for the description
"""
interface xxxx
 description Remote_Hostname(Remote_Interface) - Speed 

"""

# print out the changes being made
# get user to confirm happy
print("This is the change being made: ")
"""
device xxxx
 interface xxxx
  description Remote_Hostname(Remote_Interface) - Speed 
 !
 interface xxxx
  description Remote_Hostname(Remote_Interface) - Speed 
!
!
device yyyyy
 interface yyyyy 
  description Remote_Hostname(Remote_Interface) - Speed 
"""
push = input("Confirm 'Y' to push:")
if push == 'Y' or 'y':
    #push the config
    print("pushing now... ")
else:
    print("not pushing this change, make up your mind!")
    #back out

# go to the interface in config mode & insert new description

