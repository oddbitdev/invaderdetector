from collections import namedtuple
from dataclasses import dataclass
from typing import List


@dataclass
class Invader:
    name: str
    str_pattern: List[str]

    def __post_init__(self):
        self.pattern = self.str_pattern.split()
        self.width = len(self.pattern[0])
        self.height = len(self.pattern)

    def __repr__(self) -> str:
        return f"Invader {self.name}, width: {self.width}, height: {self.height}"


InvaderMatch = namedtuple("InvaderMatch", "name x y real_x real_y width height score")
