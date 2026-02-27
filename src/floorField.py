######################## Floor Field ########################

'''
Créer le FloorField pour la partie supérieure de la matrice

Préconditions: 
    arrayUse : Matrice vide
    roomWidth : Taille de la pièce
Postconditions:
    Champ scalaire avec des valeurs plus importantes en s'éloignant de la sortie
'''
def setupFloorField(arrayUse, roomWidth):
    nouvelleValeurColonne = 0 
    #Variable qui va être incrémenter plus tard sauf pour la première ligne, elle permet de se déplacer en fonction des lignes sur le tableau
    for nbColonnes in range(roomWidth//2):
        incrementation = 0 
        # Cette variable permet d'incrémenter les première colonnes du tableau de 0.5. 
        # Par exemple 1 case première ligne, 2 case deuxième ligne, 3 case troisème ligne...
        valeurActuelle = 1 + nouvelleValeurColonne #Permet d'incrémenter chaque premier élément de chaque ligne de 1
        incrementation = nbColonnes #On définit cette fonction pour pouvoir la modifier sans modifier nbColonnes
        conditionNouvelleValeurColonne = False #Condition pour incrémenter chaquer premier élément de chaque ligne de 1 une seule fois 
        for nbLignes in range(roomWidth):
            #Augmente de 0.5 sauf la première ligne quand incrementation est sur la deuxieme ligne ou plus
            if incrementation >= 1:
                #Comme la variable valeurActuelle = valeurActuelle + 1 n'est pas modifié dans la condition incrementation >= 1
                #On augmente les valeurs en fonction des lignes, on augmente manuellement de 1 pour une seule itération, ici le premier cas
                if nbLignes == 0:
                    valeurActuelle = valeurActuelle + 1
                valeurActuelle = valeurActuelle + 0.5 #On incremente la valeur de 0.5 uniquement pour les premieres cases, (explication ligne 7)
                arrayUse[roomWidth//2-nbColonnes,nbLignes+1] = valeurActuelle 
                #Change la case du tableau en partant du mileu du nombre choisi et remontant de un en un 
                #(grâce à -nbColonnes) tout en excluant les murs
                incrementation = incrementation-1 
                #On augmente incrementation avant pour chaque ligne mais on ne veut pas aller jusqu'à la fin de ligne
                #Car on sort du tableau, donc on diminue de 1 en 1.
                #Par exemple pour la deuxième ligne incrementation = 1 donc une seule case sera augmenté de 0.5 au lieu de 1
                #Pour la troisième ligne c'est deux case qui seront augmenté et ainsi de suite jusqu'au mur
                conditionNouvelleValeurColonne = True 
                #La condition se met à jour une seule fois comme ça nous pouvons modifier uniquement la première colonne
            #Sinon dans les autres cas incrémenter de 1 au lieu de 0.5
            else:
                valeurActuelle = valeurActuelle + 1
                arrayUse[roomWidth//2-nbColonnes,nbLignes+1] = valeurActuelle 
                #La valeur pour la partie supérieure du tableau est changé à valeurActuelle
        if conditionNouvelleValeurColonne:
            nouvelleValeurColonne = nouvelleValeurColonne + 1 #Si la condition est vérifié incrémenter de 1

#Même partie que la précédente mais pour la partie inférieure
def setupFloorFieldPartieInferieure(arrayUse, roomWidth):
    nouvelleValeurColonne = 0
    for nbColonnes in range(roomWidth//2):
        incrementation = 0
        valeurActuelle = 1 + nouvelleValeurColonne
        incrementation = nbColonnes
        conditionNouvelleValeurColonne = False
        for nbLignes in range(roomWidth):
            if incrementation >= 1:
                if nbLignes == 0:
                    valeurActuelle = valeurActuelle + 1
                valeurActuelle = valeurActuelle + 0.5
                #La condition -nbColonnes devient +nbColonnes 
                #Incrémente du milieu vers le bas et incrémenter roomWitdth de 1 pour ne pas superposer les deux fonctions
                arrayUse[roomWidth//2+1+nbColonnes,nbLignes+1] = valeurActuelle
                incrementation = incrementation-1
                conditionNouvelleValeurColonne = True
            else:
                valeurActuelle = valeurActuelle + 1
                arrayUse[roomWidth//2+1+nbColonnes,nbLignes+1] = valeurActuelle
        if conditionNouvelleValeurColonne:
            nouvelleValeurColonne = nouvelleValeurColonne + 1

'''
Permet de fixer tous les côtés à la valeur "500"

Préconditions:
    arrayMurs : Matrice remplie sans murs
    roomWidth : Taille de la pièce
Postconditions:
    Matrice avec murs
'''
def afficherMurs(arrayMurs, roomWidth):
    #Ces boucles pour les côtés gauche et droite
    for ligneCotes in range (roomWidth+2):
        arrayMurs[ligneCotes, 0] = 500
        arrayMurs[ligneCotes, roomWidth+1] = 500
    #Et celle-ci fait le haut et le bas
    for ligneHautEtBas in range (roomWidth+2):
        arrayMurs[0, ligneHautEtBas] = 500
        arrayMurs[roomWidth+1, ligneHautEtBas] = 500

#Cette fonction met la porte de sortie au milieu gauche du tableau
def porteDeSortie(leTableau, roomWidth):
    leTableau[roomWidth//2, 0] = 1
    leTableau[roomWidth//2+1, 0] = 1

#Cette fonction permet de rassembler les 4 fonctions en une seule
def afficherFloorField(room, roomWidth):
    setupFloorField(room, roomWidth)
    setupFloorFieldPartieInferieure(room, roomWidth)
    afficherMurs(room, roomWidth)
    porteDeSortie(room, roomWidth)

######################## Floor Field ########################