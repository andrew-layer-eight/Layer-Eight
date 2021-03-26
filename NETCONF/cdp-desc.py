# connect to devices via API, check all CDP neighbors, then based off the CDP information change the interface description to a particular format/standard. 
import requests
import os
import sys
from ncclient import manager
import xmltodict
import xml.dom.minidom

# Get the absolute path for the directory where this file is located "here"
here = os.path.abspath(os.path.dirname(__file__))

# Get the absolute path for the project / repository root
project_root = os.path.abspath(os.path.join(here, "../.."))


# Extend the system path to include the project root and import the env files
sys.path.insert(0, project_root)
import env_lab  # noqa
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

