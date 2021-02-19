import ipaddress
import itertools


def encryption_domains():

    local_traffic_list = []
    remote_traffic_list = []

    # get the number of subnets as input
    l_subnets = int(input("Enter number of Local Encryption Domain Subnets: "))

    # get the user to enter the subnets, line by line and append to list
    print("NOTE: Enter subnet with mask, then press enter and repeat!")
    for i in range(0,l_subnets):
        local_traffic_list.append(input("Whats the local encryption domain? "))

    # ensure this is a valid IP and convert to wildcard and make list
    host_wc_acl = [ipaddress.ip_network(item).with_hostmask.replace("/", " ").splitlines() for item in local_traffic_list]

    # get the number of subnets as input
    r_subnets = int(input("Enter number of Remote Encryption Domain Subnets: "))


    print("NOTE: Enter subnet with mask, then press enter and repeat!")
    for x in range(0,r_subnets):
        remote_traffic_list.append(input("Whats the remote encryption domain? "))

    # ensure this is a valid IP and convert to wildcard  and make list
    dest_wc_acl=[ipaddress.ip_network(item).with_hostmask.replace("/", " ").splitlines() for item in remote_traffic_list]

    #joing source and dest's together for every possible solution
    combinations = [" ".join(["ip permit"] + list(itertools.chain.from_iterable(a))) for a in itertools.product(host_wc_acl, dest_wc_acl)]

    print(combinations)


encryption_domains()


    


