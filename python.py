import numpy as np
from tkinterInput import *
from floorField import *
from caseSuivanteCA import *
from pygameLeProgramme import *
import time

'''
Gère le mouvement des personnes dans la pièce

Préconditions :
    room : floorField
    roomWidth : taille de la pièce
    tableauDeplacements : matrice indiquant la position de chaque personnes
    nbPersonnes : nombre de personnes
Postconditions :
    Renvoie le nombre de personnes sorties
'''
def mouvementDesPersonne(room, roomWidth, tableauDeplacements, nbPersonnes):
    # Scanne les cases et obtient l'ordre actuel et les positions actuelles
    ordreActuel = scanCases(roomWidth, tableauDeplacements)
    postionsActuelles = listeCoordonnees(tableauDeplacements, ordreActuel)

    personnesSorties = 0

    dictionnaire = {}
    # Remplir le dictionnaire avec les positions actuelles des personnes
    for remplirDictionnaire in range(roomWidth**2):
        if ordreActuel[remplirDictionnaire] != 0:
            dictionnaire[ordreActuel[remplirDictionnaire]] = postionsActuelles[remplirDictionnaire]

    caseAllerActuelle = [0]*2
    tableauConflits = np.array([[0]*roomWidth]*roomWidth)
    # Boucle principale de mouvement

    for deplacement in range(roomWidth**2):
        variableDeplacement = 0

        if ordreActuel[deplacement] != 0:
            nbCol = dictionnaire[ordreActuel[deplacement]][0]
            nbLig = dictionnaire[ordreActuel[deplacement]][1]
            numActuel = tableauDeplacements[nbCol, nbLig]
            caseAllerActuelle = caseAller(room, nbCol, nbLig, variableDeplacement)
            nbColSuivant = nbCol - 2 + caseAllerActuelle[0]
            nbLigSuivant = nbLig - 2 + caseAllerActuelle[1]
            # Si la personne atteint le bord inférieur de la pièce            
            if nbLigSuivant < 0 and (nbCol == roomWidth // 2 or nbCol == roomWidth // 2 - 1):
                tableauDeplacements[nbCol, nbLig] = 0
                dictionnaire.pop(ordreActuel[deplacement])
                ordreActuel[deplacement] = 0
                personnesSorties += 1

            # Gestion des mouvements et des conflits

            while tableauDeplacements[nbCol, nbLig] == numActuel and variableDeplacement < 4:
                
                if variableDeplacement != 0:
                    caseAllerActuelle = caseAller(room, nbCol, nbLig, variableDeplacement)
                    if caseAllerActuelle[0] == 0 or caseAllerActuelle[1] == 0:
                        break
                    nbColSuivant = nbCol - 2 + caseAllerActuelle[0]
                    nbLigSuivant = nbLig - 2 + caseAllerActuelle[1]
                
                if nbLigSuivant < 0:
                    nbLigSuivant = 0
                
                if tableauDeplacements[nbColSuivant, nbLigSuivant] == 0 and tableauConflits[nbColSuivant, nbLigSuivant] == 0:
                    tableauDeplacements[nbColSuivant, nbLigSuivant] = numActuel
                    tableauConflits[nbColSuivant, nbLigSuivant] = numActuel
                    tableauDeplacements[nbCol, nbLig] = 0
                
                elif tableauConflits[nbColSuivant, nbLigSuivant] != 0:
                    numWanted = tableauConflits[nbColSuivant, nbLigSuivant]
                    hasard = random.randint(1, 3)
                    
                    if hasard == 3:
                        nbColRetour = dictionnaire[numWanted][0]
                        nbLigRetour = dictionnaire[numWanted][1]
                    
                        if tableauConflits[nbColRetour, nbLigRetour] == 0:
                            tableauDeplacements[nbColRetour, nbLigRetour] = numWanted
                            tableauConflits[nbColRetour, nbLigRetour] = numWanted
                            tableauDeplacements[nbColSuivant, nbLigSuivant] = numActuel
                            tableauConflits[nbColSuivant, nbLigSuivant] = numActuel
                            tableauDeplacements[nbCol, nbLig] = 0
                            tableauConflits[nbCol, nbLig] = 0
                variableDeplacement += 1

    return personnesSorties

'''
Créer une liste des coordonnées des personnes

Préconditions :
    tableauDeplacements : matrice indiquant la position des personnes
    ordreActuel : ordre des déplacements choisi actuel
Postconditions :
    Renvoie une liste des coordonnées de chaque personne
'''
def listeCoordonnees(tableauDeplacements, ordreActuel):
    Lcoor=[]
    dico={}
    roomWidth= len(tableauDeplacements)  #normalement ta variable est définie en dehors, tu n'as pas besoin de faire ça, mais on sait jamais
    for i in range(roomWidth): #on parcours les cases de la matrice
        for j in range(roomWidth):
            if tableauDeplacements[i, j]!=0 or tableauDeplacements[i, j]==0: #si il y a une personne, on retient sa valeur. Remarque je repere la case par [i][j] mais je crois que tu préfère faire [i,j], il faut voir lequel marche
                personne=tableauDeplacements[i, j] #on sauvegarde la personne
                dico[personne]=[i,j] #on sauvegarde ses coordonnées

    #ici on a sauvegardé toutes les personnes et leurs coordonnées

    for x in ordreActuel:
        if x != 0:
            Lcoor.append(dico[x]) #on garde l'ordre de ordreActuel
        else:
            Lcoor.append(0)

    return Lcoor

'''
Permet la modification des stratégies pour chaque personnes

Préconditions : 
    ListeDeplacements : matrice contenant les déplacements précédents de chaque personnes
    nbPersonnes : nombre de personnes
    k : indice de raison
Postconditions :
    Renvoie la stratégie actuelle pour chaque personne
'''
def ajouterStratégies(ListeDeplacements, nbPersonnes, k):
    personnes_strategies = {}
    for i in range(0, nbPersonnes):
        if ListeDeplacements[i][k - 1] == ListeDeplacements[i][k] + 1:
            personnes_strategies[i] = "presse"
        elif ListeDeplacements[i][k] == ListeDeplacements[i][k + 1]:
            personnes_strategies[i] = "poli"
        else:
            personnes_strategies[i] = "normal"
    return personnes_strategies

# Fonction pour choisir une liste aléatoirement parmi deux
def choisirListe(roomWidth, deuxListes):
    hasard = random.randint(1, 2)
    roomWidthMoitie = roomWidth // 2
    ordreActuel = [0]*roomWidth*roomWidthMoitie

    if hasard == 1:
        ordreActuel = deuxListes[0]
    else:
        ordreActuel = deuxListes[1]

    return ordreActuel

'''
Créer deux liste différentes de positions

Préconditions :
    tableauPostionHaut : Position du haut de la matrice uniquement
    tableauPostionBas : De même avec le bas
    roomWidth : Taille de la pièce
Postconditions :
    Renvoie les deux listes
'''
def creerDeuxListes(tableauPostionHaut, tableauPostionBas, roomWidth):
    nouvelleListe1 = [0]*roomWidth*roomWidth
    nouvelleListe2 = [0]*roomWidth*roomWidth

    for loop in range(roomWidth*roomWidth // 2):
            nouvelleListe1[2*loop] = tableauPostionHaut[loop]
            nouvelleListe1[2*loop+1] = tableauPostionBas[loop]
    for loop in range(roomWidth*roomWidth // 2):
            nouvelleListe2[2*loop] = tableauPostionBas[loop]
            nouvelleListe2[2*loop+1] = tableauPostionHaut[loop]

    return (nouvelleListe1, nouvelleListe2)


'''
Scanne le haut puis le bas du tableau puis détermine quelle liste parcourir en premier

Préconditions : 
    roomWidth : taille de la pièce
    tableauDeplacements : matrice avec personnes
Postconditions :
    Retourne la liste choisie
'''
def scanCases(roomWidth, tableauDeplacements):
    boucle = 0
    moitieRoomWidth = roomWidth //2
    tableauPostionHaut = [0]*roomWidth*moitieRoomWidth
    tableauPostionBas = [0]*roomWidth*moitieRoomWidth

    # Scan des positions en haut de la pièce
    for deplacementHaut in range(roomWidth + 1):
        nbColonne = roomWidth // 2
        nbLigne = deplacementHaut
        while nbColonne > 0 and nbLigne > 0:
            nbColonne -= 1
            nbLigne -= 1
            tableauPostionHaut[boucle] = tableauDeplacements[nbColonne, nbLigne]
            boucle += 1

    for deplacementHautFin in range(roomWidth // 2 - 1):
        nbColonne = roomWidth // 2 - 1 - deplacementHautFin
        nbLigne = roomWidth
        while nbColonne > 0 and nbLigne > 0:
            nbColonne -= 1
            nbLigne -= 1
            tableauPostionHaut[boucle] = tableauDeplacements[nbColonne, nbLigne]
            boucle += 1

    boucle = 0

    # Scan des positions en bas de la pièce


    for deplacementBas in range(roomWidth + 1):
        nbColonne = roomWidth // 2 - 1
        nbLigne = deplacementBas
        while nbColonne < roomWidth - 1 and nbLigne > 0:
            nbColonne += 1
            nbLigne -= 1
            tableauPostionBas[boucle] = tableauDeplacements[nbColonne, nbLigne]
            boucle += 1

    for deplacementBasFin in range(roomWidth // 2 - 1):
        nbColonne = roomWidth // 2 + deplacementBasFin
        nbLigne = roomWidth
        while nbColonne < roomWidth - 1 and nbLigne > 0:
            nbColonne += 1
            nbLigne -= 1
            tableauPostionBas[boucle] = tableauDeplacements[nbColonne, nbLigne]
            boucle += 1

    deuxListes = creerDeuxListes(tableauPostionHaut, tableauPostionBas, roomWidth)
    return choisirListe(roomWidth, deuxListes)

#Execution principale
def main():
    #Valable pour tout chiffre pair strictement supérieur à 0
    roomWidth = tkinterEntree("Entrez la taille de la piece", "") #On demande la valeur sous forme d'int
    while roomWidth % 2 == 1 or roomWidth <= 0:
        roomWidthPrecedent = roomWidth
        roomWidth = tkinterEntree("Entrez la taille de la piece", "La valeur ne peut pas être impaire, négative ou nulle") #Met dans la variable roomWidth la valeur peut importe si elle paire ou non
        if roomWidth == roomWidthPrecedent:
            exit()
    #La boucle s'arrête dès que la valeur est paire différente de 0 non négative
    nbPersonnes = tkinterEntree("Entrez le nombre de personnes", "")
    while nbPersonnes > roomWidth**2 or nbPersonnes <=0:
        nbPersonnesPrecedent = nbPersonnes
        nbPersonnes = tkinterEntree("Entrez le nombre de personnes", "La valeur ne peut pas être supérieure à la taille de la pièce au carré, négative ou nulle")
        if nbPersonnes == nbPersonnesPrecedent:
            exit()
    
    roomSize = roomWidth + 2 #Incrémente de 2 unités pour ajouter les murs a la pièce
    roomInt = np.array([[0]*roomSize]*roomSize) #Créé une matrice carré de la taille de la pièce
    room = np.asarray(roomInt, dtype = np.float64) #Convertit toutes les valeurs de la matrices d'int à float
    afficherFloorField(room, roomWidth) ## Fonction du Floor Field ##
    tableauDeplacements = np.array([[0]*roomWidth]*roomWidth)

    boucle = 1
    personnesSorties = 0

    if nbPersonnes <= roomWidth**2:
        while boucle <= nbPersonnes:
            coordonneeslig=np.random.randint(roomWidth)
            coordonneescol=np.random.randint(roomWidth)
            if tableauDeplacements[coordonneeslig,coordonneescol]==0:
                tableauDeplacements[coordonneeslig,coordonneescol]=boucle
                boucle += 1
    else:
        print("nbPersonnes trop grand")

    pygameAfficherPremierTableau = True

    while personnesSorties < nbPersonnes:
        if not pygameAfficherPremierTableau:
            personnesSorties = personnesSorties + mouvementDesPersonne(room, roomWidth, tableauDeplacements, nbPersonnes)
        pygameAfficherPremierTableau = False
        afficherPygame(tableauDeplacements, roomWidth, roomSize, nbPersonnes, room)
        time.sleep(0.2)
        print(tableauDeplacements)
main()