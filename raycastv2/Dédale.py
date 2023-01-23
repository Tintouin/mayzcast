#Imports
from random import randint
from tkinter import *
from Arianne import *
from Minos import main

info = "Programme écrit pour le cours de NSI de Mr. Toulouse par Clément ESTREM, Titouan MICHAUD, Kilian ROCHE-RODRIGUEZ, Thibaut ROSA. \
    \n Le programme d'exploration à été écrit à l'origine par https://twitter.com/Net_Skeleton et voici son lien GitHub : https://github.com/bloodocean7/Python-Raycasting-Engine-Project"
infobugs = "    1- Il est possible que le programme génère une graine de monde qui ne fonctionne pas,\
plus la taille du labyrinthe est grande moins les chances d'obtenir une de ces maps sont grandes,\n\
nous ne savons pas réelement comment régler ce problème, mais il semblerait qu'il arrive lorsque l'une des deux composantes de la graine sont nulles,\
ou les deux. \nSi c'est le cas les chances sont donc de 1/taille de la map+1 ou de (1/taille de la map+1)² bref assez minoritaires dans les deux cas relativement à la taille de la map...\n\
Parfois générer une solution fait planter le script, c'est qu'il n'existe pas de passage possible vers la sortie parce que l'entrée ou la sortie sont obstruées.\n\
Pour résoudre ces problèmes, relancez le programme.    \n\n\
    2- La map peut être mal générée, c'est du à des graines très précises qu'on ne peut pas vraiment prévoir. \nD'autres peuvent montrer des signes étranges, \
il n'y a rien à interpréter aucun fantôme qui hante le programme seulement du bruit informatique, \ntoutes images percues dans nos labyrinthes sont le produit d'une paréidolie https://fr.wikipedia.org/wiki/Paréidolie \n\n\
    3- Le problème le plus facile à reproduire et pourtant le plus difficile à résoudre est un bug dans le module Minos,\n\
lorsqu'on génère la solution de la map et que l'on veut jouer dessus, \
cela ne fonctionne pas...\nC'est une erreur absurde car en théorie Arianne et Minos n'intéragissent pas du tout ensemble, \
\nil semblerait qu'il s'agisse d'un problème lié à l'activité de la fenêtre tkinter, mais après différents test rien ne change.\n\
Quant à la console elle indique un problème avec le module numba (qui nous permet de rendre les calculs bien plus rapides pour le raycast),\n\
numba indique que ce qu'on essaye d'utiliser n'est pas une variable np.array, or c'en est bien une vous pouvez aller vérifier. \
\nEn fait c'est une erreur du côté de numba comme semble l'indiquer ce rapport sur GitHub : https://github.com/lmcinnes/umap/issues/392"

#Initialisation et conventions
root = Tk()
root.geometry("800x800")
root.resizable(False,False)
canvas = Canvas(root, width=800, height=800)
canvas.pack()

taille=30
t_cell=800/taille
visited_cells = []
walls = []

#Création aléatoire de la map
map = [[1 for _ in range(taille)]for _ in range(taille)]

def check_neighbours(ccr, ccc):
    """Fonction qui regarde chacune de ses voisines pour génerer le labyrinthe"""
    neighbours = [[ccr, ccc-1, ccr-1, ccc-2, ccr, ccc-2, ccr+1, ccc-2, ccr-1, ccc-1, ccr+1, ccc-1], #gauche
                [ccr, ccc+1, ccr-1, ccc+2, ccr, ccc+2, ccr+1, ccc+2, ccr-1, ccc+1, ccr+1, ccc+1], #droite
                [ccr-1, ccc, ccr-2, ccc-1, ccr-2, ccc, ccr-2, ccc+1, ccr-1, ccc-1, ccr-1, ccc+1], #haut
                [ccr+1, ccc, ccr+2, ccc-1, ccr+2, ccc, ccr+2, ccc+1, ccr+1, ccc-1, ccr+1, ccc+1]] #bas
    visitable_neighbours = []           
    for i in neighbours:                                                                        #cherche des voisines à visiter
        if i[0] > 0 and i[0] < (taille-1) and i[1] > 0 and i[1] < (taille-1):
            if map[i[2]][i[3]] == 0 or map[i[4]][i[5]] == 0 or map[i[6]][i[7]] == 0 or map[i[8]][i[9]] == 0 or map[i[10]][i[11]] == 0:
                walls.append(i[0:2])                                                                                               
            else:
                visitable_neighbours.append(i[0:2])
    return visitable_neighbours


#Détermination de la graine
scr = randint(1, taille)
scc = randint(1, taille)

ccr, ccc = scr, scc

map[ccr][ccc] = 0
finished = False
while not finished:
    visitable_neighbours = check_neighbours(ccr, ccc)
    if len(visitable_neighbours) != 0:
        d = randint(1, len(visitable_neighbours))-1
        ncr, ncc = visitable_neighbours[d]
        map[ncr][ncc] = 0
        visited_cells.append([ncr, ncc])
        ccr, ccc = ncr, ncc
    if len(visitable_neighbours) == 0:
        try:
            ccr, ccc = visited_cells.pop()
        except:
            finished = True

map1=[]
for i in range(taille):
    map1.append((map[i]))

#Définition des ponts clés entrée et sortie toujours respectivement dans les coins supérieur gauche et inférieur droit
map[1][1]=2
map[1][2]=0
map[taille-2][taille-2]=3


print(map1)



# print(solution(map1))
def draw_map():
    """Fonction qui dessine seulement la map"""
    col=0
    row=0
    x=0
    y=0
    for j in range(taille):
        for i in range(taille):
            if map1[row][col] == 1:
                canvas.create_rectangle(x,y,x+t_cell,y+t_cell, fill='black')
                col+=1
                x+=t_cell
            elif map1[row][col] == 2:
                canvas.create_rectangle(x,y,x+t_cell,y+t_cell, fill='green')
                col+=1
                x+=t_cell
            elif map1[row][col] == 3:
                canvas.create_rectangle(x,y,x+t_cell,y+t_cell, fill='red')
                col+=1
                x+=t_cell   
            else:
                col+=1
                x+=t_cell
       
        col=0
        x=0
        y+=t_cell
        row+=1             

draw_map()

#Petite fonction toute simple qui retire le 2 et le 3 invalides pour le format de map de Minos
def adaptmap(damap=map1):
    col=0
    row=0
    newmap=[]
    r=[]
    for j in range(len(damap)):
        for i in range(len(damap[0])):
        
            if damap[row][col] == 0 or damap[row][col] == 2 or damap[row][col] == 3:
                r.append(0)
            elif damap[row][col] == 1:
                r.append(1) 
            col+=1       
        newmap.append(r)
        r=[]
        row+=1
        col=0   
    print(newmap)
    return newmap 

#Touches sur tkinter
def keys(event):
    if event.char=="r":
        solution(map1,canvas,t_cell)
    if event.char=="e":
        main(adaptmap(),taille) 
    if event.char=="i":
        print("\n\nInformations générales : \n\n",info,"\n\nInformation liées aux bogues et limites : \n\n",infobugs)       


root.bind("<Key>", keys)
print("Mémorisez ce plan, vous pourrez l'explorer avec E. \n R : Solution \n E : Exploration \n I : Plus d'infos...")
root.mainloop()