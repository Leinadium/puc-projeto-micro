from jogo.main import main

print("bom dia")

if __name__ == "__main__":
    notas_verdade = [
        ('verde', 0.2564 + 3, 0),
        ('vermelho', 0.2564 * 2 + 3, 0),
        ('verde', 0.2564 * 3 + 3, 0),
        ('vermelho', 0.2564 * 4 + 3, 0),
        ('verde', 0.2564 * 5 + 3, 0),
        ('vermelho', 0.2564 * 6 + 3, 0),
    ]
    main(notas_verdade, using_guitarra=False)
