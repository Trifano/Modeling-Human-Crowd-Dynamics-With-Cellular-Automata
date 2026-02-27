import numpy as np
import matplotlib.pyplot as plt # type: ignore
import matplotlib.animation as animation # type: ignore
import random

TAILLE_GRILLE = (20, 20)
POSITION_SORTIE = (19, 10)
DECROISSANCE = 0.5
NOMBRE_AUTOMATES = 30
NOMBRE_ETAPES = 50

TYPES_AUTOMATES = ["passif", "normal", "presse"]
PRIORITE_AUTOMATES = {"passif": 0, "normal": 1, "presse": 2}

def creer_champ_potentiel(taille, position_sortie, decroissance):
    champ = np.zeros(taille)
    for i in range(taille[0]):
        for j in range(taille[1]):
            distance = np.sqrt((i - position_sortie[0])**2 + (j - position_sortie[1])**2)
            champ[i, j] = np.exp(-decroissance * distance)
    return champ

def generer_obstacles(taille, pourcentage=0.1):
    obstacles = np.zeros(taille, dtype=bool)
    nombre_obstacles = int(taille[0] * taille[1] * pourcentage)
    indices = np.random.choice(taille[0] * taille[1], nombre_obstacles, replace=False)
    for index in indices:
        x, y = divmod(index, taille[1])
        obstacles[x, y] = True
    obstacles[POSITION_SORTIE] = False
    return obstacles

def initialiser_automates(nombre, taille, obstacles):
    automates = []
    positions_occupees = {}

    while len(automates) < nombre:
        x, y = np.random.randint(0, taille[0]), np.random.randint(0, taille[1])
        if not obstacles[x, y] and (x, y) not in positions_occupees:
            type_automate = random.choice(TYPES_AUTOMATES)
            automates.append([x, y, type_automate])
            positions_occupees[(x, y)] = type_automate

    return np.array(automates, dtype=object)

def deplacer_automates(automates, champ_potentiel, obstacles):
    nouvelles_positions = {}
    
    for i in range(len(automates)):
        x, y, type_automate = automates[i]

        if (x, y) == POSITION_SORTIE:
            nouvelles_positions[(x, y)] = type_automate
            continue

        voisins = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        voisins = [(nx, ny) for nx, ny in voisins
                   if 0 <= nx < TAILLE_GRILLE[0] and 0 <= ny < TAILLE_GRILLE[1]
                   and not obstacles[nx, ny]]

        if not voisins:
            nouvelles_positions[(x, y)] = type_automate
            continue

        meilleur_deplacement = max(voisins, key=lambda pos: champ_potentiel[pos])

        if meilleur_deplacement in nouvelles_positions:
            type_existant = nouvelles_positions[meilleur_deplacement]
            if PRIORITE_AUTOMATES[type_automate] > PRIORITE_AUTOMATES[type_existant]:
                nouvelles_positions[(x, y)] = type_existant 
                nouvelles_positions[meilleur_deplacement] = type_automate
            else:
                nouvelles_positions[(x, y)] = type_automate
        else:
            nouvelles_positions[meilleur_deplacement] = type_automate

    return np.array([[pos[0], pos[1], nouvelles_positions[pos]] for pos in nouvelles_positions], dtype=object)

def mettre_a_jour(frame):
    global automates

    automates[:] = deplacer_automates(automates, champ_potentiel, obstacles)

    axe.clear()
    axe.imshow(champ_potentiel, cmap="hot", origin="lower", alpha=0.6)
    axe.imshow(obstacles, cmap="gray", origin="lower", alpha=0.8)

    couleurs = {'passif': 'yellow', 'normal': 'blue', 'presse': 'red'}
    for x, y, type_automate in automates:
        axe.scatter(y, x, color=couleurs[type_automate], label=type_automate if frame == 0 else "")

    axe.scatter(POSITION_SORTIE[1], POSITION_SORTIE[0], color='green', marker="*", s=100, label="Sortie")
    axe.set_title(f"Étape de simulation {frame}")
    axe.legend()

champ_potentiel = creer_champ_potentiel(TAILLE_GRILLE, POSITION_SORTIE, DECROISSANCE)
obstacles = generer_obstacles(TAILLE_GRILLE)
automates = initialiser_automates(NOMBRE_AUTOMATES, TAILLE_GRILLE, obstacles)

fig, axe = plt.subplots(figsize=(6, 6))
animation_simulation = animation.FuncAnimation(fig, mettre_a_jour, frames=NOMBRE_ETAPES, interval=300)

plt.show()