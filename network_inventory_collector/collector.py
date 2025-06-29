# collector.py

import logging
from typing import List, Optional
from network_inventory_collector.ssh_client import try_ssh_connection
from network_inventory_collector.parser import parse_ip_route, parse_ip_address
from network_inventory_collector.models import HostData
from network_inventory_collector.config import COMMANDS
from network_inventory_collector.utils import retry_with_backoff

@retry_with_backoff
def safe_exec(ssh, command: str) -> str:
    stdin, stdout, _ = ssh.exec_command(command)
    return stdout.read().decode()

def collect_from_host(host: str, credentials: dict, interface_filters: Optional[List[str]] = None) -> Optional[dict]:
    for username, password in credentials.items():
        ssh = try_ssh_connection(host, username, password)
        if not ssh:
            # Try key-based auth fallback
            ssh = try_ssh_connection(host, username, None)
        if ssh:
            try:
                route_output = safe_exec(ssh, COMMANDS["ROUTE"])
                address_output = safe_exec(ssh, COMMANDS["ADDRESS"])
                ssh.close()

                routing_table = parse_ip_route(route_output)
                interfaces = parse_ip_address(address_output, interface_filters)

                return HostData(
                    host=host,
                    routing_table=routing_table,
                    interfaces=interfaces
                ).to_dict()

            except Exception as e:
                logging.error(f"[{host}] Failed to retrieve data: {e}")
                return None

    logging.warning(f"[{host}] All credential attempts failed")
    return None
