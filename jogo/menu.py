from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter import Menu
from os import sep, path

class Menu:
    _ALTURA = 400
    _LARGURA = 600
    
    def __init__(self):
        self._root = None
        self._canvas = None
    
    
    # def _
    def start(self):
        """ inicia uma nova partida """
        root = Tk()
        root.geometry("%sx%s" %(self._LARGURA, self._ALTURA))
        root.title('Guitar Hero')
        root.resizable(0, 0)
        root.configure(background='grey')
        
        
        canvas = Canvas(root, width=350, height=160, background='grey', highlightthickness=0)
        canvas.pack()
        
        # imagem do jogo
        
        iniciar_button = Button(root, text="Iniciar", command=lambda: self._menu_escolhe_musica(), width=20)
        fechar_button = Button(root, text="Fechar", command=lambda: self.fechar_menu(), width=20)
        
        
        iniciar_button.place(x=self._LARGURA / 2 - 70, y=self._ALTURA * 5 / 7)
        fechar_button.place(x=self._LARGURA / 2 - 70, y=self._ALTURA * 5 / 7 + 40)
        
        self._root = root
        root.mainloop()
    
    
    def fechar_menu(self):
        """ fecha a partida atual """
        self._root.destroy() 
        exit(1)

    def _menu_escolhe_musica(self):
        root = Tk()
        


        


men = Menu()
men.start()