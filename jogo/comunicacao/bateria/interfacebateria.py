from .listenerbateria import ListenerBateria, NotaBateria
from ..base import InterfaceBase
from ..notaprocessada import NotaProcessada
from mido.backends.rtmidi import Input

from typing import Callable, Any

__all__ = ['InterfaceBateria']


class InterfaceBateria(InterfaceBase):
    def __init__(self, midi_port: Input, callback: Callable[[NotaProcessada], None]):
        """Inicializa a interface da bateria para o jogo

        Args:
            midi_port: Porta MIDI para ser utilizada
            callback: função para ser chamada ao receber uma nota valida
        """
        super().__init__()
        self._listener = ListenerBateria()
        self._porta = midi_port
        self._dicionario: dict = dict()
        self._callback_usuario = callback

    def _callback(self, nota: NotaBateria):
        """Faz o callback para o client"""
        if nota.codigo in self._dicionario:
            self._callback_usuario(
                NotaProcessada(
                    nome=self._dicionario[nota.codigo],
                    on=nota.on
                )
            )

    def send_notification(self, notification: Any):
        """Envia a notificacao pra bateria"""
        raise NotImplemented()

    def start(self):
        """Inicializa a captura de notas.

        Retorna imediatamente
        """
        self._listener.callback = lambda x: self._callback(x)
        self._listener.input_port = self._porta
        self._listener.start()

    def stop(self):
        """Para a captura de notas."""
        self._listener.stop()
