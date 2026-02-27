from tkinter import *
from tkinter import ttk

def afficherText():
    global nombre
    nombre = entree.get()
    nombre = int(nombre)

'''
Affichage graphique des saisies de l'utilisateur

Préconditions :
    texteAfficher : texte à afficher
    siErreur : valeure max
Postconditions :
    Renvoie le nombre de personnes choisies par l'utilisateur
'''
def tkinterEntree(texteAfficher, siErreur):    
    global entree

    fenetre = Tk()

    fenetre.geometry("600x230")
    if len(siErreur) > 10:
        fenetre.geometry("900x230")

    label=Label(fenetre, text=texteAfficher, font=("Helvetica 16"))
    label.pack(pady = 20)
    label2=Label(fenetre, text=siErreur, font=("Helvetica 16"))
    label2.pack()

    entree = Entry(fenetre, width = 40)
    entree.focus_set()
    entree.pack(pady = 10)

    ttk.Button(fenetre, text= "Valider",width= 20, command= lambda:[afficherText(), fenetre.destroy()]).pack(pady=20)

    fenetre.mainloop()

    return nombre
        