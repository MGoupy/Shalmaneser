#pyinstaller --onefile engines/Shalmaneser.py
#Set-ExecutionPolicy Unrestricted -Scope Process
from Bot_Methodes import *
import time
from threading import Thread

class Bot():
    
    def __init__(self):
        self.profondeur=4
        
        self.attendre_jouer_coup=False
        self.isready=True

    def partie(self):
        
        while True:
            data = input()
            if "uci"in data and not "newgame" in data:
                cherche=Cherche()
                print("id name Shalmaneser")
                print("id author Maxime Goupy")
                print("uciok")
            
            elif "isready" in data:
                while not self.isready:
                    time.sleep(0.1)
                print("readyok")
                
            elif "quit" in data:
                quit()
                      
            elif "ucinewgame" in data:
                partie=Partie("") #serait bien qu"il garde trace des coup et rejoue pas tout à chaque fois
                
            elif "position" in data:
                            
                self.isready=False
                
                data=data[data.find("position")+8:]
                while data[0]==" ":
                    data=data[1:]
                    
                #Récupère la position
                if "startpos" in data:
                    partie=Partie("")
                elif "fen"in data:
                    FEN=data[:data.find("moves")-1]
                    partie=Partie(FEN[3:],True)
                else:
                    print("Erreur position envoyé au bot")
                    print("Position envoyé ="+data)
                    break
                
                #Joue les coups dans la position
                if "moves" in data:
                    data=data[data.find("moves")+5:]
                    partie=faire_moves(partie,data)
                self.isready=True
                self.attendre_jouer_coup=True
            
            elif "go" in data and self.attendre_jouer_coup:
                coup=cherche.AlphaBeta_racine(self.profondeur,partie)
                print("bestmove "+(coup))
                self.attendre_jouer_coup=False

    
if __name__ == "__main__":
    
    shalmanseser=Bot()
    shalmanseser.partie()
    
#Optimisation partie avec dico pièce