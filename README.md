# About pySpot

**pySpot** was written to pass through the captive portals in public Wi-Fi networks by hijacjing auttorized IP/MAC addresses.

Be careful, this script needs to be run under Linux (*tested on Kali*)

## Usage

Print the help to get all necessary information

```bash
$ sudo python3 pySpot.py -h
usage: pySpot.py [-h] --iface IFACE [--ip] [--verbose]

Public Wi-Fi HotSpot ByPass

options:
  -h, --help     show this help message and exit
  --iface IFACE  Specify Wireless Interface conncted to HotSpot Wi-Fi
  --ipspoof      Hijack MAC AND IP addresses
  --verbose      Set verbose mode
```

You can now choose the interface (required) and specify if you want only MAC spoofing or both MAC and IP spoofing using **--ipspoof** parameter:

```bash
$ sudo python3 pySpot.py --iface wlan0 --verbose

[x] Current network information
 -  Interface: wlan0
 -  SSID: ORHUS Wi-Fi
 -  IP Address: 10.XX.20.106
 -  Broadcast IP: 10.XX.20.255
 -  Netmask (CIDR): 255.255.255.0 (/24)
 -  Physical Address: f4:XX:88:XX:5c:XX

[x] Identify appropriate subnet
  -  Scanning 10.XX.20.106/24...

[x] Network information theft
 - Trying to hijack 00:XX:DB:XX:10:XX
 - Trying to hijack 80:XX:55:XX:43:XX
 - Trying to hijack 3C:XX:30:XX:10:XX

[!] Internet is now reachable!!
 New IP: 10.XX.20.96
 New MAC: 3C:XX:30:XX:10:XX
```


## Author

Régis SENET ([rsenet](https://github.com/rsenet))


## Contributing

Bug reports and pull requests are welcome on [GitHub](https://github.com/rsenet/pySpot).

## License

The project is available as open source under the terms of the [GPLv3](https://www.gnu.org/licenses/quick-guide-gplv3.en.html)
