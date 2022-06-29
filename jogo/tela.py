import pygame

from .models.notas import NotaTela
from .constants import *


class Tela:
    COMPRIMENTO = 720
    ALTURA = 480
    ALTURA_ACORDE = 450
    RAIO_ACORDE = 10
    LIMITE_ADIANTADO = ALTURA_ACORDE - RAIO_ACORDE
    LIMITE_ATRASADO = ALTURA_ACORDE + RAIO_ACORDE
    ALTURA_NOTA = ALTURA_ACORDE / 9
    COMPRIMENTO_LINHA = 439

    def __init__(self):
        """Cria uma instância da tela"""
        self._tela = pygame.display.set_mode(
            (self.COMPRIMENTO, self.ALTURA)
        )
        pygame.display.set_caption("nome do jogo aqui")

        # superficie
        self.s = pygame.Surface((229, 553))
        self.s.set_alpha(70)
        self.s.fill((176, 176, 176))

    def desenha_nota(self, nota: NotaTela, raio=None):
        """Desenha uma nota na tela

        Se raio for None, utiliza o tamanho do raio padrao
        """
        # desenho da borda
        if raio is None:
            raio = self.RAIO_ACORDE

        pygame.draw.circle(
            self._tela,                 # surface
            MAPA_CORES[Cor.PRETO],      # preto
            (
                MAPA_POSICOES[nota.cor],    # x
                nota.posicao                # y
            ),
            raio + 3        # raio da borda
        )
        pygame.draw.circle(
            self._tela,
            MAPA_CORES[nota.cor],
            (
                MAPA_POSICOES[nota.cor],  # x
                nota.posicao  # y
            ),
            raio      # raio da borda
        )

    def desenha(self):
        # desenha cinza opaco
        self._tela.fill(MAPA_CORES[Cor.BRANCO])

        self._tela.blit(self.s, (248, 0))

        for cor, pos in MAPA_POSICOES.items():
            # desenha linhas
            pygame.draw.line(
                self._tela,
                MAPA_CORES[Cor.PRETO],
                (pos, 0),
                (pos, self.COMPRIMENTO_LINHA),
                width=3
            )

            # desenha os finais
            self.desenha_nota(
                NotaTela(cor, self.ALTURA_ACORDE, 0),
                raio=self.RAIO_ACORDE + 5
            )
