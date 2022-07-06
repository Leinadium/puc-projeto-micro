from serial import Serial
from threading import Lock, Thread
from dataclasses import dataclass
from ..base import ListenerBase
from ..notificacao import Notificacao

from typing import Optional, List, Callable

__all__ = ['NotaGuitarra', 'ListenerGuitarra']


@dataclass
class NotaGuitarra:
    codigo: float
    on: bool


class ListenerGuitarra(ListenerBase):
    """Classe para ficar recebendo comandos da guitarra

    Possui duas propriedades e dois métodos principais:

        * input_port e callback
        * start() e stop()

    Possui uma propriedade especial:

        * range
    """
    def __init__(self):
        self._input_port: Optional[Serial] = None
        self._callbacks: List[Callable] = list()
        self._lock: Lock = Lock()
        self._range: float = 0.5
        # para a thread
        self._running: bool = False
        self._thread: Optional[Thread] = None
        # para o buffer
        self._nota_buffer: Optional[NotaGuitarra] = None
        # para o buffer de notificacoes
        self._notificacao_lock: Lock = Lock()
        self._notificacao_buffer: List[Notificacao] = list()

    @property
    def range(self):
        return self._range

    @range.setter
    def range(self, value):
        if isinstance(value, float):
            if value > 0.5:
                self._range = 0.5
            elif value < 0:
                self._range = 0
            else:
                self._range = value

    @property
    def input_port(self) -> Serial:
        return self._input_port

    @input_port.setter
    def input_port(self, port: Serial):
        """Configura a porta para receber os comandos do Serial.

        Levanta serial.SerialException caso a porta esteja inválida

        :param port: Porta Serial
        """

        if not port.is_open:
            port.open()     # levanta excecao caso a porta nao exista

        with self._lock:
            if self._input_port is not None:
                self._input_port.close()    # fecha a anterior
            self._input_port = port

        print(f"porta {port.name} configurada")
        return

    @property
    def callback(self):
        return self._callbacks

    @callback.setter
    def callback(self, func: Callable[[NotaGuitarra], None]):
        """Registra um callback para enviar a nota pressionada

        :param func: Função cujo parâmetro sera a `NotaGuitarra` pressionada
        """
        with self._lock:
            self._callbacks.append(func)

    def stop(self):
        """Para a captura da porta"""
        with self._lock:
            if self._running:
                self._running = False
                self._thread.join()
                self._thread = None

    def append_notification(self, notificacao: Notificacao):
        """Adiciona uma notificação para ser enviada após a próxima
        mensagem recebida pela porta."""
        with self._notificacao_lock:
            self._notificacao_buffer.append(notificacao)

    def _parse_notifications(self):
        """Envia as notificacoes pela porta"""
        with self._notificacao_lock:
            for nf in self._notificacao_buffer:
                texto = f"{'1' if nf.valor else '0'};{6 - nf.nota}\n"
                self._input_port.write(texto.encode())
                print(f"[LISTENER] enviado texto: {texto}")
            # limpa o buffer
            self._notificacao_buffer.clear()

    def _loop(self):
        """Faz o loop de escuta da porta"""
        while self._running and self._input_port.is_open:
            try:
                linha_bytes: bytes = self._input_port.readline()
            except AttributeError:
                break
            print("LI UMA LINHA -> ", linha_bytes)
            # decodificacao dos bytes
            try:
                linha: str = linha_bytes.decode()
            except UnicodeDecodeError:
                continue

            # decodificao do texto
            ret = NotaGuitarra(codigo=-1, on=False)
            linha_lista: List[str] = [x.strip() for x in linha.split(';')]
            if len(linha_lista) != 2:       # deve ter dois elementos
                continue
            identificador_raw: str = linha_lista[0]
            # verificando se é float
            try:
                ret.codigo = float(identificador_raw)
            except ValueError:
                continue

            if ret.codigo < 0:
                continue        # nenhuma nota

            pressionado_raw: str = linha_lista[1]
            if pressionado_raw not in ('1', '0'):   # deve ser um binario
                continue
            ret.on = pressionado_raw.startswith('1')

            # print(ret)

            # processando de acordo com o buffer
            if self._nota_buffer is not None:
                # verificando se esta no range e inverteu o sinal
                if abs(self._nota_buffer.codigo - ret.codigo) < self._range:
                    if self._nota_buffer.on != ret.on:
                        # envia a nota afinal
                        for c in self._callbacks:
                            c(ret)

                        self._nota_buffer = ret     # se eu troquei a nota
                    else:
                        pass                        # se a nota ta parecida
                else:
                    self._nota_buffer = ret         # se a nota foi longe
            else:
                self._nota_buffer = ret             # se era none

            # verificando notificacoes
            with self._notificacao_lock:
                verificar_buffer = len(self._notificacao_buffer) > 0

            # (fora do "with:" para liberar o lock)
            if verificar_buffer:
                self._parse_notifications()

        print("LISTENER: fechando loop")

    def start(self):
        """Inicia a captura da porta"""
        if not self._running and self._thread is None:
            self._running = True
            self._input_port.timeout = 5
            self._thread = Thread(target=self._loop)
            self._thread.start()
            print("Iniciando thread")

    @property
    def running(self):
        """Diz se a porta está sendo executada ou não"""
        return self._running

    def close(self):
        if self._input_port is not None and self._input_port.is_open:
            self._input_port.close()
