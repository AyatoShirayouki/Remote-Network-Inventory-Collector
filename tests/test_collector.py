# tests/test_collector.py

import pytest
from unittest.mock import patch, MagicMock
from network_inventory_collector.collector import collect_from_host

@patch('network_inventory_collector.collector.try_ssh_connection')
@patch('network_inventory_collector.collector.safe_exec')
def test_collect_from_host_success(mock_safe_exec, mock_ssh):
    mock_ssh.return_value = MagicMock()
    mock_safe_exec.side_effect = ["fake route output", "fake address output"]

    # Mock the parsers if needed — skip or use real ones
    with patch('network_inventory_collector.collector.parse_ip_route') as mock_parse_route:
        with patch('network_inventory_collector.collector.parse_ip_address') as mock_parse_addr:
            mock_parse_route.return_value = [{'raw': 'route'}]
            mock_parse_addr.return_value = [{'name': 'eth0', 'addresses': ['192.168.1.10']}]

            result = collect_from_host('fakehost', {'user': 'pass'})
            assert result['host'] == 'fakehost'
            assert len(result['routing_table']) == 1
            assert len(result['interfaces']) == 1
