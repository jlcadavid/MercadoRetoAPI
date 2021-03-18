#!/usr/bin/env python3

# Parse, filter and lookup the published Amazon IP Ranges.
# Useful for creating Security Groups and other firewall rules.
# E.g. incoming only from CloudFront
#   or outgoing only to non-EC2 ranges in US-WEST-1 region

# Author: Michael Ludvig <mludvig@logix.net.nz>
# Modified by: José Luis Martínez Cadavid <jlcadavid@uninorte.edu.co>

# Original code: https://github.com/mludvig/aws-utils/blob/master/filter-ip-ranges

from httplib2 import Http

import json
import socket
import ipaddress


# Función de listado de prefijos encontrados en Amazon IP Ranges.
def list_prefixes(ipv4=True):
    if ipv4:
        address_family = socket.AF_INET
        prefixes_label = 'prefixes'
        ip_prefix_label = 'ip_prefix'
    else:
        address_family = socket.AF_INET6
        prefixes_label = 'ipv6_prefixes'
        ip_prefix_label = 'ipv6_prefix'

    pfx_dict = {}
    for prefix in ipranges[prefixes_label]:
        ip_prefix = prefix[ip_prefix_label]
        if ip_prefix not in pfx_dict:
            pfx_dict[ip_prefix] = {}
            pfx_dict[ip_prefix]['net'] = ip_prefix
            pfx_dict[ip_prefix]['rgn'] = prefix['region']
            pfx_dict[ip_prefix]['svc'] = [prefix['service']]
        else:
            pfx_dict[ip_prefix]['svc'].append(prefix['service'])

    pfx_vals = list(pfx_dict.values())
    pfx_vals = sorted(pfx_vals, key=lambda x: socket.inet_pton(
        address_family, x['net'].split('/')[0]))

    return pfx_vals


# Función de búsqueda de IPs según Amazon IP Ranges.
def ip_lookup(ipv4, *args):
    prefixes = []
    if ipv4:
        prefixes.extend(list_prefixes(ipv4=True))
    if not ipv4:
        prefixes.extend(list_prefixes(ipv4=False))

    ips = []
    for arg in args:
        ips.append(ipaddress.ip_network(arg))

    if ips:
        _pfx = []
        for ip in ips:
            for prefix in prefixes:
                net = ipaddress.ip_network(prefix['net'])
                if net.overlaps(ip):
                    _pfx.append(prefix)
        prefixes = _pfx

    result = f"{len(prefixes)} prefixes matching / {len(ipranges['prefixes'])} prefixes found"

    for prefix in prefixes:
        result += f" - ({prefix['net']} {prefix['rgn']} {' '.join(prefix['svc'])})"

    return result

# Obtención de versión más actual de Amazon IP Ranges.
try:
    resp, content = Http().request('https://ip-ranges.amazonaws.com/ip-ranges.json')
    if resp.status != 200:
        print("Unable to load %s - %d %s" %
              ('https://ip-ranges.amazonaws.com/ip-ranges.json', resp.status, resp.reason))
    content = content.decode('latin1')
    ipranges = json.loads(content)
except Exception as e:
    print("Unable to load %s - %s" %
          ('https://ip-ranges.amazonaws.com/ip-ranges.json', e))

if len(ipranges['prefixes']) + len(ipranges['ipv6_prefixes']) < 1:
    print("No prefixes found")
