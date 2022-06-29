from enum import Enum
from typing import Dict


class Cor(Enum):
    AZUL = 1
    VERMELHO = 2
    AMARELO = 3
    VERDE = 4
    LARANJA = 5
    PRETO = 6
    BRANCO = 7


class Instrumento(Enum):
    BATERIA = 1
    GUITARRA = 2


MAPA_CORES: Dict[Cor, tuple] = {
    Cor.AZUL: (42, 61, 229),
    Cor.VERMELHO: (193, 27, 27),
    Cor.AMARELO: (231, 196, 15),
    Cor.VERDE: (26, 153, 61),
    Cor.LARANJA: (231, 145, 17),
    Cor.PRETO: (0, 0, 0),
    Cor.BRANCO: (255, 255, 255)
}

MAPA_NOME_NOTAS: Dict[str, Cor] = {
    "nota4": Cor.AZUL,
    "nota2": Cor.VERMELHO,
    "nota3": Cor.AMARELO,
    "nota1": Cor.VERDE,
    "nota5": Cor.LARANJA
}

ORDEM_CORDAS: Dict[Cor, int] = {
    Cor.VERDE: 0,
    Cor.VERMELHO: 1,
    Cor.AMARELO: 2,
    Cor.AZUL: 3,
    Cor.LARANJA: 4
}

MAPA_POSICOES: Dict[Cor, float] = {
    Cor.VERDE: 276.07,
    Cor.VERMELHO: 320.24,
    Cor.AMARELO: 364.41,
    Cor.AZUL: 408.57,
    Cor.LARANJA: 452.74
}
