# tests/test_ssh_client.py

import pytest
from unittest.mock import patch, MagicMock
from network_inventory_collector.ssh_client import try_ssh_connection

@patch('network_inventory_collector.ssh_client.paramiko.SSHClient')
def test_try_ssh_connection_success(mock_ssh):
    instance = mock_ssh.return_value
    instance.connect.return_value = True

    client = try_ssh_connection('fakehost', 'user', 'pass')
    assert client is not None
    instance.connect.assert_called_once()
