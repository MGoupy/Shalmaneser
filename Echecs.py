import tkinter as tk 

from Fenetre_Jeu import *
from Serveur import *

class Menu(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Menu")
        self.zone_boutons=tk.Canvas(self)
        self.zone_boutons.pack()
        self.bouton_2joueurs=tk.Button(self.zone_boutons,text="Jouer à deux joueurs", width=40,height=5, bd="10",command=self.partie_deux_joueurs)
        self.bouton_2joueurs.pack()
        self.bouton_blanc=tk.Button(self.zone_boutons,text="Jouer blanc contre l'ordinateur", width=40,height=5, bd="10",command=self.partie_blanc)
        self.bouton_blanc.pack()
        self.bouton_noir=tk.Button(self.zone_boutons,text="Jouer noirs contre l'ordinateur", width=40,height=5, bd="10",command=self.partie_noirs)
        self.bouton_noir.pack()
        self.bouton_2bots=tk.Button(self.zone_boutons,text="Laisser deux ordinateurs jouer entre eux", width=40,height=5, bd="10",command=self.partie_deux_bots)
        self.bouton_2bots.pack()
        
        #Lance serveur
        self.serveur=Serveur()
        thread_jeu = Thread(target=self.lancer_partie)
        thread_jeu.daemon = True
        thread_jeu.start()
        
    def partie_deux_joueurs(self):
        self.fenetre_jeu=Fenetre(self.fermer_fenetre,self.fermer_fenetre_tout)
        self.serveur.def_joueurs(["h","h"])
        self.withdraw()
    
    def partie_blanc(self):
        self.fenetre_jeu=Fenetre(self.fermer_fenetre,self.fermer_fenetre_tout)
        self.serveur.def_joueurs(["h","b"])
        self.withdraw()
        
    def partie_noirs(self):
        self.fenetre_jeu=Fenetre(self.fermer_fenetre,self.fermer_fenetre_tout)
        self.serveur.def_joueurs(["b","h"])
        self.withdraw()
    
    def partie_deux_bots(self):
        self.fenetre_jeu=Fenetre(self.fermer_fenetre,self.fermer_fenetre_tout)
        self.serveur.def_joueurs(["b","b"])
        self.withdraw()
    
    def fermer_fenetre(self):
        self.fenetre_jeu.destroy()
        self.deiconify()
        self.mainloop()
    
    def fermer_fenetre_tout(self):
        self.fenetre_jeu.destroy()
        self.destroy()
        
    def lancer_partie(self):
        self.serveur.partie()
        
if __name__ == "__main__":
    menu=Menu()
    menu.mainloop()
    
########################################
#A faire


#Mettre tous déplacement dans partie et avoir une liste des coordonées des pieces noirs et blanches
#solution pas check en passant et roque tt le temps
#optimisations
    #multiprocesseur
#nulle par manque matériel
#serveur dans classe propre
#fermer toutes fenetres ensemble
#régler erreur quand ferme fenetre
#Interface
    #Contour
    #Redimentionnement
    #Page lancement mieux
    #Page fin mieux
    #Liste coups
#Exportation PNG
#IA
    #Intervface UCI finir
    #Evaluation position mieux
    #chercher séquences captures jusqu'au bout
    #garder principale variation
#Multijoueurs
#Instalateur
    
#Cree Fichier exe
#pyinstaller --onefile Echecs.py