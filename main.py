
if __name__ == "__main__":
    from jogo.core import Jogo
    from jogo.constants import Instrumento

    a = Jogo(
        None ,
        'C:\\Users\\Daniel\\PycharmProjects\\puc-projeto-micro\\jogo\\musicas\\Happy BirthdayBat.txt',
        'C:\\Users\\Daniel\\PycharmProjects\\puc-projeto-micro\\jogo\\musicas\\parabens.mp3'
    )
    a.loop()
