import mido
import tkinter
from tkinter import N, E, S, W
from tkinter import ttk

from .listenerbateria import ListenerBateria, NotaBateria

# para typing
from typing import Optional, List, Any
from mido.backends.rtmidi import Input


# base do tkinter
# deve ser feito antes de tudo
root = tkinter.Tk()
root.title("Calibragem da Bateria")


class Tabela:
    """Classe contendo os métodos para a manipulação da tabela"""

    nomes = ['Bumbo', 'Caixa', "Hi-Hat", "Tom", "Prato"]

    def __init__(self, tamanho: int = 5):
        # cria as StringVars para a tabela
        self._quantidade = tamanho
        self._string_vars = [tkinter.StringVar() for _ in range(tamanho)]
        self._notas: List[int] = list()
        self._listener: ListenerBateria = ListenerBateria()
        self._listener.register_callback(lambda n: self._callback(n))
        self._buffer: Any = None
        self._callback_botao_final = None

        # colocando os strings vars como "[ ]"
        for s in self._string_vars:
            s.set("[ ]")

    @property
    def finalizada(self) -> bool:
        return len(self._notas) == self._quantidade

    def get_nome(self, index: int):
        """Retorna o nome daquela linha da tabela"""
        return self.nomes[index]

    def get_string_var(self, index: int):
        """Retorna o StringVar para aquela linha da tabela"""
        return self._string_vars[index]

    def change_input_port(self, port: Input):
        """Troca a porta para ouvir"""
        self._listener.set_input_port(port)

    def _callback(self, nota: NotaBateria):
        """Comando executado pelo listener"""
        if isinstance(self._buffer, NotaBateria):
            # se a ultima nota foi a mesma,
            # AND se a atual foi um release,
            # AND a outra foi um pressionar
            if nota.codigo == self._buffer.codigo and not nota.on and self._buffer.on:
                if len(self._notas) < self._quantidade:  # se ainda tem espaco
                    self._notas.append(nota.codigo)  # adiciona a nota
                    # atualiza a string var (atualiza a tela)
                    self._string_vars[len(self._notas) - 1].set(f'[ {nota.codigo} ]')
                    # chamando callback para ligar botao final
                    if len(self._notas) == self._quantidade and self._callback_botao_final is not None:
                        self._callback_botao_final(True)

        self._buffer = nota  # adiciona a nota no buffer

    def remover_ultima_nota(self):
        """Remover a ultima nota da tabela"""
        if self._notas:
            self._notas.pop()
            self._string_vars[len(self._notas)].set('[ ]')
            # chamando callback
            if self._callback_botao_final is not None:
                self._callback_botao_final(False)

    def get_notas(self):
        """Pega a lista de notas com os ids das notas midi"""
        return self._notas

    def add_callback_pronto(self, callback):
        """Callback para o botao final

        Quando as 5 notas estiverem disponíveis, será executado callback(True)
        Em caso contrário, callback(False)
        """
        self._callback_botao_final = callback
        self._callback_botao_final(False)   # chama como False ja no inicio

    def fechar(self):
        self._listener.stop()


# funcionalidade principal da tela
tabela = Tabela(5)


# frame principal da tela
mainframe = ttk.Frame(root, padding='3 3 12 12')
mainframe.grid(column=0, row=0)

# root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)

# dropdown
lista_input_names: List[str] = mido.get_input_names()  # noqa
input_combo_var = tkinter.StringVar()
# http://tkdocs.com/tutorial/widgets.html#combobox
inputs_combo = ttk.Combobox(mainframe, textvariable=input_combo_var)
inputs_combo.grid(column=0, row=0, columnspan=5, sticky=[E, W])
inputs_combo['values'] = lista_input_names
inputs_combo.state(['readonly'])


def trocar_input(_e):
    """Troca o input midi atual de acordo com o selecionado no comboBox"""
    try:
        tabela.change_input_port(
            mido.open_input(input_combo_var.get())  # noqa
        )
    except OSError:
        inputs_combo.selection_clear()


inputs_combo.bind("<<ComboboxSelected>>", trocar_input)

# 5 sessoes
# | input | input | input | input | input |
# | bumbo | caixa | hihat |  tom  | prato |

for (indice, nome) in enumerate(tabela.nomes):
    novo_frame = ttk.Frame(mainframe, borderwidth=2, relief='solid', padding=(5, 10))
    novo_frame.grid(column=indice, row=1)

    # nome em cima
    tkinter.Label(novo_frame, text=nome, pady=5).grid(column=0, row=0)
    # input embaixo
    caixa = ttk.Label(novo_frame)
    caixa.grid(column=0, row=1)
    caixa['textvariable'] = tabela.get_string_var(indice)


for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

# botao de remover
ttk.Button(
    mainframe,
    text="Corrigir",
    command=tabela.remover_ultima_nota
).grid(
    column=1, row=2
)

botao_final = ttk.Button(
    mainframe,
    text="Finalizar",
    command=root.destroy
)
botao_final.grid(
    column=3, row=2
)

tabela.add_callback_pronto(
    lambda x: botao_final.state([f'{"!" if x else ""}disabled'])    # desliga ou liga o btao
)


def calibrar_bateria():
    root.mainloop()

    tabela.fechar()
    return tabela.get_notas() if tabela.get_notas() else None


if __name__ == "__main__":
    print(
        calibrar_bateria()
    )
