# module imports
from threading import Lock

# local imports
import pygame

from .tela import Tela
from .constants import *
from .models.notas import NotaTela, NotaArquivo
from .models.sprites import Sprite, TipoSprite
from .comunicacao.notaprocessada import NotaProcessada
from .comunicacao.notificacao import Notificacao


# typing imports
from typing import List, Optional
from .comunicacao.base import InterfaceBase


class Jogo:
    FPS = 25
    PONTUACAO_MINIMA = 5
    LIMITE_MULTIPLICADOR = 5
    MILLIS = 1 / FPS * 1000

    def __init__(self,
                 instrumento: Optional[Instrumento],
                 musica_notas: str,
                 musica_som: str
                 ):
        """Inicia uma instância do jogo

        Args:
            instrumento (Instrumento): tipo do instrumento escolhido
            musica_notas (str): path das notas da música escolhida
            musica_som (str): path do audio da música escolhida
        """
        pygame.init()

        self.musica = musica_notas
        self.bpm = -1   # vai ser atribuido pelo self._carregar_notas
        pygame.mixer.music.load(musica_som)

        self.tipo_instrumento = instrumento
        self.interface: Optional[InterfaceBase] = None
        self.tela: Optional[Tela] = Tela()

        if instrumento == Instrumento.BATERIA:
            self._iniciar_bateria()
        elif instrumento == Instrumento.GUITARRA:
            self._iniciar_guitarra()

        # lista das notas da musica
        self.notas = self._carregar_notas(musica_notas)
        self.lock = Lock()  # para evitar concorrencia
        self.running = False
        self.musica_tocando = False

        # mapa de que notas estão sendo tocadas atualmente
        self.inputs = {k: False for k in ORDEM_CORDAS.keys()}

        # pontuacao
        self.pontuacao: int = 0
        self.multiplicador: int = 0
        self.notas_seguidas: int = 0
        self.buffer_acerto: bool = False

    def _iniciar_bateria(self):
        """Faz as configurações relativas a bateria"""
        import mido
        from .comunicacao.bateria.calibragembateria import calibrar_bateria
        from .comunicacao.bateria.interfacebateria import InterfaceBateria
        try:
            id_notas, porta = calibrar_bateria()
        except TypeError:
            print("Erro ao calibrar bateria (return None)")
            return

        # inicializacao da interface
        self.interface = InterfaceBateria(
            midi_port=mido.open_input(porta),  # noqa
            callback=lambda nota: self._callback_interface(nota)
        )

        self.interface.atribui_notas(
            nota1=id_notas[0],
            nota2=id_notas[1],
            nota3=id_notas[2],
            nota4=id_notas[3],
            nota5=id_notas[4],
        )
        self.interface.start()

    def _iniciar_guitarra(self):
        """Faz as configurações relativas a guitarra"""
        from serial import Serial
        from .comunicacao.guitarra.calibragemguitarra import calibrar_guitarra
        from .comunicacao.guitarra.interfaceguitarra import InterfaceGuitarra
        porta, range_considerado = calibrar_guitarra()

        # inicializacao da interface
        self.interface = InterfaceGuitarra(
            serial_port=Serial(porta),
            callback=lambda nota: self._callback_interface(nota),
            rangen=range_considerado
        )
        self.interface.atribui_notas(
            nota1=5.0,
            nota2=4.0,
            nota3=3.0,
            nota4=2.0,
            nota5=1.0
        )
        self.interface.start()

    def _carregar_notas(self, path_musica: str) -> List[NotaTela]:
        """Carrega as notas a partir do arquivo"""
        notas_carregadas: List[NotaArquivo] = list()
        try:
            with open(path_musica, 'r') as f:
                self.bpm = float(f.readline().strip())
                for linha in f:
                    linha_lista = linha.strip().split(',')
                    cor = linha_lista[0]                        # cor da nota
                    tempo = float(linha_lista[1]) / 1000        # tempo da nota
                    duracao = float(linha_lista[2]) / 1000 if len(linha_lista) == 3 else 0     # duracao

                    if duracao < 0.200:
                        duracao = 0

                    notas_carregadas.append(NotaArquivo(cor, tempo, duracao))

        except Exception as e:
            print(e)
            print("Carregando notas mockadas")
            notas_carregadas: List[NotaArquivo] = [
                NotaArquivo('verde', 0.2564 + 3, 0),
                NotaArquivo('vermelho', 0.2564 * 2 + 3, 0),
                NotaArquivo('verde', 0.2564 * 3 + 3, 0),
                NotaArquivo('vermelho', 0.2564 * 4 + 3, 0),
                NotaArquivo('verde', 0.2564 * 5 + 3, 0),
                NotaArquivo('vermelho', 0.2564 * 6 + 3, 0),
            ]

        return [
            NotaTela.from_nota_arquivo(
                nota=nota,
                comprimento_acorde=self.tela.ALTURA_ACORDE,
                comprimento_divisao=self.tela.ALTURA_NOTA,
                bpm=self.bpm
            ) for nota in notas_carregadas
        ]

    def _callback_interface(self, nota: NotaProcessada):
        # pegando o id da nota pelo nome
        try:
            cor_nota_tocada: Cor = MAPA_NOME_NOTAS[nota.nome]
        except ValueError:
            print("Nota invalida (valor invalido): ", nota)
            return

        # salva nos inputs
        self.inputs[cor_nota_tocada] = nota.on

        # altera o valor na lista
        try:
            nova_lista = list()
            for nota_lista in self.notas:
                pode_remover = False
                if cor_nota_tocada == nota_lista.cor:       # cor correta
                    # se a nota foi pressionada no tempo correto
                    if self.tela.LIMITE_ADIANTADO <= nota_lista.posicao <= self.tela.LIMITE_ATRASADO and nota.on:
                        self.parse_acerto(cor_nota_tocada)
                        pode_remover = nota_lista.extensao == 0     # so remove se nao tem extensao

                    # se passou do tempo, mas é uma nota extendida, verifica tbm
                    elif nota_lista.extensao > 0:
                        pos = nota_lista.posicao - nota_lista.extensao
                        if self.tela.LIMITE_ADIANTADO <= pos <= self.tela.LIMITE_ATRASADO and not nota.on:
                            self.parse_acerto(cor_nota_tocada)
                            pode_remover = True

                if not pode_remover:
                    nova_lista.append(nota_lista)

            self.notas = nova_lista

        except IndexError:
            print("Nota invalida (indice invalido): ", nota)

    def checa_eventos(self):
        """Checa os eventos do pygame"""
        if not pygame.mixer.music.get_busy() and self.musica_tocando:
            self.running = False
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # temporario: funcionamento pelo teclado
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self._callback_interface(NotaProcessada('nota1', event.type == pygame.KEYDOWN))
                if event.key == pygame.K_s:
                    self._callback_interface(NotaProcessada('nota2', event.type == pygame.KEYDOWN))
                if event.key == pygame.K_d:
                    self._callback_interface(NotaProcessada('nota3', event.type == pygame.KEYDOWN))
                if event.key == pygame.K_f:
                    self._callback_interface(NotaProcessada('nota4', event.type == pygame.KEYDOWN))
                if event.key == pygame.K_g:
                    self._callback_interface(NotaProcessada('nota5', event.type == pygame.KEYDOWN))

    def parse_acerto(self, cor: Cor):
        """Faz as operações relativas ao acerto de uma nota"""
        id_nota: int = ORDEM_CORDAS[cor] + 1
        # feedback pra guitarra
        if self.tipo_instrumento == Instrumento.GUITARRA:
            self.interface.send_notification(
                Notificacao(nota=id_nota, valor=True)
            )

        # multiplicador
        multiplicador_adicionado = False
        if self.notas_seguidas >= self.LIMITE_MULTIPLICADOR and self.multiplicador <= 3:
            multiplicador_adicionado = True
            self.multiplicador += 1
            self.notas_seguidas = 0
        else:
            self.notas_seguidas += 1

        # pontuacao
        ponto_ganho = int(self.PONTUACAO_MINIMA * self.multiplicador)
        self.pontuacao += ponto_ganho
        self.tela.adiciona_sprite(
            Sprite(
                tipo=TipoSprite.MULTIPLICADOR if multiplicador_adicionado else TipoSprite.ACERTO,
                valor=self.multiplicador if multiplicador_adicionado else ponto_ganho
            )
        )
        print(f"Acertou! [cor: {cor}]")
        return

    def parse_erro(self, cor: Cor):
        """Faz as operações relativas ao erro de uma nota"""
        id_nota: int = ORDEM_CORDAS[cor] + 1
        # feedback pra guitarra
        if self.tipo_instrumento == Instrumento.GUITARRA:
            self.interface.send_notification(
                Notificacao(nota=id_nota, valor=False)
            )
            pass

        self.notas_seguidas = 0
        self.multiplicador = 1

        self.tela.adiciona_sprite(
            Sprite(
                tipo=TipoSprite.ERRO,
                valor=None
            )
        )

        print(f"Errou! [cor: {cor}]")
        return

    def update(self):
        self.tela.desenha(
            inputs=self.inputs,
            pontuacao=self.pontuacao,
            multiplicador=self.multiplicador
        )

        # movendo as notas
        nova_lista: List[NotaTela] = list()

        with self.lock:
            for nota in self.notas:
                nota.posicao += self.MILLIS / 1000 * self.tela.ALTURA_NOTA * self.bpm / 60

                if nota.posicao - nota.extensao - self.tela.ALTURA_NOTA + 5 > self.tela.LIMITE_ATRASADO:
                    # ERROU
                    self.parse_erro(nota.cor)

                else:
                    if nota.extensao > 0:
                        self.tela.desenha_nota_extendida(nota.cor, nota.posicao, nota.extensao)
                    else:
                        self.tela.desenha_nota(nota.cor, nota.posicao)
                    nova_lista.append(nota)

        pygame.display.flip()
        self.notas = nova_lista

    def loop(self):
        clock = pygame.time.Clock()
        self.running = True
        self.multiplicador = 1
        pygame.mixer.music.play()

        while self.running:
            clock.tick(self.FPS)
            self.checa_eventos()
            self.update()

        if self.interface is not None:
            pygame.mixer.music.stop()
            self.interface.stop()

