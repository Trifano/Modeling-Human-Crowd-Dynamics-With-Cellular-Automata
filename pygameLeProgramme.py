import pygame

'''
Affichage graphique

Préconditions :
    tableauDeplacements : matrice avec l'état actuel des personnes (0 : rien, 1 : une personne est sur la case)
    roomWidth : taille de la pièce sans murs
    roomSize : taille de la pièce avec murs
    nbPersonnes : nombre de personnes
    room : matrice avec FloorField
'''
def afficherPygame(tableauDeplacements, roomWidth, roomSize, nbPersonnes, room):
    global ecran
    global WHITE
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    GREY = (138, 138, 138)

    LONGEUR = 20
    HAUTEUR = 20

    MARGE = 2

    if nbPersonnes == 0:
        pygame.init()

    WINDOW_SIZE = [LONGEUR * roomSize + 2 * roomSize, HAUTEUR * roomSize + 2 * roomSize]
    ecran = pygame.display.set_mode(WINDOW_SIZE)

    pygame.display.set_caption("Array Backed Grid")
    clock = pygame.time.Clock()


    fini = False

    ecran.fill(GREY)

    while not fini:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        else:
            for analyseColonne in range(roomWidth):
                for analyseLigne in range(roomWidth):
                    color = WHITE
                    if tableauDeplacements[analyseColonne, analyseLigne] != 0:
                        color = BLACK
                    pygame.draw.rect(ecran, color, [(LONGEUR + MARGE)*(analyseLigne + 1) + MARGE, (HAUTEUR + MARGE)*(analyseColonne + 1) + MARGE, LONGEUR, HAUTEUR])
            for murEtPorteColonne in range(roomSize):
                for murEtPorteLignes in range(roomSize):
                    color = RED
                    if room[murEtPorteColonne, murEtPorteLignes] == 500 or room[murEtPorteColonne, murEtPorteLignes] == 1:
                        if room[murEtPorteColonne, murEtPorteLignes] == 1:
                            color = YELLOW
                        pygame.draw.rect(ecran, color, [(LONGEUR + MARGE)*murEtPorteLignes + MARGE, (HAUTEUR + MARGE)*murEtPorteColonne + MARGE, LONGEUR, HAUTEUR])
        clock.tick(60)
        pygame.display.flip()
        fini = True