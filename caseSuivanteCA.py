import numpy as np
import random
from floorField import *
from astar import *

'''
Permet de sélectionner le premier, deuxième ou troisième choix de déplacement

Préconditions :
    arrayFloorField : Champ scalaire uniquement
    nbCol : indice des colonnes
    nbLig : indice des lignes
    variableDeplacement : Indique le déplacement entre la case étudiée actuelle et l'endroit réel où se trouve la personne
Postconditions:
    Renvoie la prochaine case libre pour se déplacer
'''
def caseAller(arrayFloorField, nbCol, nbLig, variableDeplacement):
    tableauPos = [0]*9 
    #Créer un tableau de 9 cases avec une valeur assez haute pour qu'aucune valeur ne puisse la dépasser. 
    #Lors du tri les plus grandes valeurs seront mis à la fin et ignorés
    tableauCaseCol = [0]*9 #Créer un tableau de 9 cases pour stocker les potentielles case en colonne à se déplacer
    tableauCaseLig = [0]*9 #Idem mais pour les lignes
    nombre = 0 #Nous incrémenterons cette valeur de 0 à 8 pour balayer toutes les cases des tableaux

    #La fonction suivante va regarder les 8 cases autour de la personnes
    #Elle va alors stocker les différences (case autour - case avec la personne) dans deux tableaux 
    for col in range(3):
        for lig in range(3):
            if arrayFloorField[nbCol + 1, nbLig + 1] - arrayFloorField[nbCol + col, nbLig + lig] > 0 and arrayFloorField[nbCol + col, nbLig + lig] != 500: #Condition qui ne sélectionne pas les différences négatives ni les murs
                tableauPos[nombre] = arrayFloorField[nbCol + 1, nbLig + 1] - arrayFloorField[nbCol + col, nbLig + lig]  
                #On stocke les différences dans un tableau
                tableauCaseCol[nombre] = col + 1 
                #On stocke le nombre de lignes à se déplacer par rapport à l'endroit où la condition est vérifiée
                #Donc le tableau peut comporter plusieurs valeurs
                tableauCaseLig[nombre] = lig + 1 #Pareil mais pour les colonnes
            nombre += 1 #Incrémente la variable vu ligne.56


    tableauPos, tableauCaseCol, tableauCaseLig = (list(t) for t in zip(*sorted(zip(tableauPos, tableauCaseCol, tableauCaseLig)))) 
    #cette ligne permet grâce à la fonction zip de python de trier le premier tableau (tableauPos) en fonction de la plus petite valeur 
    #Et de trier les deux autres tableaux comme le premier

    #Cette grande boucle permet de chosir parmi deux valeurs égales. Si list1[i] = list2[i] 
    #On échange les valeurs à l'intérieur soit list1[i] = list2[i] et list2[i] = list1[i]
    #Les listes suivantes sont lues de la forme 8 - i car après l'avoir triée les différences les plus grandes se retrouvent en fin de liste 
    for choixBoucle in range(8):
        double = random.randint(1, 2)
        stockageCol = 0
        stockageLig = 0
        if tableauPos[7 - choixBoucle] == tableauPos[8 - choixBoucle] and tableauPos[7 - choixBoucle] != 0:
            if double == 1:
                #Les valeurs de stockage permettent de ne pas écraser une des valeurs nécessaire
                stockageCol = tableauCaseCol[8 - choixBoucle]
                stockageLig = tableauCaseLig[8 - choixBoucle]
                #On échange les valeurs des deux listes
                tableauCaseLig[8 - choixBoucle] = tableauCaseLig[7 - choixBoucle]
                tableauCaseCol[8 - choixBoucle] = tableauCaseCol [7 -choixBoucle]
                tableauCaseCol[7 - choixBoucle] = stockageCol
                tableauCaseLig[7 - choixBoucle] = stockageLig

    return (tableauCaseCol[8 - variableDeplacement], tableauCaseLig[8 - variableDeplacement]) 
#On retourne la case à se déplacer en fonction de variableDeplacement pour prendre le deuxième ou troième déplacement possible

