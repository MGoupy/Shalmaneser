from Cases import *
from Mouvements import *

class Piece:
    
    def __init__(self,type,x,y):
        if type.isupper():
            self.couleur="w"
        else:
            self.couleur="b"
        self.type=type.lower()
        self.x=x
        self.y=y
        self.id="@"+str(x)+str(y)

    def __bool__(self): #Toute pièce qui existe à une valeur boolenne de True
        return True
    
    def __str__(self):
        if self.couleur=="w":
            return self.type.upper()
        else:
            return self.type


def cherche_piece(x,y,table):
    return table[x][y]

def table_pieces(FEN):
    table_pieces=[]
    for i in range(8):
        table_pieces.append([""] * 8)
    i=1
    while i<65:
        if FEN[0]=="/":
            FEN=FEN[1:]
        elif FEN[0].isnumeric():
            i+=(int)(FEN[0])
            FEN=FEN[1:]
        else:
            table_pieces[(i-1)%8][(i-1)//8]=Piece(FEN[0],(i-1)%8,(i-1)//8)
            FEN=FEN[1:]
            i+=1
    return table_pieces