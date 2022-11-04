from dataclasses import dataclass, field
from app import db


@dataclass
class Group():
    maxNum: int = 0
    tries: int = 0
    gameState: bool = False
    members: list[int] = field(default_factory=list, repr=False)
