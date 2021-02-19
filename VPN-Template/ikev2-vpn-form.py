from jinja2 import Environment, FileSystemLoader
import ipaddress
import itertools
import os

#-------------------------------------------- Functions ----------------------------------------------#

# Insert Encryption Domain Function, when you get it working!!!
    

#pull the template from the directory
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

# -------------------------------------- Find out VPN Type -----------------------#
print("Is this a route based or policy based VPN? ")
vpn_type = input("> ")
print("\n")
print("NOW COMPLETE THE FOLLOWING:")

# -------------------------------- Find out standard VPN information  -------------------------#
party_name = input("Who is this for(3rd party)? ").upper().replace(" ", "")
domain = input("What is this envrionment(prod,dev,test)? ").upper().replace(" ", "")
dc = input("remote side DC? ")
vpn_name = party_name + "-" + domain
peer_pub_ip = ipaddress.IPv4Address(input("What is their peer IP? "))
local_pub_ip = ipaddress.IPv4Address(input("What is our Peer IP? ")) 
psk = input("please type the PSK: ")
ike_lifetime = int(input("what is the phase 1 lifetime? "))
ipsec_lifetime = int(input("Phase 2 sa lifetime? "))
if ike_lifetime < ipsec_lifetime:
    print("Your Phase 1 lifetime must be longer or equal to your phase 2 lifetime!!")
    print("Double check the config!")
    exit()
pfs = input("is pfs required? (yes/no) ")
if pfs == "yes":
    pfs2 = int(input("PFS group? "))
else:
    pfs2 = "none"

# select the correct template based on the variables above and post them to the text file 

#----------------------------------- Route Based VPN Template ----------------------------------------#
if vpn_type in "route":
    template = env.get_template('ikev2-rb-temp.txt')
    tunnel_int = int(input("what tunnel interface number? "))
    tunnel_ip = ipaddress.ip_network(input("what is the IP and mask of the tunnel interface? "))
    output = template.render(vpn_name=vpn_name, peer_gw=peer_pub_ip, key=psk, local_peer=local_pub_ip, tunnel_int=tunnel_int, tunnel_ip=tunnel_ip, ike_lifetime=ike_lifetime, ipsec_lifetime=ipsec_lifetime, pfs2=pfs2, dc=dc)

#---------------------------------- Policy Based VPN Template ----------------------------------------#
else:
    template = env.get_template('ikev2-pb-temp.txt')
    cmap_name = input("Type the name of the crypto map (EXACT) > ")
    cmap_num = int(input("what is the next available CMAP number? "))
    # get the user to enter a subnet for the ACL - modify the rest in the template
    print("NOTE: enter ONE LOCAL encryption domain, we'll do the rest later!")

    local_traffic = input("Whats the local encryption domain? ")

    # ensure this is a valid IP and convert to wildcard mask
    host_wc_acl = ipaddress.ip_network(local_traffic).with_hostmask.replace("/", " ")

    print("NOTE: enter ONE REMOTE encryption domain!")
    remote_traffic = input("Whats the remote encryption domain? ")

    # ensure this is a valid IP and convert to wildcard 
    dest_wc_acl = ipaddress.ip_network(remote_traffic).with_hostmask.replace("/", " ")

    #create f string and use this in the jinja template
    #acl = print(f"ip permit {host_wc_acl} {dest_wc_acl}")
    output = template.render(vpn_name=vpn_name, peer_gw=peer_pub_ip, key=psk, local_peer=local_pub_ip, cmap_name=cmap_name, cmap_num=cmap_num, ike_lifetime=ike_lifetime, ipsec_lifetime=ipsec_lifetime, pfs2=pfs2, dc=dc, ed_local=host_wc_acl, ed_remote=dest_wc_acl)



#apply the variables to the template and show the user the result
print(output)
# write the output to a .txt file for future use.
file = open(f"{vpn_name.lower()}_vpn_config.txt", "w")
file.write(output)
file.close()
# tell the user where the file is located
#print(os.path.abspath(file))

