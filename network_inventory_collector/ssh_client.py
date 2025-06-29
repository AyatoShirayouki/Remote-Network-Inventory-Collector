# ssh_client.py

import paramiko
import socket
from typing import Optional
from network_inventory_collector.utils import retry_with_backoff
from network_inventory_collector.config import SSH_TIMEOUT

@retry_with_backoff
def try_ssh_connection(host: str, username: str, password: Optional[str]) -> Optional[paramiko.SSHClient]:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        if password:
            client.connect(
                hostname=host,
                username=username,
                password=password,
                timeout=SSH_TIMEOUT
            )
        else:
            # SSH key fallback
            client.connect(
                hostname=host,
                username=username,
                key_filename="~/.ssh/id_rsa",
                timeout=SSH_TIMEOUT,
                allow_agent=True,
                look_for_keys=True
            )
        return client

    except (paramiko.AuthenticationException, paramiko.SSHException, socket.error) as e:
        raise e
