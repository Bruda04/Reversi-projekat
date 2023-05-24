import math
def calculateHeuristics(tabla, tablaMogucihPotezaMaksimizer, tablaMogucihPotezaMinimizer, maksimizer, minimizer):
    maksimizerZetoni = 0
    minimizerZetoni = 0
    maksimizerUglova = 0
    minimizerUglova = 0
    maksimizerStabilnost = 0
    minimizerStabilnost = 0
    kvalitet = 0
    maksimizerBlizinaUglova = 0
    minimizerBlizinaUglova = 0

    vrednostX = [-1, -1, 0, 1, 1, 1, 0, -1]
    vrednostY = [0, 1, 1, 1, 0, -1, -1, -1]

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


    # Mobilnost
    brojMogucihPotezaMaksimizer = len(tablaMogucihPotezaMaksimizer)
    brojMogucihPotezaMinimizer = len(tablaMogucihPotezaMinimizer)
    if brojMogucihPotezaMaksimizer > brojMogucihPotezaMinimizer:
        mobilnost = (100 * brojMogucihPotezaMaksimizer) / (brojMogucihPotezaMaksimizer + brojMogucihPotezaMinimizer)
    elif brojMogucihPotezaMinimizer > brojMogucihPotezaMaksimizer:
        mobilnost = -(100* brojMogucihPotezaMinimizer) / (brojMogucihPotezaMaksimizer + brojMogucihPotezaMinimizer)
    else:
        mobilnost = 0

    if  brojMogucihPotezaMaksimizer == 0 and brojMogucihPotezaMinimizer != 0:
        return -math.inf 
    elif brojMogucihPotezaMinimizer == 0 and brojMogucihPotezaMaksimizer != 0:
        return math.inf
    elif brojMogucihPotezaMaksimizer == 0 and brojMogucihPotezaMinimizer == 0:
        if maksimizerZetoni >  minimizerZetoni:
            return math.inf
        elif minimizerZetoni > maksimizerZetoni:
            return -math.inf
        else:
            return 0
        
        
    for i in range(8):
         for j in range(8):
            if tabla[i][j] == maksimizer:
                maksimizerZetoni += 1
                kvalitet += kvalitetPolja[i][j]
                if (i == 7 or i == 0) and (j == 0 or j == 7):
                    maksimizerUglova += 1
                    


            elif tabla[i][j] == minimizer:
                minimizerZetoni += 1
                kvalitet -= kvalitetPolja[i][j]
                if (i == 7 or i == 0) and (j == 0 or j == 7):
                    minimizerUglova += 1
                                        

            elif tabla[i][j] != None:
                for k in range(8):
                    x = i + vrednostX[k]
                    y = j + vrednostY[k]
                    if (x >= 0 and x < 8  and y >= 0 and y < 8 and tabla[x][y] == None):
                        if tabla[i][j] == maksimizer:
                            maksimizerStabilnost += 1
                        else:
                            minimizerStabilnost += 1
                        break


    #Razlika zetona
    if maksimizerZetoni > minimizerZetoni:
        razlikaZetona = (100 * maksimizerZetoni) / (maksimizerZetoni + minimizerZetoni)
    elif minimizerZetoni > maksimizerZetoni:
        razlikaZetona = -(100 * minimizerZetoni) / (maksimizerZetoni + minimizerZetoni)
    else:
        razlikaZetona = 0    

    #Stabilnost
    if maksimizerStabilnost > minimizerStabilnost:
        stabilnost = -(100 * maksimizerStabilnost) / (maksimizerStabilnost + minimizerStabilnost)
    elif minimizerStabilnost > maksimizerStabilnost:
        stabilnost = (100 * minimizerStabilnost) / (maksimizerStabilnost + minimizerStabilnost)
    else:
        stabilnost = 0

    # Uglovi zauzeti
    uglovi = 25 * (maksimizerUglova - minimizerUglova)

    #Blizina uglovima
    if tabla[0][0] != maksimizer and tabla[0][0] != minimizer:
        if tabla[0][1] == maksimizer:
            maksimizerBlizinaUglova += 1
        elif tabla[0][1] == minimizer:
            minimizerBlizinaUglova += 1
        if tabla[1][1] == maksimizer:
            maksimizerBlizinaUglova += 1
        elif tabla[1][1] == minimizer:
            minimizerBlizinaUglova += 1
        if tabla[1][0] == maksimizer:
            maksimizerBlizinaUglova += 1
        elif tabla[1][0] == minimizer:
            minimizerBlizinaUglova += 1

    if tabla[0][7] != maksimizer and tabla[0][7] != minimizer:
        if tabla[0][6] == maksimizer:
            maksimizerBlizinaUglova += 1
        elif tabla[0][6] == minimizer:
            minimizerBlizinaUglova += 1
        if tabla[1][6] == maksimizer:
            maksimizerBlizinaUglova += 1
        elif tabla[1][6] == minimizer:
            minimizerBlizinaUglova += 1
        if tabla[1][7] == maksimizer:
            maksimizerBlizinaUglova += 1
        elif tabla[1][7] == minimizer:
            minimizerBlizinaUglova += 1
    
    if tabla[7][0] != maksimizer and tabla[7][0] != minimizer:
        if tabla[7][1] == maksimizer:
            maksimizerBlizinaUglova += 1
        elif tabla[7][1] == minimizer:
            minimizerBlizinaUglova += 1
        if tabla[6][1] == maksimizer:
            maksimizerBlizinaUglova += 1
        elif tabla[6][1] == minimizer:
            minimizerBlizinaUglova += 1
        if tabla[6][0] == maksimizer:
            maksimizerBlizinaUglova += 1
        elif tabla[6][0] == minimizer:
            minimizerBlizinaUglova += 1
    
    if tabla[7][7] != maksimizer and tabla[7][7] != minimizer:
        if tabla[6][7] == maksimizer:
            maksimizerBlizinaUglova += 1
        elif tabla[6][7] == minimizer:
            minimizerBlizinaUglova += 1
        if tabla[6][6] == maksimizer:
            maksimizerBlizinaUglova += 1
        elif tabla[6][6] == minimizer:
            minimizerBlizinaUglova += 1
        if tabla[7][6] == maksimizer:
            maksimizerBlizinaUglova += 1
        elif tabla[7][6] == minimizer:
            minimizerBlizinaUglova += 1

    blizinaUglova = -12.5 * (maksimizerBlizinaUglova - minimizerBlizinaUglova)
    
    

    
    # return 10 * razlikaZetona + 801.724 * uglovi + 78.922 * mobilnost + 74.396 * stabilnost + 10 * kvalitet + 382.026 * blizinaUglova
    return 100 * razlikaZetona + 801.724 * uglovi + 178.922 * mobilnost + 74.396 * stabilnost + 10 * kvalitet + 382.026 * blizinaUglova
    # return 10 * razlikaZetona + 801.724 * uglovi + 10 * kvalitet + 382.026 * blizinaUglova
    # return 10* razlikaZetona +  801.724 * uglovi

if __name__ == "__main__":
    pass