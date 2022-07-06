import tkinter
from tkinter import *
from tkinter.ttk import Combobox, Label
from os import listdir
from os.path import isfile, join

    
from ..core import Jogo
from ..constants import Instrumento
from PIL import ImageTk, Image


class Menu:
    _ALTURA = 380
    _LARGURA = 600
    _FONT = ('Helvetica', 18)


    def __init__(self):
        self._root: Tk
        self._frame: Frame
        self._musica_selecionada: str
        self._musicas_possiveis: StringVar
        self._instrumento_atual: StringVar
        self._combo: Combobox
        self._listbox: Listbox
        self._instrumento_selecionado: str
        self._path_selecionado: str
        self._pathmp3: str

    def _seleciona_musica(self):

        selecionada = self._listbox.curselection()
        instrumento_param = 0
        
        if self._instrumento_selecionado == "Guitarra":
            instrumento_param = Instrumento.GUITARRA
        elif self._instrumento_selecionado == "Bateria":
            instrumento_param = Instrumento.BATERIA
        else:
            instrumento_param = None
        
        if selecionada != tuple():
            self._musica_selecionada = self._listbox.get(selecionada)
            #pegar o path, ler a lista, fechar menu
            print(self._musica_selecionada)
            self._path_selecionado = f'../musicas/{self._musica_selecionada}.txt'
            print(self._path_selecionado)
            self._pathmp3 = f'./jogo/musicas/{self._musica_selecionada}.mp3'
            
            self._root.destroy()
            a = Jogo(
                instrumento_param,
                self._path_selecionado,
                self._pathmp3
            )
            
            a.loop()
            
        self.start()
    

            
            

    def _lista_musicas(self, instrumento: str):
        self._instrumento_selecionado = instrumento
        
        suffix = f"_{instrumento.lower()}.txt"
        if instrumento is not None:
            self._musicas_possiveis.set('\n'.join([
                f.rstrip(suffix) for f in listdir('./jogo/musicas')
                if isfile(join('./jogo/musicas', f)) and f.endswith(suffix)
            ]))
            
            print(self._musicas_possiveis.get())

    def _combo_callback(self, event=None):
        if event:
            self._lista_musicas(self._instrumento_atual.get())

    def _menu_selecao_instrumento(self):
        self._frame.destroy()
        frame = Frame(self._root, width=self._LARGURA, height=self._ALTURA, background='grey')
        frame.grid(row=0, column=0, sticky='NW')

        label = Label(frame, text="Escolha o seu instrumento e música", font=self._FONT, background='grey', foreground='black')
        label.place(relx=0.5, rely=0.1, anchor=CENTER)

        combo = Combobox(frame, state='readonly', width=30, font=16, textvariable=self._instrumento_atual)
        combo['values'] = ('Guitarra', 'Bateria', 'Teclado')
        combo.current(0)
        combo.bind("<<ComboboxSelected>>", self._combo_callback)
        combo.place(relx=0.5, rely=0.2, anchor=CENTER)

        self._combo = combo

        list_box = Listbox(frame, selectmode="single", width=60)
        list_box.grid(row=0, column=0, sticky="nwes")
        list_box.place(relx=0.5, rely=0.5, anchor=CENTER)
        list_box['listvariable'] = self._musicas_possiveis
        self._listbox = list_box


        confirmar_button = Button(frame, width=20, text="Confirmar", command=self._seleciona_musica)
        confirmar_button.place(relx=0.5, rely=0.85, anchor=CENTER)


        self._frame = frame


    def start(self):
        """ inicia uma nova partida """
        self._root = Tk()
        self._root.geometry("%sx%s" %(self._LARGURA, self._ALTURA))
        self._root.title('Guitar Hero')
        self._root.resizable(False, False)
        self._root.configure(background='grey')

        self._musicas_possiveis = StringVar()
        self._instrumento_atual = StringVar()

        frame = Frame(self._root, background='grey')
        frame.pack(expand=True, fill=BOTH)
        
        canvas = Canvas(frame, width= 350, height=160, background='grey')
        canvas.place(x=130, y=30)
        
        
        img_raw = Image.open("./jogo/menu/GuitarHero.png")
        print(img_raw)
        img_resized = img_raw.resize((1844, 1256), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img_resized)
        canvas.create_image(20, 10, anchor=NW, image=img)

        # label = Label(frame,image=img, background='white')
        # label.place(x=-550, y=-200)


        iniciar_button = Button(frame, text="Iniciar", command=self._menu_selecao_instrumento, width=20)
        iniciar_button.place(x=self._LARGURA / 2 - 70, y=self._ALTURA * 5 / 7)


        criar_musica_button = Button(frame, text="Cria uma música", command=lambda : print('chama a interface'), width=20)
        criar_musica_button.place(x=self._LARGURA / 2 - 70, y=self._ALTURA * 5 / 7  + 40)


# nome da musica _instrumento.txt
#

        self._frame = frame
        self._root.mainloop()






if __name__ == "__main__":
    men = Menu()
    men.start()

