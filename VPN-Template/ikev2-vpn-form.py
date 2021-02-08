from jinja2 import Environment, FileSystemLoader

#pull the template from the directory
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

template = env.get_template('ikev2-temp.txt')

# variables in the VPNs
party_name = input("Who is this for(3rd party)? ").upper().replace(" ", "")
domain = input("What is this envrionment(prod,dev,test)? ").upper().replace(" ", "")
vpn_name = party_name + "_" + domain
peer_pub_ip = input("What is their peer IP? ")
local_pub_ip = input("What is our Peer IP? ")
peer_lan_ip = input("what is their LAN IP? ")
psk = input("please type the PSK: ")


output = template.render(vpn_name=vpn_name, peer_gw=peer_pub_ip)

print(output)
