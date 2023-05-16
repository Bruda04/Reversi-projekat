def calculateHeuristics(tabla, tablaMogucihPoteza, maksimizer, minimizer):
    maksimizerZetoni = 0
    minimizerZetoni = 0
    maksimizerPoteza = 0
    minimizerPoteza = 0
    maksimizerUglova = 0
    minimizerUglova = 0
    maksimizerStabilnost = 0
    minimizerStabilnost = 0

    for i in range(8):
         for j in range(8):
            if tablaMogucihPoteza[i][j] == maksimizer:
                maksimizerPoteza += 1
                continue
            elif tablaMogucihPoteza[i][j] == minimizer:
                minimizerPoteza += 1
                continue

            if tabla[i][j] == maksimizer:
                maksimizerZetoni += 1
                if (i == 7 or i == 0) and (j == 0 or j == 7):
                    maksimizerUglova += 1
                    maksimizerStabilnost += 1
                    continue
                    
                if ((j<7 and tabla[i][j+1] == minimizer ) or 
                    (i<7 and tabla[i+1][j] == minimizer) or 
                    (i<7 and j<7 and tabla[i+1][j+1] == minimizer) or
                    (j>0 and tabla[i][j-1] == minimizer) or 
                    (i>0 and tabla[i-1][j] == minimizer) or 
                    (i>0 and j>0 and tabla[i-1][j-1] == minimizer)):
                    maksimizerStabilnost -= 1



            elif tabla[i][j] == minimizer:
                minimizerZetoni += 1
                if (i == 7 or i == 0) and (j == 0 or j == 7):
                    minimizerUglova += 1
                    minimizerStabilnost += 1
                    continue

                if ((j<7 and tabla[i][j+1] == maksimizer ) or 
                    (i<7 and tabla[i+1][j] == maksimizer) or 
                    (i<7 and j<7 and tabla[i+1][j+1] == maksimizer) or
                    (j>0 and tabla[i][j-1] == maksimizer) or 
                    (i>0 and tabla[i-1][j] == maksimizer) or 
                    (i>0 and j>0 and tabla[i-1][j-1] == maksimizer)):
                    minimizerStabilnost -= 1

    razlikaZetona = 100 * (maksimizerZetoni - minimizerZetoni ) / (maksimizerZetoni + minimizerZetoni)
    
    if ( maksimizerPoteza + minimizerPoteza != 0):
        mobilnost = 100 * (maksimizerPoteza - minimizerPoteza) / (maksimizerPoteza + minimizerPoteza)
    else:
        mobilnost = 0

    if ( maksimizerUglova + minimizerUglova != 0):
        uglovi = 100 * (maksimizerUglova - minimizerUglova) / (maksimizerUglova + minimizerUglova)
    else:
        uglovi = 0
            
    if ( maksimizerStabilnost + minimizerStabilnost != 0):
        stabilnost = 100 * (maksimizerStabilnost - minimizerStabilnost) / (maksimizerStabilnost + minimizerStabilnost)
    else:
        stabilnost = 0
    
    # print(maksimizerStabilnost, minimizerStabilnost)
    # print(razlikaZetona, mobilnost, uglovi, stabilnost)
    # print((razlikaZetona + mobilnost + uglovi + stabilnost)/4)
    return (razlikaZetona + mobilnost + uglovi + stabilnost)/4


if __name__ == "__main__":

        tabla = [ 
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, 1, -1, None, None, None],    #None = prazno, 1 = Black, -1 = White
            [None, None, None, -1, 1, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [1, None, None, None, None, None, None, None],
            ]
        
        tablaMogucihPoteza = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, -1, 1, None, None, None],
            [None, None, -1, None, None, 1, None, None],
            [None, None, 1, None, None, -1, None, None],    #None = prazno, 1 = Black, -1 = White
            [None, None, None, 1, -1, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            ]


        calculateHeuristics(tabla, tablaMogucihPoteza, 1, -1)