from threading import Lock
from dataclasses import dataclass
from ..base import ListenerBase

from typing import Optional, Callable, List
from mido.backends.rtmidi import Input

__all__ = ['NotaBateria', 'ListenerBateria']


@dataclass
class NotaBateria:
    codigo: int
    on: bool


class ListenerBateria(ListenerBase):
    """Classe para ficar recebendo comandos MIDI.

    Possui duas propriedades e dois métodos principais:

        * input_port e callback
        * start() e stop()

    """
    def __init__(self):
        self._input_port: Optional[Input] = None
        self._lock: Lock = Lock()
        self._callbacks: List[Callable] = list()

    @property
    def input_port(self):
        return self._input_port

    @input_port.setter
    def input_port(self, port: Input):
        """Configura a porta para receber comandos MIDI

        :param port: Porta MIDI
        """
        with self._lock:
            if self._input_port is not None:    # fecha a porta anterior
                self._input_port.close()
            self._input_port = port             # adiciona a nova porta
            # adiciona o callback an porta
            self._input_port.callback = lambda msg: self._real_callback(msg)

        print(f"porta {port} configurada")

    def _real_callback(self, msg):
        """Callback que sera executado pelo Input

        Trata a mensagem, e envia para os callbacks registrados
        """
        if hasattr(msg, 'type') and hasattr(msg, 'note') and hasattr(msg, 'velocity'):
            if msg.type == 'note_on' or msg.type == 'note_off':
                soltou = msg.type == 'note_off' or msg.velocity == 0
                if hasattr(msg, 'note'):
                    n = NotaBateria(codigo=msg.note, on=not soltou)
                    # chamando os callbacks da lista com a nota
                    # print("nota pressionada: ", n)
                    for c in self._callbacks:
                        c(n)

    @property
    def callback(self):
        return self._callbacks

    @callback.setter
    def callback(self, func: Callable[[NotaBateria], None]):
        """Registra um callback para enviar a nota pressionada.

        OBS: NÃO SOBREESCREVE O ANTERIOR

        :param func: Função cujo parâmetro sera a `Nota` pressionada
        """
        with self._lock:
            self._callbacks.append(func)

    def stop(self):
        """Para a captura da porta"""
        with self._lock:
            self._input_port.close()

    def start(self):
        """Inicia a captura da porta"""
        # a captura é iniciada ao registrar o input_port
        pass