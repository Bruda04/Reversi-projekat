from Heuristics.Heuristika import calculateHeuristics
import os, copy, time, math

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
                [None, None, None, -1, 1, None, None, None],    #None = prazno, 1 = Black, -1 = White
                [None, None, None, 1, -1, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                ]
        
        self._tablaMogucihPoteza = {}

        self._sracunateHeuristike = {}

        self._varijabilnaDubina = 3.1
        
    
    def prikazTable(self, clear):
        boje = [None, "⬛", "⬜"]
        if clear:
            if os.name == "nt":
                os.system("cls")
            else:
                os.system("clear")
        print()
        print(f"Igrac {boje[self._igrac]}: {self._igracScore}")
        print(f"Bot {boje[self._bot]}: {self._botScore}")
        print()
        print ("   |{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|".format("🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭"))
        brojevi = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]
        redniBroj = 0
        for i in range(8):
            kolona = self._tabla[i]
            prntCol = []
            for j in range(8):
                polje = kolona[j]
                match(polje):
                    case None: prntCol.append("🟩")
                    case 1: prntCol.append("⬛")
                    case -1: prntCol.append("⬜")
                if ((i, j) in self._tablaMogucihPoteza):
                    prntCol[j] = "🟥"
                    
            print("-"*47)
            print("{:^4} |{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}| {:^4}".format(brojevi[redniBroj], prntCol[0], prntCol[1], prntCol[2], prntCol[3], prntCol[4], prntCol[5], prntCol[6], prntCol[7], brojevi[redniBroj]))
            redniBroj += 1
        print("-"*47)
        print ("   |{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|".format("🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭"))


        print()
    
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
                obrnutiLevoGore.append((y, x))
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

    def isKrajIgre(self, moguciPotezi):
        if len(moguciPotezi) == 0:
            return True
        else:
            return False
    
    def minmax(self, tabla, dubina, igraBot, alpha, beta, vreme):
        if igraBot:
            moguciPoteziBota = self.izracunajMogucePoteze(tabla, self._bot)
            kraj = self.isKrajIgre(moguciPoteziBota)


        else:
            moguciPoteziIgraca = self.izracunajMogucePoteze(tabla, self._igrac)
            kraj = self.isKrajIgre(moguciPoteziIgraca)
        
        if dubina == 0 or kraj or (time.time() - vreme) > self._varijabilnaDubina:
            hashTable = str(tabla)
            if hashTable in self._sracunateHeuristike:
                return self._sracunateHeuristike[hashTable]
            else:
                if igraBot:
                    vrednostHeuristike = calculateHeuristics(tabla, moguciPoteziBota, self.izracunajMogucePoteze(tabla, self._igrac), self._bot, self._igrac)
                else:
                    vrednostHeuristike = calculateHeuristics(tabla, self.izracunajMogucePoteze(tabla, self._bot), moguciPoteziIgraca, self._bot, self._igrac)
                self._sracunateHeuristike[hashTable] = vrednostHeuristike
                return vrednostHeuristike
            

        
        if igraBot:
            maximalanaEvaluacija = -math.inf
            for (i, j) in moguciPoteziBota:
                tablaCopy = copy.deepcopy(tabla)
                novaTabla = self.postaviBota(tablaCopy, i, j, moguciPoteziBota[(i ,j)])
                evaluacijaSituacije = self.minmax(novaTabla, dubina - 1, False, alpha, beta, vreme)
                maximalanaEvaluacija = max(maximalanaEvaluacija, evaluacijaSituacije)
                alpha = max(alpha, evaluacijaSituacije)
                if beta <= alpha:
                    break
            return maximalanaEvaluacija
        
        else:
            minimalnaEvaluacija = math.inf
            for (i, j) in moguciPoteziIgraca:
                tablaCopy = copy.deepcopy(tabla)
                novaTabla = self.postaviIgraca(tablaCopy, i, j, moguciPoteziIgraca[(i, j)])
                evaluacijaSituacije = self.minmax(novaTabla, dubina - 1, True, alpha, beta, vreme)
                minimalnaEvaluacija = min(minimalnaEvaluacija, evaluacijaSituacije)
                beta = min(beta, evaluacijaSituacije)
                if beta <= alpha:
                    break
            return minimalnaEvaluacija
        
    def proglasiPobednika(self):
        if self._botScore > self._igracScore:
                print("BOT JE POBEDIO")
        elif self._botScore < self._igracScore:
            print("IGRAC JE POBEDIO")
        else:
                print("NERESENO")

    def igracPotez(self):
        if self._kraj:
            return

        self.azurirajMogucePotezeIgraca()
        kraj = self.isKrajIgre(self._tablaMogucihPoteza)
    
        if kraj:
            moguciPoteziBota = self.izracunajMogucePoteze(self._tabla, self._bot)
            krajProtivnik = self.isKrajIgre(moguciPoteziBota)
            if not krajProtivnik:
                self._kraj = True
                self._tablaMogucihPoteza = {}
                self.prikazTable(True)
                print()
                print("BOT JE POBEDIO")
            else:
                self._kraj = True
                self._tablaMogucihPoteza = {}
                self.prikazTable(True)
                self.proglasiPobednika()
            return
        

        self.prikazTable(True)
        ponudaPoteza = []
        print("Ponudjeni potezi:")
        indexPoteza = 0
        for potez in self._tablaMogucihPoteza:
            indexPoteza += 1
            ponudaPoteza.append(potez)
            print(f"{indexPoteza}. {potez[0] + 1}{chr(potez[1] + 65)} - obrnuce {len(self._tablaMogucihPoteza[potez])}")

        validanUnos = False
        while not validanUnos:
            unos = int(input("Unesite indeks zeljenog poteza: ")) - 1
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
        if self._kraj:
            return
        moguciPoteziBota = self.izracunajMogucePoteze(self._tabla, self._bot)

        kraj = self.isKrajIgre(moguciPoteziBota)

        if kraj:
            moguciPoteziIgraca =  self.izracunajMogucePoteze(self._tabla, self._igrac)
            krajProtivnik = self.isKrajIgre(moguciPoteziIgraca)
            if not krajProtivnik:
                self._kraj = True
                self._tablaMogucihPoteza = {}
                self.prikazTable(True)
                print("IGRAC JE POBEDIO")
            else:
                self._kraj = True
                self._tablaMogucihPoteza = {}
                self.prikazTable(True)
                self.proglasiPobednika()
            return
        self._tablaMogucihPoteza = moguciPoteziBota
        self.prikazTable(False)
        moguciPoteziBotaLista = []
        vrednostiPoteza = []
        vremeStart = time.time()
        for (i, j) in moguciPoteziBota:
            timeDelta = time.time()-vremeStart
            if (timeDelta) > self._varijabilnaDubina:
                break
            tablaTmp = self.postaviBota(copy.deepcopy(self._tabla), i, j, moguciPoteziBota[(i,j)]) # odradjen potez
            moguciPoteziBotaLista.append((i,j))

            if len(moguciPoteziBota) >= 4:
                vrednostPoteza = self.minmax(tablaTmp, 4, True, -math.inf, math.inf, vremeStart)
            else:
                vrednostPoteza = self.minmax(tablaTmp, 5, True, -math.inf, math.inf, vremeStart)
                            
            vrednostiPoteza.append(vrednostPoteza)

        najboljiPotez = moguciPoteziBotaLista[vrednostiPoteza.index(max(vrednostiPoteza))]

        zaObrtanje = moguciPoteziBota[najboljiPotez]
        self._tabla = self.postaviBota(copy.deepcopy(self._tabla), najboljiPotez[0], najboljiPotez[1], zaObrtanje)
        self._botScore += 1 + len(zaObrtanje)
        self._igracScore -= len(zaObrtanje)

    def igracBot(self):
        if self._kraj:
            return
        moguciPoteziIgracaBota = self.izracunajMogucePoteze(self._tabla, self._bot)

        kraj = self.isKrajIgre(moguciPoteziIgracaBota)
        
        if kraj:
            moguciPoteziIgraca = self.izracunajMogucePoteze(self._tabla, self._igrac)
            krajProtivnik = self.isKrajIgre(moguciPoteziIgraca)  
            if not krajProtivnik:
                self._kraj = True
                self._tablaMogucihPoteza = {}
                self.prikazTable(True)
                print("IGRAC JE POBEDIO")
            else:
                self._kraj = True
                self._tablaMogucihPoteza = {}
                self.prikazTable(True)
                self.proglasiPobednika()
            return

        self._tablaMogucihPoteza = self.izracunajMogucePoteze(self._tabla, self._bot)
        self.prikazTable(False)
        ponudaPoteza = []
        print("Ponudjeni potezi:")
        indexPoteza = 0
        for potez in moguciPoteziIgracaBota:
            indexPoteza += 1
            ponudaPoteza.append(potez)
            print(f"{indexPoteza}. {potez[0] + 1}{chr(potez[1] + 65)} - obrnuce {len(moguciPoteziIgracaBota[potez])}")

        validanUnos = False
        while not validanUnos:
            unos = int(input("Unesite zeljeni potez: ")) - 1
            if unos >= 0 and unos < len(ponudaPoteza):
                validanUnos = True
            else:
                print("Niste uneli validnu opciju!")
        odabraniPotez = ponudaPoteza[unos]
        trenutnaTabla = copy.deepcopy(self._tabla)
        zaObrtanje = moguciPoteziIgracaBota[odabraniPotez]
        self._tabla = self.postaviBota(trenutnaTabla, odabraniPotez[0], odabraniPotez[1], zaObrtanje)
        self._botScore +=1 + len(zaObrtanje)
        self._igracScore -= len(zaObrtanje)

    def igrajProtivBota(self):
        if self._igrac == 1:
            while self._kraj != True:
                self.igracPotez()
                self.botPotez()
        elif self._bot == 1:
            while self._kraj != True:
                self.botPotez()
                self.igracPotez()

    def igrajProtivIgraca(self):
        if self._igrac == 1:
            while self._kraj != True:
                self.igracPotez()
                self.igracBot()
        elif self._bot == 1:
            while self._kraj != True:
                self.igracBot()
                self.igracPotez()


if __name__ == "__main__":
    print("POKRENITE main.py FILE")
