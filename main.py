from Reversi import Reversi as rvr

def instancaIgreProtivBota():
    print()
    print("-"*50)
    print("Boja")
    print("-"*50)
    print("1. Crna")
    print("2. Bela")
    print("-"*50)
    print()
    validanUnos = False
    while not validanUnos:
        unos = int(input("Odaberite zeljenu boju: "))
        if unos == 1 or unos == 2:
            validanUnos = True

    match(unos):
        case 1: igra = rvr.Reversi(1)
        case 2: igra = rvr.Reversi(-1)

    igra.igrajProtivBota()

def instancaIgreProtivIgraca():
    print()
    print("-"*50)
    print("Boja")
    print("-"*50)
    print("1. Crna")
    print("2. Bela")
    print("-"*50)
    print()
    validanUnos = False
    while not validanUnos:
        unos = int(input("Odaberite zeljenu boju: "))
        if unos == 1 or unos == 2:
            validanUnos = True

    match(unos):
        case 1: igra = rvr.Reversi(1)
        case 2: igra = rvr.Reversi(-1)

    igra.igrajProtivIgraca()

trajeIgra = True
while trajeIgra:
    print()
    print("-"*50)
    print("Menu")
    print("-"*50)
    print("1. Igraj protiv bota")
    print("2. Igraj protiv igraca")
    print("3. Izlaz")
    print("-"*50)
    print()
    validanUnos = False
    while not validanUnos:
        unos = int(input("Odaberite zeljeni tip igre: "))
        if unos == 1 or unos == 2 or unos == 3:
            validanUnos = True
    match(unos):
        case 1: instancaIgreProtivBota()
        case 2: instancaIgreProtivIgraca()
        case 3: trajeIgra = False

    
