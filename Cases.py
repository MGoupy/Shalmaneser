
### Conversion entre différents systèmes
def conversion_num_alg(num):
    x=num[0]
    y=num[1]
    nom_colonnes="abcdefghg"
    c=nom_colonnes[(int)(x)]
    l=str(8-(int)(y))
    return c+l
    
def conversion_alg_num(alg):
    l=alg[1]
    c=alg[0]
    nom_colonnes="abcdefgh"
    x=str(nom_colonnes.find(c))
    y=str(8-(int)(l))
    return x+y

def conversion_num_1012(num):
    x=(int)(num[0])
    y=(int)(num[1])
    return 91+x-y*10

def conversion_1012_num(co):
    x=co%10-1
    y=9-co//10
    return (str)(x)+(str)(y)

def conversion_1012_alg(co):
    nom_colonnes="abcdefghg"
    c=nom_colonnes[co%10-1]
    l=str(co//10-1)
    return c+l

def conversion_alg_1012(alg): #refaire mieux
    c=alg[0]
    l=alg[1]
    nom_colonnes="abcdefgh"
    x=nom_colonnes.find(c)
    y=8-(int)(l)
    return 91+x-y*10
    
def conversion_coup_alg_1012(coup):
    coup=string_suppr_espaces(coup)
    if len(coup)==4:
        return [conversion_alg_1012(coup[:2]),conversion_alg_1012(coup[2:]),""]
    else:
        return [conversion_alg_1012(coup[:2]),conversion_alg_1012(coup[2:]),coup[4]] #pas propore le [2:] prend trop d'info mais bon marche

def conversion_coup_1012_alg(coup):
    return (conversion_1012_alg(coup[0])+conversion_1012_alg(coup[1])+coup[2])

def string_suppr_espaces(FEN):
    while FEN[0]==" ":
        FEN=FEN[1:]
    while FEN[len(FEN)-1]==" ":
        FEN=FEN[:len(FEN)-1]
    return(FEN)
      
### Gestion couleurs
def change_couleur(couleur):
    if couleur=="w":
        return "b"
    else:
        return "w"

def change_couleur_1012(couleur):
    if couleur==1:
        return 2
    else:
        return 1

def couleur_opp(c1,c2):
    if c1==1:
        if c2==2:
            return True
        else:
            return False
    elif c1==2:
        if c2==1:
            return True
        else:
            return False
    else:
        return False

### Listes vides préfaites
def cases_sur_plateau():
    return [21,22,23,24,25,26,27,28,31,32,33,34,35,36,37,38,41,42,43,44,45,46,47,48,51,52,53,54,55,56,57,58,61,62,63,64,65,66,67,68,71,72,73,74,75,76,77,78,81,82,83,84,85,86,87,88,91,92,93,94,95,96,97,98]

def cases_sur_plateau_ordre_inv():
    return [91,92,93,94,95,96,97,98,81,82,83,84,85,86,87,88,71,72,73,74,75,76,77,78,61,62,63,64,65,66,67,68,51,52,53,54,55,56,57,58,41,42,43,44,45,46,47,48,31,32,33,34,35,36,37,38,21,22,23,24,25,26,27,28]

def liste_vide():
    return [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

### Recupère parties du FEN
def FEN_get_position(FEN):
    return FEN[:FEN.find(" ")]

def FEN_get_couleur(FEN):
    return FEN[FEN.find(" ")+1]

def FEN_get_roque(FEN):
    FEN=FEN[FEN.find(" ")+3:]
    return FEN[:FEN.find(" ")]

def FEN_get_demicoup(FEN):
    FEN=FEN[:FEN.rfind(" ")]
    return FEN[FEN.rfind(" ")+1:]

def FEN_get_passant(FEN):
    FEN=FEN[FEN.find(" ")+1:]
    FEN=FEN[FEN.find(" ")+1:]
    FEN=FEN[FEN.find(" ")+1:]
    return(FEN[:FEN.find(" ")])
    
    
def FEN_get_coup(FEN):
    return FEN[FEN.rfind(" ")+1:]

### Tests

if __name__ == "__main__":
    liste=[5,4,3]
    print(len(liste))
