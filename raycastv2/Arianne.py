from tkinter import *


def est_valide(i, j, n, m):
    return  0 <= i <= n-1 and 0 <= j <= m-1

def depart(lab):
    """fonction qui indique le depart du labyrinthe"""
    n = len(lab)
    m = len(lab[0])
    for row in range(0,n):
        for colonne in range(0,m):
            if lab[row][colonne] == 2:
                return (row, colonne)

def nb_cases_vides(lab):
    """fonction qui indique si la case choisi est vide"""
    n = len(lab)
    m = len(lab[0])
    compteur = 0
    for row in range(0,n):
        for colonne in range(0,m):
            if lab[row][colonne] in (0, 2, 3):
                compteur += 1
    return compteur              


def voisines(i, j, lab):
    """fonction qui vérifie les cases voisines"""
    n = len(lab)
    m = len(lab[0])
    voisins = [(i,j-1), (i-1,j), (i+1,j), (i, j+1)]
    voisins_valides = [x for x in voisins if est_valide(x[0], x[1], n, m)]
    return  [x for x in voisins_valides if lab[x[0]][x[1]] != 1 and lab[x[0]][x[1]] != 4]


def solution(lab,canvas,t_cell):
    case = depart(lab)
    chemin = [case]
    i, j = case[0], case[1]
    while lab[i][j] != 3:
        lab[i][j] = 4
        voisinage = voisines(i, j, lab)
        if voisinage != [] :
            chemin.append(voisinage[0])
        else:
            chemin.pop()
        # mise à jour de la prochaine case à visiter:
        case = chemin[-1]
        i, j = case[0], case[1]
    print(chemin)
    liste=[x for elem in chemin for x in elem]
    print(liste)
    i=1
    j=0
    for m in range(len(chemin)):
        x=liste[i]
        y=liste[j]
        canvas.create_rectangle(x*t_cell,y*t_cell,x*t_cell+t_cell,y*t_cell+t_cell, fill='blue')
        i+=2
        j+=2


