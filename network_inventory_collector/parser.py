import re
from typing import List, Dict, Optional

def parse_ip_route(output: str) -> List[Dict]:
    lines = output.strip().splitlines()
    routes = []
    for line in lines:
        route = {"raw": line.strip()}
        if "default" in line:
            route["type"] = "default"
        routes.append(route)
    return routes

def parse_ip_address(output: str, filters: Optional[List[str]] = None) -> List[Dict]:
    interfaces = []
    current = {}
    for line in output.splitlines():
        line = line.strip()
        if re.match(r"^\d+: ", line):
            if current:
                interfaces.append(current)
            name = line.split(":")[1].strip().split("@")[0]
            if filters and not any(name.startswith(f) for f in filters):
                current = {}
                continue
            current = {"name": name, "addresses": []}
        elif "inet" in line or "inet6" in line:
            addr = line.split()[1]
            current.setdefault("addresses", []).append(addr)
    if current:
        interfaces.append(current)
    return interfaces
