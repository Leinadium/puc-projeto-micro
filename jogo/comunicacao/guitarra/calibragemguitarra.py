import tkinter
from tkinter import ttk
from serial.tools.list_ports import comports

from .listenerguitarra import ListenerGuitarra, NotaGuitarra
# para typing
from typing import List
from serial import Serial


NENHUM_SERIAL = 'Nenhuma detectada'


class Preview:
    PRE_MENSAGEM = 'Status: '
    NOT_CONNECTED = 'Não conectado'
    OFFLINE = "Offline"
    ONLINE = "Online"

    def __init__(self, label: ttk.Label, string_var: tkinter.StringVar):
        self._label = label
        self._string_var = string_var
        self._listener = ListenerGuitarra()
        self._listener.range = 0.5  # maximo
        self._listener.callback = lambda n: self._callback(n)
        self._callback_botao_final = None
        self._retorno = None

        self.string_var = self.NOT_CONNECTED

    @property
    def ready(self) -> bool:
        return self.string_var == self.ONLINE

    @property
    def string_var(self) -> str:
        return self._string_var.get().lstrip(self.PRE_MENSAGEM)

    @string_var.setter
    def string_var(self, value: str):
        if value == self.NOT_CONNECTED:
            self._label.config(foreground='grey')
        elif value == self.OFFLINE:
            self._label.config(foreground='red')
        else:
            self._label.config(foreground='green')

        self._string_var.set(f"{self.PRE_MENSAGEM}{value}")

    @property
    def port(self):
        return self._listener.input_port

    @port.setter
    def port(self, port: Serial):
        self._listener.stop()
        self._listener.input_port = port
        self._listener.start()
        self.string_var = self.OFFLINE

    def _callback(self, _nota: NotaGuitarra):
        """Comando executado pelo listener"""
        botao_final.state(['!disabled'])
        self.string_var = self.ONLINE
        self.retorno_calibragem = input_combo_var.get(), range_combo_var.get()

    @property
    def retorno_calibragem(self):
        return self._retorno

    @retorno_calibragem.setter
    def retorno_calibragem(self, value):
        self._retorno = value

    def close(self):
        self._listener.stop()


# base do tkinter
# deve ser feito antes de tudo
root = tkinter.Tk()
root.title("Calibragem da Guitarra")
root.grid_columnconfigure(0, minsize=400)

mainframe = ttk.Frame(root, padding='3 3 12 12')
mainframe.grid(column=0, row=0)


def trocar_input(_e):
    """Troca o input serial atual de acordo com o selecionado no combobox"""
    try:
        preview.port = Serial(
            port=input_combo_var.get(),
            baudrate=9600
        )
    except OSError:
        inputs_combo.selection_clear()


# combobox de selecao de inputs (usa as linhas 0 e 1 e 2 da coluna 0)
ttk.Label(mainframe, text="Escolha a porta serial").grid(
    column=0, row=0, pady=5
)
lista_inputs: List[str] = [x.device for x in comports()]
if not lista_inputs:
    lista_inputs = [NENHUM_SERIAL]

input_combo_var = tkinter.StringVar()

inputs_combo = ttk.Combobox(mainframe, textvariable=input_combo_var)
inputs_combo.grid(column=0, row=1, columnspan=1, pady=(0, 5))     # noqa
inputs_combo['values'] = lista_inputs
inputs_combo.state(['readonly'])
inputs_combo.bind("<<ComboboxSelected>>", trocar_input)


# preview
sv = tkinter.StringVar()
status_label = ttk.Label(mainframe, textvariable=sv)
status_label.grid(column=0, row=2, pady=(0, 10))
preview = Preview(status_label, sv)


# combobox de selecao de range (usa as linhas 3 e 4 da coluna 0)
ttk.Label(mainframe, text='Escolha o range de consideração').grid(
    column=0, row=3, pady=5
)
lista_ranges: List[str] = [str(x / 10) for x in range(1, 6)]
range_combo_var = tkinter.StringVar()

range_combo = ttk.Combobox(mainframe, textvariable=range_combo_var)
range_combo.grid(column=0, row=4, pady=(0, 20))      # noqa
range_combo['values'] = lista_ranges
range_combo.state(['readonly'])


botao_final = ttk.Button(
    mainframe,
    text="Finalizar",
    command=root.destroy
)
botao_final.grid(
    column=0, row=5
)

botao_final.state(['disabled'])


def calibrar_guitarra():
    root.mainloop()
    preview.close()
    return preview.retorno_calibragem


if __name__ == '__main__':
    print(
        calibrar_guitarra()
    )
