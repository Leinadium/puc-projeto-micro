import pygame
from pygame.locals import *
from .nota import Nota
from .comunicacao.notaprocessada import NotaProcessada

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

ALTURA_ACORDE = 450

map_cores = {
    "azul": AZUL,
    "vermelho": VERMELHO,
    "amarelo": AMARELO,
    "verde": VERDE,
    "laranja": LARANJA,
}

map_nome_notas = {
    "bumbo": "azul",
    "caixa": "vermelho",
    "hihat": "amarelo",
    "tom": "verde",
    "prato": "laranja"
}

RAIO_ACORDE = 15
RAIO_ACORDE_MOVEL = 10
TAMANHO_LINHA_VERTICAL = 439

pos_cordas = [276.07, 320.24, 364.41, 408.57, 452.74]

pos_cordas_dict = {
    'verde': 0,
    'vermelho': 1,
    'amarelo': 2,
    'azul': 3,
    'laranja': 4
}

# notas_tela_antigo = [
#     Nota("verde", 0, 330, 0), Nota("vermelho", 1, 110, 0), Nota("verde", 0, 200, 0), Nota("laranja", 4, 150, 0)]


def calcula_altura_nota(tam_divisao, bpm, tempo):
    deslomento_em_funcao_da_base = tam_divisao * tempo * bpm / 60
    return ALTURA_ACORDE - deslomento_em_funcao_da_base


tela: pygame.Surface = None     # noqa


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
    desenha_acorde("verde", pos_cordas[0], ALTURA_ACORDE)
    desenha_acorde("vermelho", pos_cordas[1], ALTURA_ACORDE)
    desenha_acorde("amarelo", pos_cordas[2], ALTURA_ACORDE)
    desenha_acorde("azul", pos_cordas[3], ALTURA_ACORDE)
    desenha_acorde("laranja", pos_cordas[4], ALTURA_ACORDE)


def desenha_pontuacao(pontos):
    """Desenha a pontuação na tela

    Args:
        pontos (int): pontos do jogador
    """
    # caixa dos pontos
    s = pygame.Surface((171, 105))
    s.set_alpha(89)
    s.fill((176, 176, 176))
    tela.blit(s, (38, 38))

    # texto dos pontos


def desenha_tela():
    tela.fill(BRANCO)
    desenha_caminho_notas()

    return 1


def move_notas(notas_tela, millis, altura_nota, bpm):
    for nota in notas_tela:
        # nota.pos_y += 5
        nota.pos_y += millis / 1000 * altura_nota * bpm / 60

    return 1


def exibe_notas(notas_tela):
    for nota in notas_tela:
        desenha_acorde_movel(nota.cor, pos_cordas[nota.corda], nota.pos_y)

    return 1


def insere_nota_tela(notas_tela, nota):
    notas_tela.append(nota)
    return 1


def remove_nota_tocada(notas_tela, cor):
    y_max = -1
    index_y_max = -1

    for (i, nota) in enumerate(notas_tela):
        if cor == nota.cor:
            if 435 <= nota.pos_y <= 470:
                print("acertou")
                notas_tela.pop(i)
                return 1
            else:
                if nota.pos_y > y_max:
                    y_max = nota.pos_y
                    index_y_max = i

    if index_y_max != -1:
        print("errou")
        # notas_tela.pop(index_y_max)
        return 0


def remove_se_chegou_no_final(notas_tela):
    for (i, nota) in enumerate(notas_tela):
        if nota.pos_y > 480:
            print("errou")
            notas_tela.pop(i)

    return 1


def proximo_segundo(notas_tela, millis, altura_nota, bpm):
    desenha_tela()
    move_notas(notas_tela, millis, altura_nota, bpm)
    remove_se_chegou_no_final(notas_tela)
    exibe_notas(notas_tela)
    pygame.display.flip()


def main(notas_verdade, using_bateria=False, using_guitarra=False, musica=None):
    if using_guitarra:
        from .comunicacao.guitarra.calibragemguitarra import calibrar_guitarra
        from .comunicacao.guitarra.interfaceguitarra import InterfaceGuitarra
        from serial import Serial

        def callback(nota: NotaProcessada):
            print(f"Recebi nota {nota.nome} [{nota.on}]")
            remove_nota_tocada(notas_tela, nota.nome)

        porta, range_considerado = calibrar_guitarra()
        interface = InterfaceGuitarra(
            serial_port=Serial(porta),
            callback=callback,
            rangen=range_considerado
        )
        interface.atribui_notas(
            verde=1.0,
            vermelho=2.0,
            amarelo=3.0,
            azul=4.0,
            laranja=5.0
        )
        interface.start()
    elif using_bateria:
        from .comunicacao.bateria.calibragembateria import calibrar_bateria
        from .comunicacao.bateria.interfacebateria import InterfaceBateria
        import mido

        def callback(nota: NotaProcessada):
            print("Recebi nota ", nota.nome)
            remove_nota_tocada(notas_tela, map_nome_notas[nota.nome])

        id_notas = calibrar_bateria()
        interface = InterfaceBateria(
            midi_port=mido.open_input('Circuit 0'),  # noqa
            callback=callback
        )
        interface.atribui_notas(
            bumbo=id_notas[0],
            caixa=id_notas[1],
            hihat=id_notas[2],
            tom=id_notas[3],
            prato=id_notas[4]
        )
        interface.start()
    else:
        interface = None

    pygame.init()
    global tela
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Guitar hero 3.5")
    tela.fill(BRANCO)
    pygame.display.flip()

    FPS = 30
    MILLIS = 1 / FPS * 1000
    BPM = 116

    notas_tela = [
        Nota(
            cor,
            pos_cordas_dict[cor],
            calcula_altura_nota(ALTURA_ACORDE / 9, 117, tempo),
            duracao
        )
        for cor, tempo, duracao in notas_verdade
    ]

    altura_de_uma_nota = ALTURA_ACORDE / 9

    pygame.mixer.music.load('background.wav')
    pygame.mixer.music.play(0)

    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)

        if not pygame.mixer.music.get_busy():
            # musica acabou, o jogo acabou
            pass

        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
                pygame.quit()
                break

            if event.type == KEYDOWN:
                if event.key == pygame.K_a:
                    remove_nota_tocada(notas_tela, "verde")
                if event.key == pygame.K_s:
                    remove_nota_tocada(notas_tela, "vermelho")
                if event.key == pygame.K_d:
                    remove_nota_tocada(notas_tela, "amarelo")
                if event.key == pygame.K_f:
                    remove_nota_tocada(notas_tela, "azul")
                if event.key == pygame.K_g:
                    remove_nota_tocada(notas_tela, "laranja")

        if run:
            proximo_segundo(notas_tela, MILLIS, altura_de_uma_nota, bpm=BPM)

    if interface is not None:
        interface.stop()
