
if __name__ == "__main__":
    # notas_verdade = [
    #     ('verde', 0.2564 + 3, 0),
    #     ('vermelho', 0.2564 * 2 + 3, 0),
    #     ('verde', 0.2564 * 3 + 3, 0),
    #     ('vermelho', 0.2564 * 4 + 3, 0),
    #     ('verde', 0.2564 * 5 + 3, 0),
    #     ('vermelho', 0.2564 * 6 + 3, 0),
    # ]
    # main(notas_verdade, using_guitarra=False)
    from jogo.core import Jogo

    a = Jogo(
        None,
        'C:\\Users\\Daniel\\PycharmProjects\\puc-projeto-micro\\jogo\\musicas\\Happy BirthdayBat.txt',
        'C:\\Users\\Daniel\\PycharmProjects\\puc-projeto-micro\\jogo\\musicas\\parabens.mp3'
    )
    a.loop()
