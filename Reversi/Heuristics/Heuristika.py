def calculateHeuristics(tabla, tablaMogucihPotezaMaksimizer, tablaMogucihPotezaMinimizer, maksimizer, minimizer):
    maksimizerZetoni = 0
    minimizerZetoni = 0
    maksimizerUglova = 0
    minimizerUglova = 0
    maksimizerStabilnost = 0
    minimizerStabilnost = 0
    kvalitet = 0

    kvalitetPolja = [
        [20, -3, 11, 8, 8, 11, -3, 20],
        [-3, -7, -4, 1, 1, -4, -7, -3],
        [11, -4, 2, 2, 2, 2, -4, 11],
        [8, 1, 2, -3, -3, 2, 1, 8],
        [8, 1, 2, -3, -3, 2, 1, 8],
        [11, -4, 2, 2, 2, 2, -4, 11],
        [-3, -7, -4, 1, 1, -4, -7, -3],
        [20, -3, 11, 8, 8, 11, -3, 20]
    ]

    for i in range(8):
         for j in range(8):
            if tabla[i][j] == maksimizer:
                maksimizerZetoni += 1
                kvalitet += kvalitetPolja[i][j]
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
                kvalitet -= kvalitetPolja[i][j]
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

    #Razlika zetona
    if maksimizerZetoni > minimizerZetoni:
        razlikaZetona = (100 * maksimizerZetoni) / (maksimizerZetoni + minimizerZetoni)
    elif minimizerZetoni > maksimizerZetoni:
        razlikaZetona = -(100 * minimizerZetoni) / (maksimizerZetoni + minimizerZetoni)
    else:
        razlikaZetona = 0    

    #Stabilnost
    if maksimizerStabilnost > minimizerStabilnost:
        stabilnost = (100 * maksimizerStabilnost) / (maksimizerStabilnost + minimizerStabilnost)
    elif minimizerStabilnost > maksimizerStabilnost:
        stabilnost = -(100 * minimizerStabilnost) / (maksimizerStabilnost + minimizerStabilnost)
    else:
        stabilnost = 0


    #Uglovi zauzeti
    uglovi = 25 * (maksimizerUglova - minimizerUglova)
    
    #Mobilnost
    brojMogucihPotezaMaksimizer = len(tablaMogucihPotezaMaksimizer)
    brojMogucihPotezaMinimizer = len(tablaMogucihPotezaMinimizer)
    if brojMogucihPotezaMaksimizer > brojMogucihPotezaMinimizer:
        mobilnost = (100 * brojMogucihPotezaMaksimizer) / (brojMogucihPotezaMaksimizer + brojMogucihPotezaMinimizer)
    elif brojMogucihPotezaMinimizer > brojMogucihPotezaMaksimizer:
        mobilnost = -(100* brojMogucihPotezaMinimizer) / (brojMogucihPotezaMaksimizer + brojMogucihPotezaMinimizer)
    else:
        mobilnost = 0


    return 10 * razlikaZetona + 801.724 * uglovi + 78.922 * mobilnost + 74.396 * stabilnost + 10 * kvalitet


if __name__ == "__main__":
    pass