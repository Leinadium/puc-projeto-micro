from dataclasses import dataclass


@dataclass
class Nota:
    cor: str
    corda: int
    pos_y: float
    tempo_acorde: int
