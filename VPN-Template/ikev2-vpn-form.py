from jinja2 import Environment, FileSystemLoader

#pull the template from the directory
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

template = env.get_template('ikev2-temp.txt')

# variables in the VPNs
party_name = input("Who is this for(3rd party)? ").upper().replace(" ", "")
domain = input("What is this envrionment(prod,dev,test)? ").upper().replace(" ", "")
dc = input("remote side DC? ")
vpn_name = party_name + "_" + domain
peer_pub_ip = input("What is their peer IP? ")
peer_lan_ip = input("what is their LAN IP? ")
local_pub_ip = input("What is our Peer IP? ")
psk = input("please type the PSK: ")
tunnel_int = int(input("what tunnel interface number? "))
tunnel_ip = input("what is the IP of the tunnel interface? ")
ike_lifetime = int(input("what is the phase 1 lifetime? "))
ipsec_lifetime = int(input("Phase 2 sa lifetime? "))
#make htis an if statement
pfs = input("is pfs required? (yes/no) ")
if pfs == "yes":
    pfs2 = int(input("PFS group? "))
else:
    pfs2 = "none"


# apply the variables to the template
output = template.render(vpn_name=vpn_name, peer_gw=peer_pub_ip, key=psk, local_peer=local_pub_ip, tunnel_int=tunnel_int, tunnel_ip=tunnel_ip, ipsec_lifetime=ipsec_lifetime, pfs2=pfs2, dc=dc)
print(output)
# write the output to a txt file so can copy and paste it. 
file = open("vpn_config.txt", "w")
file.write(output)
file.close()
