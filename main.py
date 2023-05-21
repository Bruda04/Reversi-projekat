from Reversi import Reversi as rvr

def instancaIgre():
    print("Boja")
    print("1. Crna")
    print("2. Bela")
    validanUnos = False
    while not validanUnos:
        unos = int(input("Odaberite zeljenu boju: "))
        if unos == 1 or unos == 2:
            validanUnos = True

    match(unos):
        case 1: igra = rvr.Reversi(1)
        case 2: igra = rvr.Reversi(-1)

    igra.igrajProtivBota()

trajeIgra = True
while trajeIgra:
    print("Menu")
    print()
    print("1. Igraj")
    print("2. Izlaz")
    validanUnos = False
    while not validanUnos:
        unos = int(input("Odaberite zeljenu boju: "))
        if unos == 1 or unos == 2:
            validanUnos = True
    match(unos):
        case 1: instancaIgre()
        case 2: trajeIgra = False

    
