from Pieces import *

##### Gestion du FEN #####

def string_vide(s):
    vide=True
    for i in range(len(s)):
        if s[i] != " ":
            vide = False
            break
    return vide
    
def FEN_update_position(liste_pieces,liste_couleurs):

    nouveauFEN_position=""
    symboles_FEN={
    1: "P",
    2: "p",
    3: "n",
    4: "b",
    5: "r",
    6: "q",
    7: "k"
    }
    for i in cases_sur_plateau_ordre_inv():
        piece=liste_pieces[i]
        couleur=liste_couleurs[i]
        if piece!=0:
            if couleur==1:
                nouveauFEN_position+=symboles_FEN[piece].upper()
            else:
                nouveauFEN_position+=symboles_FEN[piece]
        else:
            if nouveauFEN_position =="":
                nouveauFEN_position+="1"
            elif nouveauFEN_position[len(nouveauFEN_position)-1].isnumeric():
                nouveauFEN_position=nouveauFEN_position[:len(nouveauFEN_position)-1]+str((int)(nouveauFEN_position[len(nouveauFEN_position)-1])+1)
            else:
                nouveauFEN_position+="1"
        if i%10==8:
            nouveauFEN_position+="/"
    return nouveauFEN_position[:len(nouveauFEN_position)-1]


def listes_from_FEN(FEN):
    liste_pieces=liste_vide()
    liste_couleurs=liste_vide()
    i=0
    while i<64:
        if FEN[0].isnumeric():
            i+=(int)(FEN[0])
            FEN=FEN[1:]
        else:
            if FEN[0]=="P":
                piece=1
                couleur=1
            elif FEN[0]=="p":
                piece=2
                couleur=2
            elif FEN[0]=="N":
                piece=3
                couleur=1
            elif FEN[0]=="n":
                piece=3
                couleur=2
            elif FEN[0]=="B":
                piece=4
                couleur=1
            elif FEN[0]=="b":
                piece=4
                couleur=2
            elif FEN[0]=="R":
                piece=5
                couleur=1
            elif FEN[0]=="r":
                piece=5
                couleur=2
            elif FEN[0]=="Q":
                piece=6
                couleur=1
            elif FEN[0]=="q":
                piece=6
                couleur=2
            elif FEN[0]=="K":
                piece=7
                couleur=1
            elif FEN[0]=="k":
                piece=7
                couleur=2
            liste_pieces[98-(7-i%8)-10*(i//8)]=piece
            liste_couleurs[98-(7-i%8)-10*(i//8)]=couleur
            FEN=FEN[1:]
            i+=1
        if FEN[0]=="/":
            FEN=FEN[1:]
    return[liste_pieces,liste_couleurs]

def valeur_piece(piece):
    if piece==0:
        return 0
    if piece==1 or piece==2:
        return 1
    if piece==3:
        return 3
    if piece==4:
        return 3
    if piece==5:
        return 5
    if piece==6:
        return 9
    if piece==7:
        return 12
    print("valeur bizzare pièce de type :"+(str)(piece))

def valeur_mouvement(piece,co,couleur):
    if piece==0:
        return 0-0.01*(couleur*2-3)*co
    if piece==1 or piece==2:
        return 1-0.01*(couleur*2-3)*co
    if piece==3:
        return 3-0.01*(couleur*2-3)*co
    if piece==4:
        return 4-0.01*(couleur*2-3)*co
    if piece==5:
        return 5-0.01*(couleur*2-3)*co
    if piece==6:
        return 9-0.01*(couleur*2-3)*co
    if piece==7:
        return 12-0.01*(couleur*2-3)*co
    print("valeur bizzare pièce de type :"+(str)(piece))