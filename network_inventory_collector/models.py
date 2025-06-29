# models.py
from dataclasses import dataclass, asdict
from typing import List, Dict

@dataclass
class HostData:
    host: str
    routing_table: List[Dict]
    interfaces: List[Dict]

    def to_dict(self):
        return asdict(self)
