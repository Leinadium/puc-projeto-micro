import pygame
from pygame.locals import *
from sys import exit
from nota import Nota


pygame.init()

LARGURA = 720
ALTURA = 480


# CORES
LARANJA = (231, 145, 17)
AZUL = (42, 61, 229)
AMARELO = (231, 196, 15)
VERMELHO = (193, 27, 27)
VERDE = (26, 153, 61)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

map_cores = {
    "azul": AZUL,
    "vermelho": VERMELHO,
    "amarelo": AMARELO,
    "verde": VERDE,
    "laranja": LARANJA,
}


RAIO_ACORDE = 15
RAIO_ACORDE_MOVEL = 10
TAMANHO_LINHA_VERTICAL = 439

pos_cordas = [276.07, 320.24, 364.41, 408.57, 452.74]
pos_tempo = [0, 45, 90, 135, 180, 225, 270, 315, 360, 405, 450]

notas_tela = [Nota("verde", 0, 330, 0), Nota("vermelho", 1, 110, 0), Nota("verde", 0, 200, 0), Nota("laranja", 4, 150, 0)]

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Guitar hero 3.5")
tela.fill(BRANCO)
pygame.display.flip()


def desenha_acorde(cor, posX, posY):
    pygame.draw.circle(tela, PRETO, (posX, posY), RAIO_ACORDE + 3)
    pygame.draw.circle(tela, map_cores[cor], (posX, posY), RAIO_ACORDE)


def desenha_acorde_movel(cor, posX, posY):
    pygame.draw.circle(tela, PRETO, (posX, posY), RAIO_ACORDE_MOVEL + 3)
    pygame.draw.circle(tela, map_cores[cor], (posX, posY), RAIO_ACORDE_MOVEL)


def desenha_caminho_notas():
    # caminho
    s = pygame.Surface((229, 553))
    s.set_alpha(70)
    s.fill((160, 184, 231))
    tela.blit(s, (248, 0))


    # linhas verticais
    pygame.draw.line(tela, PRETO, (pos_cordas[0], 0), (pos_cordas[0], TAMANHO_LINHA_VERTICAL), width=3)
    pygame.draw.line(tela, PRETO, (pos_cordas[1], 0), (pos_cordas[1], TAMANHO_LINHA_VERTICAL), width=3)
    pygame.draw.line(tela, PRETO, (pos_cordas[2], 0), (pos_cordas[2], TAMANHO_LINHA_VERTICAL), width=3)
    pygame.draw.line(tela, PRETO, (pos_cordas[3], 0), (pos_cordas[3], TAMANHO_LINHA_VERTICAL), width=3)
    pygame.draw.line(tela, PRETO, (pos_cordas[4], 0), (pos_cordas[4], TAMANHO_LINHA_VERTICAL), width=3)


    # fim das notas
    desenha_acorde("verde", pos_cordas[0], 450)
    desenha_acorde("vermelho", pos_cordas[1], 450)
    desenha_acorde("amarelo", pos_cordas[2], 450)
    desenha_acorde("azul", pos_cordas[3], 450)
    desenha_acorde("laranja", pos_cordas[4], 450)


def desenha_pontuacao(pontos):
    # caixa dos pontos
    s = pygame.Surface((171, 105))
    s.set_alpha(89)
    s.fill((176, 176, 176))
    tela.blit(s, (38, 38))


    # texto dos pontos


def desenha_tela():
    tela.fill(BRANCO)
    desenha_caminho_notas()


def move_notas():
    for nota in notas_tela:
        nota.pos_y += 5

def exibe_notas():
    for nota in notas_tela:
        desenha_acorde_movel(nota.cor, pos_cordas[nota.corda], nota.pos_y)


def insere_nota_tela(nota):
    notas_tela.append(nota)


def remove_nota_tela(cor):

    maior_y = -1
    index_maior_y = -1

    for (i, nota) in enumerate(notas_tela):
        if cor == nota.cor:
            if nota.pos_y > maior_y:
                maior_y = nota.pos_y
                index_maior_y = i

    notas_tela.pop(index_maior_y)

def proximo_segundo():
    desenha_tela()
    move_notas()
    exibe_notas()

    pygame.display.flip()


# evento de loop
evento_usuario = pygame.event.custom_type()
pygame.time.set_timer(
    pygame.event.Event(
        evento_usuario
    ),
    millis=50,
    loops=0
)


run = True
while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
            pygame.quit()

        # detecta proximo decida
        if event.type == evento_usuario:
            proximo_segundo()
