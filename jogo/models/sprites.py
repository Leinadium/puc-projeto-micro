from enum import Enum
from typing import Optional
from dataclasses import dataclass, field


class TipoSprite(Enum):
    """Enumerador contendo os possíveis tipos de sprite"""
    ERRO = 1
    ACERTO = 2
    MULTIPLICADOR = 3


@dataclass
class Sprite:
    """Representa um sprite na tela"""
    tipo: TipoSprite
    valor: Optional[int]
    pos_x: float = field(init=False)      # coordenada x
    pos_y: float = field(init=False)      # coordenada y
    alpha: int = field(init=False)      # transparencia da cor
    ttl: int = field(init=False)        # time to live

