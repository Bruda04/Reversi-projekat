from Heuristics.Heuristika import calculateHeuristics
import os, copy, time

class Reversi(object):
    def __init__(self, player):
        if player == 1: #igrac je crni
            self._igrac = 1
            self._bot = -1
        elif player == -1: #igrac je beli
            self._igrac = -1
            self._bot = 1

        self._igracScore = 2
        self._botScore = 2

        self._kraj = False

        self._tabla = [ 
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, 1, -1, None, None, None],    #None = prazno, 1 = Black, -1 = White
                [None, None, None, -1, 1, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                ]
        
        self._tablaMogucihPoteza = {}

        self._naPotezu = self._igrac

        self._sracunateHeuristike = {}
        
    
    def prikazTable(self):
        os.system("clear")
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
                if ((i, j) in self._tablaMogucihPoteza):
                    prntCol[j] = "X"
                    
            print()
            print ("{:^7} {:^7} {:^7} {:^7} {:^7} {:^7} {:^7} {:^7} {:^7} {:^7}".format(redniBroj, prntCol[0], prntCol[1], prntCol[2], prntCol[3], prntCol[4], prntCol[5], prntCol[6], prntCol[7], redniBroj))
            redniBroj += 1
        print ("\n{:^7} {:^7} {:^7} {:^7} {:^7} {:^7} {:^7} {:^7} {:^7}".format('', 'A','B','C','D','E','F','G','H'))

    
    def postaviIgraca(self, tabla, row, col, zaObrtanje):
        rettabla = tabla
        rettabla[row][col] = self._igrac
        for (i, j) in zaObrtanje:
            rettabla[i][j] = self._igrac
        return rettabla
    
    def postaviBota(self, tabla, row, col, zaObrtanje):
        rettabla = tabla
        rettabla[row][col] = self._bot
        for (i, j) in zaObrtanje:
            rettabla[i][j] = self._bot
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
            if tabla[row][i] == protivnik and i != 7:
                obrnutiDesno.append((row, i))
                mozeDesno = True
            elif tabla[row][i] == igrac and len(obrnutiDesno) >= 1:
                mozeDesno = True
                break
            elif tabla[row][i] != protivnik and tabla[row][i] != igrac:
                mozeDesno = False
                break
            else:
                mozeDesno = False
                break 
        if mozeDesno:
            zaObrtanje.extend(obrnutiDesno)

        #provera levo:
        mozeLevo = False
        obrnutiLevo = []
        for i in range(col-1, 0-1, -1):
            if tabla[row][i] == protivnik and i != 0:
                obrnutiLevo.append((row, i))
                mozeLevo = True
            elif tabla[row][i] == igrac and len(obrnutiLevo) >= 1:
                mozeLevo = True
                break
            elif tabla[row][i] != protivnik and tabla[row][i] != igrac:
                mozeLevo = False
                break
            else:
                mozeLevo = False
                break 
        if mozeLevo:
            zaObrtanje.extend(obrnutiLevo)
        
        #provera dole:
        mozeDole = False
        obrnutiDole = []
        for i in range(row+1, 8, 1):
            if tabla[i][col] == protivnik and i != 7:
                obrnutiDole.append((i, col))
                mozeDole = True
            elif tabla[i][col] == igrac and len(obrnutiDole) >= 1:
                mozeDole = True
                break
            elif tabla[i][col] != protivnik and tabla[i][col] != igrac:
                mozeDole = False
                break
            else:
                mozeDole = False
                break 
        if mozeDole:
            zaObrtanje.extend(obrnutiDole)

        #provera gore:
        mozeGore = False
        obrnutiGore = []
        for i in range(row-1, 0-1, -1):
            if tabla[i][col] == protivnik and i != 0:
                obrnutiGore.append((i, col))
                mozeGore = True
            elif tabla[i][col] == igrac and len(obrnutiGore) >= 1:
                mozeGore = True
                break
            elif tabla[i][col] != protivnik and tabla[i][col] != igrac:
                mozeGore = False
                break
            else:
                mozeGore = False
                break 
        if mozeGore:
            zaObrtanje.extend(obrnutiGore)

        #provera desno-dole:
        mozeDesnoDole = False
        obrnutiDesnoDole = []
        for i in range(1, (min(8 - (col + 1), 8 - (row + 1)) + 1), 1):
            x = col + i
            y = row + i
            
            if tabla[y][x] == protivnik and x != 7 and y != 7:
                obrnutiDesnoDole.append((y, x))
                mozeDesnoDole = True
            elif tabla[y][x] == igrac and len(obrnutiDesnoDole) >= 1:
                mozeDesnoDole = True
                break
            elif tabla[y][x] != protivnik and tabla[y][x] != igrac:
                mozeDesnoDole = False
                break
            else:
                mozeDesnoDole = False
                break 
        if mozeDesnoDole:
            zaObrtanje.extend(obrnutiDesnoDole)
        
        #provera desno-gore:
        mozeDesnoGore = False
        obrnutiDesnoGore = []
        for i in range(1, (min(8 - (col + 1), row) + 1), 1):
            x = col + i
            y = row - i

            if tabla[y][x] == protivnik and x != 7 and y != 0:
                obrnutiDesnoGore.append((y, x))
                mozeDesnoGore = True
            elif tabla[y][x] == igrac and len(obrnutiDesnoGore) >= 1:
                mozeDesnoGore = True
                break
            elif tabla[y][x] != protivnik and tabla[y][x] != igrac:
                mozeDesnoGore = False
                break
            else:
                mozeDesnoGore = False
                break 
        if mozeDesnoGore:
            zaObrtanje.extend(obrnutiDesnoGore)

        #provera levo-dole:
        mozeLevoDole = False
        obrnutiLevoDole = []
        for i in range(1, (min(col, 8 - (row + 1)) + 1), 1):
            x = col - i
            y = row + i
            
            if tabla[y][x] == protivnik and x != 0 and y != 7:
                obrnutiLevoDole.append((y, x))
                mozeLevoDole = True
            elif tabla[y][x] == igrac and len(obrnutiLevoDole) >= 1:
                mozeLevoDole = True
                break
            elif tabla[y][x] != protivnik and tabla[y][x] != igrac:
                mozeLevoDole = False
                break
            else:
                mozeLevoDole = False
                break 
        if mozeLevoDole:
            zaObrtanje.extend(obrnutiLevoDole)

        #provera levo-gore:
        mozeLevoGore = False
        obrnutiLevoGore = []
        for i in range(1, (min(col, row) + 1), 1):
            x = col - i
            y = row - i

            if tabla[y][x] == protivnik and x != 0 and y != 0:
                obrnutiLevoGore.append((y, i))
                mozeLevoGore = True
            elif tabla[y][x] == igrac and len(obrnutiLevoGore) >= 1:
                mozeLevoGore = True
                break
            elif tabla[y][x] != protivnik and tabla[y][x] != igrac:
                mozeLevoGore = False
                break
            else:
                mozeLevoGore = False
                break 
        if mozeLevoGore:
            zaObrtanje.extend(obrnutiLevoGore)

        if len(zaObrtanje) > 0:
            return True, zaObrtanje
        else:
            return False, None
    
    def izracunajMogucePoteze(self, tabla, igrac):
        retTabla = {}
        for i in range(8):
            for j in range(8):
                legalan, zaObrtanje = self.isLegalanPotez(tabla, i, j, igrac)
                if legalan:
                    retTabla[(i, j)] = zaObrtanje

        return retTabla

    def azurirajMogucePotezeIgraca(self):
        self._tablaMogucihPoteza = self.izracunajMogucePoteze(self._tabla, self._igrac)
        

    def isKraj(self, tabla):
        brojPotezaIgrac = len(self.izracunajMogucePoteze(tabla, self._igrac))
        brojPotezaBot = len(self.izracunajMogucePoteze(tabla, self._bot))
        if brojPotezaBot == 0 and brojPotezaIgrac == 0:
            return True
        else:
            return False
    
    def minmax(self, tabla, dubina, igraBot, zaOdigrati, alpha, beta, vreme):
        if dubina == 0 or self.isKraj(tabla) or (time.time() - vreme) >= 3:
            hashTable = str(tabla)
            if hashTable in self._sracunateHeuristike:
                return (zaOdigrati, self._sracunateHeuristike[hashTable])
            else:
                if igraBot:
                    vrednostHeuristike = calculateHeuristics(tabla, self.izracunajMogucePoteze(tabla, self._bot), self.izracunajMogucePoteze(tabla, self._igrac), self._bot, self._igrac)
                else:
                    vrednostHeuristike = calculateHeuristics(tabla, self.izracunajMogucePoteze(tabla, self._igrac), self.izracunajMogucePoteze(tabla, self._bot), self._igrac, self._bot)
                self._sracunateHeuristike[hashTable] = vrednostHeuristike
                return (zaOdigrati, vrednostHeuristike)

        if igraBot:
            maximalanaEvaluacija = -99999
            moguciPoteziBota = self.izracunajMogucePoteze(tabla, self._bot)
            for (i, j) in moguciPoteziBota:
                tablaCopy = copy.deepcopy(tabla)
                novaTabla = self.postaviBota(tablaCopy, i, j, moguciPoteziBota[(i ,j)])
                if zaOdigrati == None:
                    zaOdigrati, evaluacijaSituacije = self.minmax(novaTabla, dubina - 1, False, (i, j), alpha, beta, vreme)
                else:
                    zaOdigrati, evaluacijaSituacije = self.minmax(novaTabla, dubina - 1, False, zaOdigrati, alpha, beta, vreme)
                maximalanaEvaluacija = max(maximalanaEvaluacija, evaluacijaSituacije)
                alpha = max(alpha, evaluacijaSituacije)
                if beta <= alpha:
                    break
            return (zaOdigrati, maximalanaEvaluacija)
        
        else:
            minimalnaEvaluacija = 99999
            moguciPoteziIgraca = self.izracunajMogucePoteze(tabla, self._igrac)
            for (i, j) in moguciPoteziIgraca:
                tablaCopy = copy.deepcopy(tabla)
                novaTabla = self.postaviIgraca(tablaCopy, i, j, moguciPoteziIgraca[(i, j)])
                zaOdigrati, evaluacijaSituacije = self.minmax(novaTabla, dubina - 1, True, zaOdigrati, alpha, beta, vreme)
                minimalnaEvaluacija = min(minimalnaEvaluacija, evaluacijaSituacije)
                beta = min(beta, evaluacijaSituacije)
                if beta <= alpha:
                    break
            return (zaOdigrati, minimalnaEvaluacija)

    def igracPotez(self):
        self.azurirajMogucePotezeIgraca()

        if len(self._tablaMogucihPoteza) == 0:
            # self._kraj = True
            return

        self.prikazTable()
        ponudaPoteza = []
        print("Ponudjeni potezi:")
        indexPoteza = 0
        for potez in self._tablaMogucihPoteza:
            indexPoteza += 1
            ponudaPoteza.append(potez)
            print(f"{indexPoteza}. {potez[0] + 1}{chr(potez[1] + 65)}")

        validanUnos = False
        while not validanUnos:
            unos = int(input("Unesite zeljeni potez: ")) - 1
            if unos >= 0 and unos < len(ponudaPoteza):
                validanUnos = True
            else:
                print("Niste uneli validnu opciju!")
        odabraniPotez = ponudaPoteza[unos]
        trenutnaTabla = copy.deepcopy(self._tabla)
        zaObrtanje = self._tablaMogucihPoteza[odabraniPotez]
        self._tabla = self.postaviIgraca(trenutnaTabla, odabraniPotez[0], odabraniPotez[1], zaObrtanje)
        self._igracScore +=1 + len(zaObrtanje)
        self._botScore -= len(zaObrtanje)

    
    def botPotez(self):
        moguciPoteziBota = self.izracunajMogucePoteze(self._tabla, self._bot)
        if len(moguciPoteziBota) == 0:
            # self._kraj = True
            return
        
        trenutnaTabla = copy.deepcopy(self._tabla)
        najboljiPotez = self.minmax(trenutnaTabla, 4, True, None, -99999, 99999, time.time())[0]

        zaObrtanje = moguciPoteziBota[najboljiPotez]
        self._tabla = self.postaviBota(self._tabla ,najboljiPotez[0], najboljiPotez[1], zaObrtanje)
        self._botScore += 1 + len(zaObrtanje)
        self._igracScore -= len(zaObrtanje)

        self.prikazTable()
    
    def igraj(self):
        while self.isKraj(self._tabla) != True:
            self.igracPotez()
            self.botPotez()

if __name__ == "__main__":
    igra = Reversi(1)
    igra.igraj()
    

    