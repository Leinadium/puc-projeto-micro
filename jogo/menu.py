from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter import Menu
from os import sep, path, isfile, join, listdir

class Menu:
    _ALTURA = 400
    _LARGURA = 600
    
    def __init__(self):
        self._root = None
        self._canvas = None
        self.musica_selecionada = None
    
    
    def _cria_lista_notas_verdade(self, ):
        
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
        
        iniciar_button = Button(root, text="Iniciar", command=lambda: self._menu_escolhe_instrumento(), width=20)
        fechar_button = Button(root, text="Fechar", command=lambda: self.fechar_menu(), width=20)
        
        
        iniciar_button.place(x=self._LARGURA / 2 - 70, y=self._ALTURA * 5 / 7)
        fechar_button.place(x=self._LARGURA / 2 - 70, y=self._ALTURA * 5 / 7 + 40)
        
        self._root = root
        root.mainloop()
    
    
    def fechar_menu(self):
        """ fecha a partida atual """
        self._root.destroy() 

    def _menu_escolhe_instrumento(self):
        
        self.fechar_menu()
        root = Tk()
        root.geometry("%sx%s" %(self._LARGURA, self._ALTURA))
        root.title('Escolha a musica')
        root.resizable(0, 0)
        root.configure(background='grey')
        
        canvas = Canvas(root, width=350, height=160, background='grey', highlightthickness=0)
        canvas.pack()
        
        combo = Combobox(root, width=15, state="readonly", font=('Arial', '12', 'bold'))
        confirmar_button = Button(root, text="Confirmar", command=lambda: self._escolhe_musica(combo.get()), width=20) 

        combo['values'] = ["Guitarra", "Bateria"]
        combo.current(0)
        
        combo.place(x=self._LARGURA / 2 - 85, y=self._ALTURA * 5 / 7 - 40)
        confirmar_button.place(x=self._LARGURA / 2 - 70, y=self._ALTURA * 5 / 7 + 40)
        
        self._root = root
    
    def _escolhe_musica(self, instrumento):
        
        self.fechar_menu()
        print(instrumento)
        root = Tk()
        root.geometry("%sx%s" %(self._LARGURA, self._ALTURA))
        root.title('Escolha a musica')
        root.resizable(0, 0)
        root.configure(background='grey')
        
        canvas = Canvas(root, width=350, height=160, background='grey', highlightthickness=0)
        canvas.pack()
        
        combo = Combobox(root, width=15, state="readonly", font=('Arial', '12', 'bold'))
        confirmar_button = Button(root, text="Confirmar", command=lambda: , width=20) 
        
    
        
        combo.place(x=self._LARGURA / 2 - 85, y=self._ALTURA * 5 / 7 - 40)
        confirmar_button.place(x=self._LARGURA / 2 - 70, y=self._ALTURA * 5 / 7 + 40)
        
        self._root = root
        
        
        


men = Menu()
men.start()
