from abc import ABC
from abc import abstractmethod

from .notificacao import Notificacao


class ListenerBase(ABC):
    """Classe base para as implementações do Listener"""

    @property
    @abstractmethod
    def input_port(self):
        pass

    @input_port.setter
    @abstractmethod
    def input_port(self, value):
        pass

    @property
    @abstractmethod
    def callback(self):
        pass

    @callback.setter
    @abstractmethod
    def callback(self, value):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass


class InterfaceBase(ABC):
    """Classe base para as implementações da Interface"""

    def __init__(self):
        self._dicionario: dict = dict()

    def atribui_notas(self, **kwargs):
        """Recebe as notas para serem processadas

        Chame utilizando key=value, onde key será o nome da nota e
        value o valor da nota
        """
        self._dicionario.clear()
        for k, v in kwargs.items():
            self._dicionario[int(v)] = str(k)

    @abstractmethod
    def send_notification(self, notification: Notificacao):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

