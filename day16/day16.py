import sys
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Valve:
    name: str
    rate: float
    connections: List[str]
