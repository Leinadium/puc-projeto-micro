import mido
from threading import Lock
from dataclasses import dataclass

from typing import Optional, Callable, List
from mido.backends.rtmidi import Input

__all__ = ['Nota', 'Listener']


@dataclass
class Nota:
    codigo: int
    on: bool


class Listener:
    """Classe para ficar recebendo comandos MIDI.

    Possui três métodos principais:

        * set_input_port(port) -> configura a porta para ouvir
        * register_callback(func) -> callback para receber as notas
    """
    def __init__(self):
        self._input_port: Optional[Input] = None
        self._lock: Lock = Lock()
        self._callbacks: List[Callable] = list()

    def set_input_port(self, port: Input):
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
                    n = Nota(codigo=msg.note, on=not soltou)
                    # chamando os callbacks da lista com a nota
                    # print("nota pressionada: ", n)
                    for c in self._callbacks:
                        c(n)

    def register_callback(self, func: Callable[[Nota], None]):
        """Registra um callback para enviar a nota pressionada

        :param func: Função cujo parâmetro sera a `Nota` pressionada
        """
        with self._lock:
            self._callbacks.append(func)

    def stop(self):
        """Para a captura da porta"""
        with self._lock:
            self._input_port.close()
