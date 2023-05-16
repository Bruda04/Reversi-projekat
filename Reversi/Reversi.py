from Heuristics.Heuristika import calculateHeuristics

class Reversi(object):
    def __init__(self, player):
        if player == 1: #igrac je crni
            self._igrac = 1
            self._bot = -1
        elif player == -1: #igrac je beli
            self._igrac = -1
            self._bot = 1

        self._igracPoteza = 0
        self._botPoteza = 0

        self._igracScore = 2
        self._botScore = 2

        self._isKraj = False

        self._tabla = [ 
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, 1, -1, None, None, None],    #None = prazno, 1 = Black, -1 = White
                [None, None, None, -1, 1, -1, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                ]
        self._tablaMogucihPoteza = [
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, -1, 1, None, None, None],
                [None, None, -1, None, None, 1, None, None],
                [None, None, 1, None, None, -1, None, None],    #None = prazno, 1 = Black, -1 = White
                [None, None, None, 1, -1, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                ]
        
    
    def prikazTable(self):
        print(f"Igrac: {self._igracScore}")
        print(f"Bot: {self._botScore}")
        print ("{:^7} {:^7} {:^7} {:^7} {:^7} {:^7} {:^7} {:^7} {:^7}".format('', 'A','B','C','D','E','F','G','H'))
        redniBroj = 1
        for i in range(8):
            kolona = self._tabla[i]
            prntCol = []
            for j in range(8):
                polje = kolona[j]
                match(polje):
                    case None: prntCol.append("\u2b1a")
                    case 1: prntCol.append("B")
                    case -1: prntCol.append("W")
                if (self._tablaMogucihPoteza[i][j] == self._igrac):
                    prntCol[j] = "X"
                    
            print()
            print ("{:^7} {:^7} {:^7} {:^7} {:^7} {:^7} {:^7} {:^7} {:^7} {:^7}".format(redniBroj, prntCol[0], prntCol[1], prntCol[2], prntCol[3], prntCol[4], prntCol[5], prntCol[6], prntCol[7], redniBroj))
            redniBroj += 1
        print ("\n{:^7} {:^7} {:^7} {:^7} {:^7} {:^7} {:^7} {:^7} {:^7}".format('', 'A','B','C','D','E','F','G','H'))

    
    def postaviIgraca(self, tabla, row, col):
        rettabla = tabla
        rettabla[row][col] = self._igrac
        return rettabla
    
    def postaviBota(self, tabla, row, col):
        rettabla = tabla
        rettabla[row][col] = self._bot
        return rettabla
    
    def isLegalanPotez(slef, tabla, row, col, igrac):
        match(igrac):
            case 1: protivnik = -1
            case -1: protivnik = 1

        if tabla[row][col] != None:
            return False, None
        
        zaObrtanje = []

        #provera desno:
        mozeDesno = False
        obrnutiDesno = []
        for i in range(col+1, 8 , 1):
            if tabla[row][i] == protivnik:
                obrnutiDesno.append((row, i))
                mozeDesno = True
            if tabla[row][i] == igrac and len(obrnutiDesno) >= 1:
                mozeDesno = True
                break
            elif tabla[row][i] != protivnik and tabla[row][i] != igrac:
                mozeDesno = False
                break
        if mozeDesno:
            zaObrtanje.append(obrnutiDesno)

        #provera levo:
        mozeLevo = False
        obrnutiLevo = []
        for i in range(col-1, 0-1, -1):
            if tabla[row][i] == protivnik:
                obrnutiLevo.append((row, i))
                mozeLevo = True
            if tabla[row][i] == igrac and len(obrnutiLevo) >= 1:
                mozeLevo = True
                break
            elif tabla[row][i] != protivnik and tabla[row][i] != igrac:
                mozeLevo = False
                break
        if mozeLevo:
            zaObrtanje.append(obrnutiLevo)
        
        #provera dole:
        mozeDole = False
        obrnutiDole = []
        for i in range(row+1, 8, 1):
            if tabla[i][col] == protivnik:
                obrnutiDole.append((i, col))
                mozeDole = True
            elif tabla[i][col] == igrac and len(obrnutiDole) >= 1:
                mozeDole = True
                break
            elif tabla[i][col] != protivnik and tabla[i][col] != igrac:
                mozeDole = False
                break
        if mozeDole:
            zaObrtanje.append(obrnutiDole)

        #provera gore:
        mozeGore = False
        obrnutiGore = []
        for i in range(row-1, 0-1, -1):
            if tabla[i][col] == protivnik:
                obrnutiGore.append((i, col))
                mozeGore = True
            elif tabla[i][col] == igrac and len(obrnutiGore) >= 1:
                mozeGore = True
                break
            elif tabla[i][col] != protivnik and tabla[i][col] != igrac:
                mozeGore = False
                break
        if mozeGore:
            zaObrtanje.append(obrnutiGore)

        #provera desno-dole:
        mozeDesnoDole = False
        obrnutiDesnoDole = []
        for i in range(col+1, 8 , 1):
            for j in range(row+1, 8, 1):
                if tabla[j][i] == protivnik:
                    obrnutiDesnoDole.append((j, i))
                    mozeDesnoDole = True
                if tabla[j][i] == igrac and len(obrnutiDesnoDole) >= 1:
                    mozeDesnoDole = True
                    break
                elif tabla[j][i] != protivnik and tabla[j][i] != igrac:
                    mozeDesnoDole = False
                    break
        if mozeDesnoDole:
            zaObrtanje.append(obrnutiDesnoDole)
        
        #provera desno-gore:
        mozeDesnoGore = False
        obrnutiDesnoGore = []
        for i in range(col+1, 8 , 1):
            for j in range(row-1, 0-1, -1):
                if tabla[j][i] == protivnik:
                    obrnutiDesnoGore.append((j, i))
                    mozeDesnoGore = True
                if tabla[j][i] == igrac and len(obrnutiDesnoGore) >= 1:
                    mozeDesnoGore = True
                    break
                elif tabla[j][i] != protivnik and tabla[j][i] != igrac:
                    mozeDesnoGore = False
                    break
        if mozeDesnoGore:
            zaObrtanje.append(obrnutiDesnoGore)

        #provera levo-dole:
        mozeLevoDole = False
        obrnutiLevoDole = []
        for i in range(col-1, 0-1, -1):
            for j in range(row+1, 8, 1):
                if tabla[j][i] == protivnik:
                    obrnutiLevoDole.append((j, i))
                    mozeLevoDole = True
                if tabla[j][i] == igrac and len(obrnutiLevoDole) >= 1:
                    mozeLevoDole = True
                    break
                elif tabla[j][i] != protivnik and tabla[j][i] != igrac:
                    mozeLevoDole = False
                    break
        if mozeLevoDole:
            zaObrtanje.append(obrnutiLevoDole)

        #provera levo-gore:
        mozeLevoGore = False
        obrnutiLevoGore = []
        for i in range(col-1, 0-1, -1):
            for j in range(row-1, 0-1, -1):
                if tabla[j][i] == protivnik:
                    obrnutiLevoGore.append((j, i))
                    mozeLevoGore = True
                if tabla[j][i] == igrac and len(obrnutiLevoGore) >= 1:
                    mozeLevoGore = True
                    break
                elif tabla[j][i] != protivnik and tabla[j][i] != igrac:
                    mozeLevoGore = False
                    break
        if mozeLevoGore:
            zaObrtanje.append(obrnutiLevoGore)

        if len(zaObrtanje) > 0:
            return True, zaObrtanje
        else:
            return False, None
        
    def azurirajMogucePoteze(self):
        for i in range(8):
            for j in range(8):
                potezIgrac, obrtanjeIgrac = self.isLegalanPotez(self._tabla, i, j, self._igrac)
                potezBot, obrtanjeBot = self.isLegalanPotez(self._tabla, i, j, self._bot)
                if potezIgrac:
                    print("ddaaa")
                    self._tablaMogucihPoteza[i][j] = self._igrac
                elif potezBot:
                    print("ddaaa")
                    self._tablaMogucihPoteza[i][j] = self._bot
                else:
                    self._tablaMogucihPoteza[i][j] = None

    def _isKraj(self, tabelaMogucihPoteza):
        kraj = True
        for i in range(8):
            for j in range(8):
                if tabelaMogucihPoteza[i][j] != None:
                    kraj = False
                    break
        return kraj
    
    def minmax():
        pass