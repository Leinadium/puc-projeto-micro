# Trabalho de ENG1419 - Programação de Microcontroladores

Este trabalho é referente ao projeto final da disciplina de ENG1419 
(Programação de Microtroladores), do semestre 22.1 da PUC-Rio


Integrantes:

* [Daniel Guimarães](https://github.com/Leinadium)
* [Marcos Vinicius](https://github.com/MarcosViniciusAraujo)
* Joana da Matta
* Rogerio Pazetto

## Execução

Primeiro, crie um ambiente virtual e instale os requerimentos:

```
$ virtualenv -p python3 env
$ source env/bin/activate
$ pip install -r requirements.txt
```

Depois, execute o programa:

```
$ python main.py
```

## Funcionalidade

O projeto foi divido em diversas partes e integradas posteriormente:

* Comunicação com a guitarra
* Comunicação com a bateria
* Jogo do Guitar Hero
* Menu
* Criação da Música
* Código do Arduino da Guitarra

### Comunicação com a guitarra

A comunicação com a guitarra é por meio da interface Serial entre o python e o Arduino.
A guitarra envia o sinal atual da guitarra (posição da mão e estado do swing) constantemente, e o
python responde para o Arduino se houve algum erro ou acerto do jogador.

O código da interface da guitarra está disponível em `/jogo/comunicacao/guitarra/`.

### Comunicação com a bateria

A comunicação com a bateria é por meio de uma interface de comunicação MIDI. A bateria
envia uma nota MIDI ao ser tocada e o código processo esse sinal.

O código da interface da guitarra está disponível em `/jogo/comunicacao/bateria/`

### Jogo do Guitar Hero.

O jogo consiste de uma música sendo tocada e notas sincronizadas com a música para 
serem tocadas. As notas podem ser tocadas pela guitarra ou pela bateria, de acordo com o 
que foi pré-selecionado.

O código do jogo está disponível em `/jogo/` e subpastas

### Menu

O menu é a interface antes do jogo. Nela é possível selecionar a música, selecionar o instrumento,
ou escolher criar uma música nova. 

O código do menu está disponível em `/jogo/menu/menu.py`

### Criação da música

A criação é uma interface que permite escrever uma música nova para ser reproduzida no jogo.
É possível escrever uma música para ser tocada na bateria ou na guitarra, e criada por meio do mouse
ou por meio do teclado do computador.

O código do menu está disponível em `/jogo/criacao/interface.py`

### Código do arduino da guitarra

O Arduino é responsável por medir a posição da mão do jogador, assim como detectar quando este
pressionou o swing da guitarra.

O código do arduino está disponível em `/guitarra/main.c`