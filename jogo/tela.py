import pygame
from random import randint

from .constants import *
from .models.sprites import Sprite, TipoSprite

from typing import List, Optional
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

    def desenha_nota(self,
                     cor: Cor,
                     posicao: float,
                     raio: Optional[float] = None,
                     transparente: bool = False,
                     cor_branca: Optional[bool] = False,
                     borda_inferior: bool = True,
                     borda_superior: bool = True,
                     ):
        """Desenha uma nota na tela

        Se raio for None, utiliza o tamanho do raio padrao
        Se cor_branca for True, o circulo será branco
        """
        # desenho da borda
        if raio is None:
            raio = self.RAIO_ACORDE

        if transparente:
            cor_rgba = MAPA_CORES[cor][0], MAPA_CORES[cor][1], MAPA_CORES[cor][2], 0.5
        else:
            cor_rgba = MAPA_CORES[cor if not cor_branca else Cor.BRANCO]

        # BORDA
        pygame.draw.circle(
            self._tela,                 # surface
            MAPA_CORES[Cor.PRETO],      # preto
            (
                MAPA_POSICOES[cor],     # x
                posicao                 # y
            ),
            raio + 3,        # raio da borda
            width=3,
            draw_top_left=borda_superior,
            draw_top_right=borda_superior,
            draw_bottom_left=borda_inferior,
            draw_bottom_right=borda_inferior
        )
        # NOTA
        pygame.draw.circle(
            self._tela,
            cor_rgba,
            (
                MAPA_POSICOES[cor],     # x
                posicao                 # y
            ),
            raio,     # raio da borda,
        )

    def desenha_nota_extendida(self,
                               cor: Cor,
                               posicao: float,
                               extensao: float,
                               ):
        """Desenha uma nota extendida na tela

        Extensão é o comprimento da extensao em pixels
        """
        posicao_deslocada = posicao - extensao

        # desenha um retangulo
        pygame.draw.rect(
            self._tela,
            MAPA_CORES[cor],
            (
                MAPA_POSICOES[cor] - self.RAIO_ACORDE,
                posicao_deslocada,
                self.RAIO_ACORDE * 2,
                extensao
            )
        )

        # desenha a borda
        pygame.draw.rect(
            self._tela,
            MAPA_CORES[cor.PRETO],
            (
                MAPA_POSICOES[cor] - self.RAIO_ACORDE - 3,
                posicao_deslocada - 3,
                (self.RAIO_ACORDE + 3) * 2,
                extensao + 3
            ),
            width=3
        )

        self.desenha_nota(cor, posicao, borda_inferior=True, borda_superior=True)
        self.desenha_nota(cor, posicao_deslocada, borda_inferior=False, borda_superior=True)

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
                cor_branca=inputs[cor],
                transparente=False
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
