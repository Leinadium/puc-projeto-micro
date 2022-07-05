import pygame
from random import randint

from .constants import *
from .models.sprites import Sprite, TipoSprite

from typing import List
from pygame.surface import Surface


class Tela:
    COMPRIMENTO = 720
    ALTURA = 480
    ALTURA_ACORDE = 450
    RAIO_ACORDE = 10
    LIMITE_ADIANTADO = ALTURA_ACORDE - RAIO_ACORDE
    LIMITE_ATRASADO = ALTURA_ACORDE + RAIO_ACORDE
    ALTURA_NOTA = ALTURA_ACORDE / 9
    COMPRIMENTO_LINHA = 439
    X_SPRITE = 500
    SPEED_SPRITE = 2.0
    TTL_MAXIMO = 30

    def __init__(self):
        """Cria uma instância da tela"""
        self._tela = pygame.display.set_mode(
            (self.COMPRIMENTO, self.ALTURA)
        )
        pygame.display.set_caption("nome do jogo aqui")

        # superficie
        self.s: Surface = pygame.Surface((229, 553))
        self.s.set_alpha(70)
        self.s.fill((176, 176, 176))

        # sprites
        self.font = pygame.font.SysFont('Arial', 30, True)
        self.sprites: List[Sprite] = list()
        self.texto_erro: Surface = self.font.render('X', False, MAPA_CORES[Cor.VERMELHO])

    def desenha_nota(self, cor: Cor, posicao: float, raio=None, cor_branca=False):
        """Desenha uma nota na tela

        Se raio for None, utiliza o tamanho do raio padrao
        Se cor_branca for True, o circulo será branco
        """
        # desenho da borda
        if raio is None:
            raio = self.RAIO_ACORDE

        # borda
        pygame.draw.circle(
            self._tela,                 # surface
            MAPA_CORES[Cor.PRETO],      # preto
            (
                MAPA_POSICOES[cor],     # x
                posicao                 # y
            ),
            raio + 3,        # raio da borda
            width=3
        )
        pygame.draw.circle(
            self._tela,
            MAPA_CORES[cor if not cor_branca else Cor.BRANCO],
            (
                MAPA_POSICOES[cor],     # x
                posicao                 # y
            ),
            raio      # raio da borda
        )

    def adiciona_sprite(self, sp: Sprite):
        """Adiciona um sprite para ser desenhado"""
        sp.pos_y = self.ALTURA_ACORDE
        sp.pos_x = self.X_SPRITE + randint(-10, 10)
        sp.ttl = self.TTL_MAXIMO
        sp.alpha = 1
        self.sprites.append(sp)

    def desenha_sprites(self):
        """Desenha os sprites na tela"""

        pode_remover = False        # para saber se precisar remover o ultimo elemento da lista
        for sp in self.sprites:
            # move e atualiza
            sp.pos_y -= self.SPEED_SPRITE
            sp.ttl -= 1
            sp.alpha = sp.ttl / self.TTL_MAXIMO

            # marca pra remover
            pode_remover = sp.alpha <= 0 or pode_remover    # or -> mantem True

            # desenha:
            if sp.tipo == TipoSprite.ERRO:
                superficie = self.texto_erro
            elif sp.tipo == TipoSprite.ACERTO:
                superficie = self.font.render(f'+{sp.valor}', True, MAPA_CORES[Cor.VERDE])
            elif sp.tipo == TipoSprite.MULTIPLICADOR:
                superficie = self.font.render(f'x{sp.valor}', True, MAPA_CORES[Cor.AZUL])
            else:
                continue
            superficie.set_alpha(sp.alpha * 255)

            rect = superficie.get_rect()
            rect.x = sp.pos_x
            rect.y = sp.pos_y
            self._tela.blit(superficie, rect)

        if pode_remover:
            self.sprites.pop(0)

    def desenha(self, inputs: Dict[Cor, bool], pontuacao: int, multiplicador: int):
        """Desenha tudo na tela

        Inputs é os finais da linha
        """
        # enche a tela de branco
        self._tela.fill(MAPA_CORES[Cor.BRANCO])
        # desenha cinza opaco
        self._tela.blit(self.s, (248, 0))

        # desenha as linhas e os inputs
        for cor, pos in MAPA_POSICOES.items():
            if pos < -self.RAIO_ACORDE:     # pula notas que nao estão na tela
                continue
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
                cor,
                self.ALTURA_ACORDE,
                raio=self.RAIO_ACORDE + 5,
                cor_branca=inputs[cor]
            )

        self.desenha_sprites()

        # desenha a pontuacao
        self._tela.blit(
            self.font.render(f'{pontuacao} pts', False, MAPA_CORES[Cor.PRETO]),
            (20, 50)
        )
        self._tela.blit(
            self.font.render(f'x{multiplicador}', False, MAPA_CORES[Cor.AZUL]),
            (20, 90)
        )

