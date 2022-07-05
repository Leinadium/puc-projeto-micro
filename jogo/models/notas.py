from dataclasses import dataclass
from ..constants import *


@dataclass
class NotaArquivo:
    cor: str        # cor da nota
    seg: float      # posicao na musica em segundos
    press: float    # tempo de pressionamento em segundos


class NotaTela:
    def __init__(self, cor: Cor, posicao: float, extensao: float):
        """Inicia uma nota da tela

        Atribui a cor, posicao e o tempo que a nota deve ficar pressionada
        """
        self.cor = cor
        self.posicao = posicao
        self.extensao = extensao
        self.corda = ORDEM_CORDAS[cor]

    def __repr__(self):
        return f'<NotaTela cor={self.cor} posicao={self.posicao} ex={self.extensao}>'

    @staticmethod
    def from_nota_arquivo(nota: NotaArquivo,
                          comprimento_acorde: float,
                          comprimento_divisao: float,
                          bpm: float,
                          ) -> "NotaTela":
        """Cria um NotaTela a partir de uma NotaArquivo

        Configura uma NotaTela a partir de informações do arquivo
        e do jogo

        Args:
            nota (NotaArquivo): nota do arquivo
            comprimento_acorde (float): comprimento de um acorde no jogo (8 beats)
            comprimento_divisao (float): comprimento de uma divisao (beats)
            bpm (float): beats por minuto no jogo
        """
        if nota.cor == 'verde':
            cor = Cor.VERDE
        elif nota.cor == 'vermelho':
            cor = Cor.VERMELHO
        elif nota.cor == 'azul':
            cor = Cor.AZUL
        elif nota.cor == 'amarelo':
            cor = Cor.AMARELO
        else:
            cor = Cor.LARANJA

        return NotaTela(
            cor=cor,
            posicao=comprimento_acorde - (comprimento_divisao * nota.seg * bpm / 60),
            extensao=comprimento_divisao * nota.press * bpm / 60
        )
