from dataclasses import dataclass


@dataclass
class ProjectInfo:
    id: str
    name: str
    port: int
