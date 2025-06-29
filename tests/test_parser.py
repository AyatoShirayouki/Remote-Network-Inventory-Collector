# tests/test_parser.py

import pytest
from network_inventory_collector.parser import parse_ip_route, parse_ip_address

def test_parse_ip_route_basic():
    output = """
    default via 192.168.1.1 dev eth0
    192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.10
    """
    result = parse_ip_route(output)
    assert len(result) == 2
    assert result[0]['type'] == 'default'
    assert result[0]['raw'].startswith('default via')

def test_parse_ip_address_basic():
    output = """
    2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500
        inet 192.168.1.10/24 brd 192.168.1.255 scope global eth0
        inet6 fe80::a00:27ff:fe4e:66a1/64 scope link
    """
    result = parse_ip_address(output)
    assert len(result) == 1
    assert result[0]['name'] == 'eth0'
    assert '192.168.1.10/24' in result[0]['addresses']
    assert any(addr.startswith('fe80::') for addr in result[0]['addresses'])
