import ipaddress
import itertools


# get the user to enter one subnet for the ACL - modify the rest in the template
print("NOTE: enter ONE LOCAL encryption domain, we'll do the rest later!")

local_traffic = input("Whats the local encryption domain? ")

# ensure this is a valid IP and convert to wildcard mask
host_wc_acl = ipaddress.ip_network(local_traffic).with_hostmask.replace("/", " ")

print("NOTE: enter ONE REMOTE encryption domain!")

remote_traffic = input("Whats the remote encryption domain? ")

# ensure this is a valid IP and convert to wildcard 
dest_wc_acl= ipaddress.ip_network(remote_traffic).with_hostmask.replace("/", " ")

#create f string and use this in the jinja template
acl = print(f"ip permit {host_wc_acl} {dest_wc_acl}")