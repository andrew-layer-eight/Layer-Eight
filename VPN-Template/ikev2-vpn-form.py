from jinja2 import Environment, FileSystemLoader
import ipaddress

#pull the template from the directory
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
# find out the VPN type and then find out specific variables based on those types.
print("Is this a route based or policy based VPN? ")
vpn_type = input("> ")

# variables in the VPNs
party_name = input("Who is this for(3rd party)? ").upper().replace(" ", "")
domain = input("What is this envrionment(prod,dev,test)? ").upper().replace(" ", "")
dc = input("remote side DC? ")
vpn_name = party_name + "-" + domain
peer_pub_ip = input("What is their peer IP? ")
#peer_lan_ip = input("what is their LAN IP? ") 
local_pub_ip = input("What is our Peer IP? ") 
psk = input("please type the PSK: ")
ike_lifetime = int(input("what is the phase 1 lifetime? "))
ipsec_lifetime = int(input("Phase 2 sa lifetime? "))
pfs = input("is pfs required? (yes/no) ")
if pfs == "yes":
    pfs2 = int(input("PFS group? "))
else:
    pfs2 = "none"

# select the correct template based on the variables above. 
if vpn_type in "route":
    template = env.get_template('ikev2-rb-temp.txt')
    tunnel_int = int(input("what tunnel interface number? "))
    tunnel_ip = input("what is the IP and mask of the tunnel interface? ")
    tunnel_ip_mask = tunnel_ip.with_netmask

    output = template.render(vpn_name=vpn_name, peer_gw=peer_pub_ip, key=psk, local_peer=local_pub_ip, tunnel_int=tunnel_int, tunnel_ip=tunnel_ip, ike_lifetime=ike_lifetime, ipsec_lifetime=ipsec_lifetime, pfs2=pfs2, dc=dc)
else:
    template = env.get_template('ikev2-pb-temp.txt')
    cmap_name = input("Type the name of the crypto map (EXACT) > ")
    cmap_num = input("what is the next available CMAP number? ")
    local_traffic = input("Whats the local encryption domain? ")
    remote_traffic = input("Remote Encryption domain? ")
    
    output = template.render(vpn_name=vpn_name, peer_gw=peer_pub_ip, key=psk, local_peer=local_pub_ip, cmap_name=cmap_name, cmap_num=cmap_num, ike_lifetime=ike_lifetime, ipsec_lifetime=ipsec_lifetime, pfs2=pfs2, dc=dc, local_traffic=local_traffic, remote_traffic=remote_traffic)



# apply the variables to the template
#output = template.render(vpn_name=vpn_name, peer_gw=peer_pub_ip, key=psk, local_peer=local_pub_ip, tunnel_int=tunnel_int, tunnel_ip=tunnel_ip, ike_lifetime=ike_lifetime, ipsec_lifetime=ipsec_lifetime, pfs2=pfs2, dc=dc)
print(output)
# write the output to a txt file for future use.
file = open(f"{vpn_name.lower()}_vpn_config.txt", "w")
file.write(output)
file.close()

