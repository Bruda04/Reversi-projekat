from Reversi.Reversi import Reversi

if __name__ == "__main__":
    igra = Reversi(1).prikazTable()
    print(igra.isLegalanPotez(igra._tabla, 0, 0 , 1))