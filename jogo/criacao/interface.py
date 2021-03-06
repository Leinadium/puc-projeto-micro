import tkinter as tk
import os
from datetime import datetime, timedelta
from pynput import keyboard
import pygame
def main_criar():
    global inicio_musica
    global arq
    global listaNotas
    global agora_pause
    global intervalo_pause
    global bateria
    global lista_audios

    listaNotas = []

    intervalo_pause = 0

    pygame.mixer.init()

    pasta_atual = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'musicas')
    lista_audios = []

    janela = tk.Tk()
    janela.title("Criacao de Musica")
    janela.geometry("600x350")

    etiqueta_titulo = tk.Label(janela, text = "**Menu de criacao de musicas**")
    etiqueta_titulo.place(x=10,y=10)

    etiqueta_nome = tk.Label(janela, text="Nome:")
    etiqueta_nome.place(x=15,y=40)

    etiqueta_musicas_bat = tk.Label(janela, text = "BPM")
    etiqueta_musicas_bat.place(x=170, y=40)

    nome = tk.StringVar()
    campo_nome = tk.Entry(janela, width = 13, textvariable = nome)
    campo_nome.place(x=16, y = 60)

    bpm = tk.IntVar()  
    campo_bpm = tk.Spinbox(janela, width=6, textvariable=bpm, from_=40, to=230)
    campo_bpm.place(x=171, y=60)


    #possibilidade de tocar musica
    for arquivo in os.listdir(pasta_atual):
        if arquivo.endswith(".mp3"):
            lista_audios.append(arquivo.rstrip('.mp3'))

    def pausa():
        pygame.mixer.music.pause()

    def despausa():
        pygame.mixer.music.unpause()

    def restarta_musica():
        pygame.mixer.music.rewind()
            
    def toca_musica(option):
        nome_arq = option + ".mp3"
        print(nome_arq)
        pygame.mixer.music.load('../musicas/' + nome_arq)
        pygame.mixer.music.play()
        botao_pause = tk.Button(janela, text = '⏸️', command = pausa)
        botao_pause.place(x = 350, y = 90)
        botao_pause = tk.Button(janela, text = '▶️', command = despausa)
        botao_pause.place(x = 380, y = 90)
        botao_restart = tk.Button(janela, text = '⏹️', command = restarta_musica)
        botao_restart.place(x = 410, y = 90)
        

    etiqueta_audio = tk.Label(janela, text = "Escute a musica:")
    etiqueta_audio.place(x=350, y = 35)
    audio = tk.StringVar()
    audio.set(lista_audios[0])
    campo_audios = tk.OptionMenu(janela,audio,*lista_audios, command = toca_musica)
    campo_audios.config(width = 16)
    campo_audios.place(x = 351, y = 55)

    def vermelho_Aperta(evento):
        global inicio_musica
        global listaNotas
        intervalo = datetime.now() - inicio_musica
        intervalo_bom = (intervalo.total_seconds() * 1000) - intervalo_pause
        listaNotas.append(["vermelho",intervalo_bom])
        return
    def vermelho_Solta(evento):
        global inicio_musica
        global listaNotas
        intervalo = datetime.now() - inicio_musica
        intervalo_bom = (intervalo.total_seconds() * 1000) - intervalo_pause
        listaNotas.append(["vermelho",intervalo_bom])
        return
    def verde_Aperta(evento):
        global inicio_musica
        global listaNotas
        intervalo = datetime.now() - inicio_musica
        intervalo_bom = (intervalo.total_seconds() * 1000) - intervalo_pause
        listaNotas.append(["verde",intervalo_bom])
        return
    def verde_Solta(evento):
        global inicio_musica
        global listaNotas
        intervalo = datetime.now() - inicio_musica
        intervalo_bom = (intervalo.total_seconds() * 1000) - intervalo_pause
        listaNotas.append(["verde",intervalo_bom])
    def azul_Aperta(evento):
        intervalo = datetime.now() - inicio_musica
        intervalo_bom = (intervalo.total_seconds() * 1000) - intervalo_pause
        listaNotas.append(["azul",intervalo_bom])
        return
    def azul_Solta(evento):
        intervalo = datetime.now() - inicio_musica
        intervalo_bom = (intervalo.total_seconds() * 1000) - intervalo_pause
        listaNotas.append(["azul",intervalo_bom])
        return
    def amarelo_Aperta(evento):
        global inicio_musica
        global listaNotas
        intervalo = datetime.now() - inicio_musica
        intervalo_bom = (intervalo.total_seconds() * 1000) - intervalo_pause
        listaNotas.append(["amarelo",intervalo_bom])
        return
    def amarelo_Solta(evento):
        global inicio_musica
        global listaNotas
        intervalo = datetime.now() - inicio_musica
        intervalo_bom = (intervalo.total_seconds() * 1000) - intervalo_pause
        listaNotas.append(["amarelo",intervalo_bom])
        return
    def laranja_Aperta(evento):
        global inicio_musica
        global listaNotas
        intervalo = datetime.now() - inicio_musica
        intervalo_bom = (intervalo.total_seconds() * 1000) - intervalo_pause
        listaNotas.append(["laranja",intervalo_bom])
        return
    def laranja_Solta(evento):
        global inicio_musica
        global listaNotas
        intervalo = datetime.now() - inicio_musica
        intervalo_bom = (intervalo.total_seconds() * 1000) - intervalo_pause
        listaNotas.append(["laranja",intervalo_bom])
        return

    def enviarMusica():
        global arq
        i = 0
        while i < len(listaNotas)-1 :
            nota = listaNotas[i]
            if nota[0] == listaNotas[i+1][0]:
                intervalo = listaNotas[i+1][1] - nota[1]
                if intervalo >=  220:
                    linha = str(nota[0]) + ',' + str(nota[1]) + ',' + str(intervalo) + '\n'
                    arq.write(linha)
                    i += 1
                else:
                    linha = str(nota[0]) + ',' + str(nota[1]) + '\n'
                    arq.write(linha)
            i = i + 1
        
        arq.close()
        return

    def criaRet(cor):
        etiqueta = tk.Label(janela, text = '     ', bg = cor)
        etiqueta. place(x = 255, y = 200)


    def retoma_grav():
        global agora_pause
        global intervalo_pause
        pygame.mixer.music.unpause()
        agora_play = datetime.now()
        intervalo = agora_play - agora_pause
        intervalo_pause = intervalo.total_seconds() * 1000

    def reproduzGuitarra():
        global listaNotas
        global agora_pause
        pygame.mixer.music.pause()
        agora_pause = datetime.now()
        botaoResume = tk.Button(janela, text = "Voltar a gravar", command = retoma_grav)
        botaoResume.place(x=350, y = 210)
        if listaNotas == []:
            etiquet = tk.Label(janela, text = "Nao ha notas gravadas")
            etiquet.place(x=350, y = 235)
        i = 0
        while i < len(listaNotas)-1 :
            nota = listaNotas[i]
            print(nota)
            if nota[0] == 'vermelho' and listaNotas[i+1][0] == 'vermelho' :
                janela.after(int(nota[1]),criaRet, "#ff0000")
                janela.after(int(listaNotas[i+1][1]), criaRet, "#ECEBEA")
            elif nota[0] == 'verde' and listaNotas[i+1][0] == 'verde':
                janela.after(int(nota[1]),criaRet,'#00ff00')
                janela.after(int(listaNotas[i+1][1]), criaRet, "#ECEBEA")
            elif nota[0] == 'azul' and listaNotas[i+1][0] == 'azul':
                janela.after(int(nota[1]),criaRet,'#0000ff')
                janela.after(int(listaNotas[i+1][1]), criaRet, "#ECEBEA")
            elif nota[0] == 'amarelo' and listaNotas[i+1][0] == 'amarelo':
                janela.after(int(nota[1]),criaRet,'#FAE80B')
                janela.after(int(listaNotas[i+1][1]), criaRet, "#ECEBEA")
            elif nota[0] == 'laranja' and listaNotas[i+1][0] == 'laranja':
                janela.after(int(nota[1]),criaRet,'#ffa500')
                janela.after(int(listaNotas[i+1][1]), criaRet, "#ECEBEA")
            i += 1
        return

    def reproduzBat():
        global listaNotas
        global agora_pause
        pygame.mixer.music.pause()
        agora_pause = datetime.now()
        botaoResume = tk.Button(janela, text = "Voltar a gravar", command = retoma_grav)
        botaoResume.place(x=350, y = 210)
        if listaNotas == []:
            etiquet = tk.Label(janela, text = "Nao ha notas gravadas")
            etiquet.place(x=350, y = 235)
        i = 0
        while listaNotas != []:
            nota = listaNotas[i]
            if nota[0] == 'vermelho':
                janela.after(int(nota[1]),criaRet, "#ff0000")
                janela.after(int(nota[1]) + 150, criaRet, "#ECEBEA")
            elif nota[0] == 'verde':
                janela.after(int(nota[1]),criaRet,'#00ff00')
                janela.after(int(nota[1]) + 150, criaRet, "#ECEBEA")
            elif nota[0] == 'azul':
                janela.after(int(nota[1]),criaRet,'#0000ff')
                janela.after(int(nota[1]) + 150, criaRet, "#ECEBEA")
            elif nota[0] == 'amarelo':
                janela.after(int(nota[1]),criaRet,'#FAE80B')
                janela.after(int(nota[1]) + 150, criaRet, "#ECEBEA")
            elif nota[0] == 'laranja':
                janela.after(int(nota[1]),criaRet,'#ffa500')
                janela.after(int(nota[1]) + 150, criaRet, "#ECEBEA")
            i += 1


    def on_press(key):
        if key.char == 'q':
            vermelho_Aperta(None)
        elif key.char == 'w':
            verde_Aperta(None)
        elif key.char == 'e':
            azul_Aperta(None)
        elif key.char == 'r':
            amarelo_Aperta(None)
        elif key.char == 't':
            laranja_Aperta(None)
            
    #botao criar nova musica guitarra
    def criar_musica_guitarra():
        global arq
        global inicio_musica
        listener = keyboard.Listener(on_press=on_press)
        listener.start() 
        nomeGuit = nome.get()
        nomeGuitBom = nomeGuit.replace(" ", "_")
        nomeGuitFile = nomeGuitBom + '_guitarra.txt'
        arq = open(nomeGuitFile, 'w')
        inicio_musica = datetime.now()
        linha = str(bpm.get()) + '\n'
        arq.write(linha)
        if nomeGuitBom in lista_audios:
            nome_arq = nomeGuitBom + ".mp3"
            pygame.mixer.music.load('../musicas/' + nome_arq)
            pygame.mixer.music.play()
            labelMusica = tk.Label(janela, text = 'Musica encontrada, tocando agora!')
            labelMusica.place(x=180, y = 100)
        else:
            labelMusica = tk.Label(janela, text = 'Musica nao encontrada')
            labelMusica.place(x=180, y = 120)
        #cria os botoes
        botaoVerm = tk.Button(janela, text = '     ',bg = '#ff0000')
        botaoVerm.bind("<ButtonPress>", vermelho_Aperta)
        botaoVerm.bind("<ButtonRelease>", vermelho_Solta)
        botaoVerm.place(x = 220, y= 150)
        botaoVerd = tk.Button(janela, text = '     ', bg = '#00ff00')
        botaoVerd.bind("<ButtonPress>", verde_Aperta)
        botaoVerd.bind("<ButtonRelease>", verde_Solta)
        botaoVerd.place(x= 190, y = 150)
        botaoAzul = tk.Button(janela, text = '     ', bg = '#0000ff')
        botaoAzul.bind("<ButtonPress>", azul_Aperta)
        botaoAzul.bind("<ButtonRelease>", azul_Solta)
        botaoAzul.place(x=280, y = 150)
        botaoAm = tk.Button(janela, text = '     ', bg = '#FAE80B')
        botaoAm.bind("<ButtonPress>", amarelo_Aperta)
        botaoAm.bind("<ButtonRelease>", amarelo_Solta)
        botaoAm.place(x=250, y = 150)
        botaoLar = tk.Button(janela, text = '     ', bg = '#ffa500')
        botaoLar.bind("<ButtonPress>", laranja_Aperta)
        botaoLar.bind("<ButtonRelease>", laranja_Solta)
        botaoLar.place(x=310, y = 150)
        botaoEnd = tk.Button(janela, text = 'Concluir Gravacao', command = enviarMusica)
        botaoEnd.place(x= 370, y = 150)
        
        botaoOuvir = tk.Button(janela, text = "Reproduzir", command = reproduzGuitarra)
        botaoOuvir.place(x = 190, y = 185)
        
        
    botao1 = tk.Button(janela, text = "Criar musica na Guitarra", command = criar_musica_guitarra)
    botao1.place(x = 15, y = 105)

    def enviarMusicaBat():
        global arq
        for nota in listaNotas:
            linha = str(nota[0]) + ',' + str(nota[1]) + '\n'
            arq.write(linha)
        arq.close()
        return

    #botao criar nova musica bateria
    def criar_musica_bateria():
        global arq
        global inicio_musica
        global bateria
        bateria = True
        listener = keyboard.Listener(on_press=on_press)
        listener.start()     
        nomeBat = nome.get()
        nomeBatBom = nomeBat.replace(" ", "_")
        nomeBatFile = nomeBatBom + '_bateria.txt'
        arq = open(nomeBatFile, 'w')
        inicio_musica = datetime.now()
        linha = str(bpm.get()) + '\n'
        arq.write(linha)
        nome_arq = nomeBat + ".mp3"
        if nomeBatBom in lista_audios:
            nome_arq = nomeBatBom + ".mp3"
            pygame.mixer.music.load('../musicas/' + nome_arq)
            pygame.mixer.music.play()
            labelMusica = tk.Label(janela, text = 'Musica encontrada')
            labelMusica.place(x=170, y = 135)
        else:
            labelMusica = tk.Label(janela, text = 'Musica nao encontrada')
            labelMusica.place(x=170, y = 135)
            
        botaoVerm = tk.Button(janela, text = '  W  ',bg = '#ff0000')
        botaoVerm.bind("<ButtonPress>", vermelho_Aperta)
        botaoVerm.place(x = 200, y= 160)
        botaoVerd = tk.Button(janela, text = '  Q  ', bg = '#00ff00')
        botaoVerd.bind("<ButtonPress>", verde_Aperta)
        botaoVerd.place(x= 170, y = 160)
        botaoAzul = tk.Button(janela, text = '  R  ', bg = '#0000ff')
        botaoAzul.bind("<ButtonPress>", azul_Aperta)
        botaoAzul.place(x=260, y = 160)
        botaoAm = tk.Button(janela, text = '  E  ', bg = '#FAE80B')
        botaoAm.bind("<ButtonPress>", amarelo_Aperta)
        botaoAm.place(x=230, y = 160)
        botaoLar = tk.Button(janela, text = '  T  ', bg = '#ffa500')
        botaoLar.bind("<ButtonPress>", laranja_Aperta)
        botaoLar.place(x=290, y = 160)
        botaoEnd = tk.Button(janela, text = 'Concluir Gravacao', command = enviarMusicaBat)
        botaoEnd.place(x= 350, y = 160)
        
        botaoOuvir = tk.Button(janela, text = "Reproduzir", command = reproduzBat)
        botaoOuvir.place(x = 170, y = 195)
            
        
    botao2 = tk.Button(janela, text = "Criar musica na Bateria", command = criar_musica_bateria)
    botao2.place(x = 15, y = 165)

    janela.mainloop()

    
if __name__ == "__main__":
    main_criar()
