from .listener import Listener, Nota
from mido.backends.rtmidi import Input
from dataclasses import dataclass

from typing import Callable

__all__ = ['NotaProcessada', 'Interface']


@dataclass
class NotaProcessada:
    nome: str
    on: bool


class Interface:
    def __init__(self, midi_port: Input, callback: Callable[[NotaProcessada], None]):
        """Inicializa a interface da bateria para o jogo

        Args:
            midi_port: Porta MIDI para ser utilizada
            callback: função para ser chamada ao receber uma nota valida
        """
        self._listener = Listener()
        self._porta = midi_port
        self._dicionario: dict = dict()
        self._callback_usuario = callback

    def atribui_notas(self, **kwargs):
        """Recebe as notas MIDIs para serem processadas

        Chame utilizando key=value, onde key será o nome da nota
        e value o valor da nota
        """
        self._dicionario.clear()
        for k, v in kwargs.items():
            self._dicionario[int(v)] = str(k)

    def _callback(self, nota: Nota):
        """Faz o callback para o client"""
        if nota.codigo in self._dicionario:
            self._callback_usuario(
                NotaProcessada(
                    nome=self._dicionario[nota.codigo],
                    on=nota.on
                )
            )

    def start(self):
        """Inicializa a captura de notas.

        Retorna imediatamente
        """
        self._listener.register_callback(lambda x: self._callback(x))
        self._listener.set_input_port(self._porta)

    def stop(self):
        """Para a captura de notas."""
        self._listener.stop()


if __name__ == "__main__":
    # o código abaixo retorna erro pois não há dispositivo midi com o nome.
    # o código existe somente para exemplo
    import mido
    from time import sleep

    def cb(nota: NotaProcessada):
        print(nota)

    from calibragem import calibrar
    notas = calibrar()

    interface = Interface(
        midi_port=mido.open_input('Circuit 0'),  # noqa
        callback=cb
    )

    interface.atribui_notas(
        kick=notas[0],
        caixa=notas[1],
        hihat=notas[2],
        tom=notas[3],
        prato=notas[4]
    )

    interface.start()
    sleep(20)
    interface.stop()
