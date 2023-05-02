from Cases import *
import time
def mouvements_pseudo_legaux(liste_pieces,liste_couleurs,co,FEN):

    mouvements_capture=[]
    mouvements_silencieux=[]
    roques=FEN_get_roque(FEN)
    
    couleur_piece=liste_couleurs[co]
    piece=liste_pieces[co]
    
    if FEN[FEN.find(" ")+1]=="w":
        couleur_FEN=1
    else:
        couleur_FEN=2
    
    
    # Mouvements pion blanc
    if piece==1:
        if not liste_pieces[co+10]:
            mouvements_silencieux.append(co+10)
            if co//10==3 and not liste_pieces[co+20]:
                mouvements_silencieux.append(co+20)
        if liste_couleurs[co+11]==2:
            mouvements_capture.append(co+11)
        if liste_couleurs[co+9]==2:
            mouvements_capture.append(co+9)
        if co//10==6:
            if liste_pieces[co+11]!=-1:
                if conversion_1012_alg(co+11) in FEN_get_passant(FEN):
                    mouvements_capture.append(co+11)
            elif liste_pieces[co+9]!=-1:
                if conversion_1012_alg(co+9) in FEN_get_passant(FEN):
                    mouvements_capture.append(co+9)
                
    # Mouvements pion noir
    elif piece==2:      
        if not liste_pieces[co-10]:
            mouvements_silencieux.append(co-10)
            if co//10==8 and not liste_pieces[co-20]:
                mouvements_silencieux.append(co-20)
        if liste_couleurs[co-11]==1:
            mouvements_capture.append(co-11)
        if liste_couleurs[co-9]==1:
            mouvements_capture.append(co-9)
        if co//10==5:
            if liste_pieces[co-11]!=-1:
                if conversion_1012_alg(co-11) in FEN_get_passant(FEN):
                    mouvements_capture.append(co-11)
            if liste_pieces[co-9]!=-1:      
                if conversion_1012_alg(co-9) in FEN_get_passant(FEN):
                    mouvements_capture.append(co-9)

    # Mouvements cavalier   
    elif piece==3:
        possibilites=[-21,-19,-12,-8,8,12,19,21]
        for p in possibilites:
            if liste_pieces[co+p]==0:
                mouvements_silencieux.append(co+p)
            elif couleur_opp(liste_couleurs[co+p],couleur_piece):
                mouvements_capture.append(co+p)
    # Mouvements fou
    elif piece==4:
        directions=[-11,-9,9,11]
        for d in directions:
            mouvements=mouvements_lignes(co,couleur_piece,d,liste_couleurs)
            mouvements_capture += mouvements[0]
            mouvements_silencieux += mouvements[1]
    # Mouvements tour
    elif piece==5:
        directions=[-10,-1,1,10]
        for d in directions:
            mouvements=mouvements_lignes(co,couleur_piece,d,liste_couleurs)
            mouvements_capture += mouvements[0]
            mouvements_silencieux += mouvements[1]
    # Mouvements dame
    elif piece==6:
        directions=[-10,-1,1,10,-11,-9,9,11]
        for d in directions:
            mouvements=mouvements_lignes(co,couleur_piece,d,liste_couleurs)
            mouvements_capture += mouvements[0]
            mouvements_silencieux += mouvements[1]     
    # Mouvements roi
    elif piece==7:
        possibilites=[-10,-1,1,10,-11,-9,9,11]
        for p in possibilites:
            if liste_couleurs[co+p]!=-1:
                if not cherche_echec_case(liste_pieces,liste_couleurs,couleur_piece,co+p):
                    if liste_pieces[co+p]==0:
                        mouvements_silencieux.append(co+p)
                    elif couleur_opp(liste_couleurs[co+p],couleur_piece):
                        mouvements_capture.append(co+p)
        if roques!="-":
            if couleur_piece==couleur_FEN:
                if  not cherche_echec_case(liste_pieces,liste_couleurs,couleur_piece,co):#Roques
                    if couleur_piece==1 and "K" in roques and liste_pieces[co+1]==0 and liste_pieces[co+2]==0:
                        if not cherche_echec_case(liste_pieces,liste_couleurs,couleur_piece,co+2):
                            mouvements_silencieux.append(co+2)
                    if couleur_piece==1 and "Q" in roques and liste_pieces[co-1]==0 and liste_pieces[co-2]==0 and liste_pieces[co-3]==0:
                        if not cherche_echec_case(liste_pieces,liste_couleurs,couleur_piece,co-2):
                            mouvements_silencieux.append(co-2)
                    if couleur_piece==2 and "k" in roques and liste_pieces[co+1]==0 and liste_pieces[co+2]==0:
                        if not cherche_echec_case(liste_pieces,liste_couleurs,couleur_piece,co+2):
                            mouvements_silencieux.append(co+2)
                    if couleur_piece==2 and "q" in roques and liste_pieces[co-1]==0 and liste_pieces[co-2]==0 and liste_pieces[co-3]==0:
                        if not cherche_echec_case(liste_pieces,liste_couleurs,couleur_piece,co-2):
                            mouvements_silencieux.append(co-2)
    return [mouvements_capture,mouvements_silencieux]

def mouvements_lignes(co,couleur,direction,liste_couleurs):
    mouvements_silencieux=[]
    mouvements_capture=[]
    case=co+direction
    while liste_couleurs[case] != -1:
        if liste_couleurs[case] == 0:
            mouvements_silencieux.append(case)
        elif couleur_opp(liste_couleurs[case],couleur):
            mouvements_capture.append(case)
            return [mouvements_capture,mouvements_silencieux]
        else:
            return [mouvements_capture,mouvements_silencieux]
        case += direction
    return [mouvements_capture,mouvements_silencieux]

def cherche_echec_case(liste_pieces,liste_couleurs,couleur_en_echec,co):
    co_roi=co
    if couleur_en_echec==1:
        if liste_pieces[co+11]==2 or liste_pieces[co+9]==2:
            return True
    else:
        if liste_pieces[co-11]==1 or liste_pieces[co-9]==1:
            return True
    for d in [11,9,-9,-11]:
        if recherche_echec_direction(liste_pieces,liste_couleurs,d,4,6,co_roi,couleur_en_echec):
            return True
    for d in [10,1,-1,-10]:
        if recherche_echec_direction(liste_pieces,liste_couleurs,d,5,6,co_roi,couleur_en_echec):
            return True
    for p in [-21,-19,-12,-8,8,12,19,21]:
        if liste_pieces[co+p]==3 and liste_couleurs[co+p]!=couleur_en_echec:
            return True
    for d in [11,10,9,1,-1,-11,-10,-9]:
        if liste_pieces[co+d]==7 and liste_couleurs[co+d]!=couleur_en_echec:
            return True
    return False

def recherche_echec_direction(liste_pieces,liste_couleurs,direction,p1,p2,co,couleur):
    co+=direction
    while liste_pieces[co]!=-1:
        if (liste_pieces[co]==p1 and liste_couleurs[co]!=couleur) or (liste_pieces[co]==p2 and liste_couleurs[co]!=couleur) :
            return True
        elif(liste_pieces[co]!=0):
            return False
        co+=direction
    return False

def danger_roi(liste_pieces,liste_couleurs,couleur,FEN,dico):
    co_roi=dico[7][0]
    
    for d in [11,9,-9,-11]:
        if recherche_clouage_ou_echec(liste_pieces,liste_couleurs,d,4,6,co_roi,couleur):
            return True
    for d in [10,1,-1,-10]:
        if recherche_clouage_ou_echec(liste_pieces,liste_couleurs,d,5,6,co_roi,couleur):
            return True
    for p in [-21,-19,-12,-8,8,12,19,21]:
        if liste_pieces[co_roi+p]==3 and liste_couleurs[co_roi+p]!=couleur:
            return True
    if couleur==1:
        if liste_pieces[co_roi+11]==2 or liste_pieces[co_roi+9]==2:
            return True
    else:
        if liste_pieces[co_roi-11]==1 or liste_pieces[co_roi-9]==1:
            return True
    return False

def recherche_clouage_ou_echec(liste_pieces,liste_couleurs,direction,p1,p2,co,couleur):
    bloqueur=0
    co+=direction
    while liste_pieces[co]!=-1:
        if liste_couleurs[co]!=0:
            if (liste_pieces[co]==p1 and liste_couleurs[co]!=couleur) or (liste_pieces[co]==p2 and liste_couleurs[co]!=couleur) :
                return True
            elif(liste_couleurs[co]==couleur):
                bloqueur+=1
                if bloqueur==2:
                    return False
            else:
                return False
        co+=direction
    return False

def enlever_mouvements_illegaux(cod,mouvements,liste_pieces,liste_couleurs,FEN,dico):
    return list(filter(lambda coup: coup_met_pas_en_echec(cod,coup,liste_pieces, liste_couleurs, FEN,dico), mouvements))

def coup_met_pas_en_echec(cod,m,liste_pieces,liste_couleurs,FEN,dico):
    couleur_piece=liste_couleurs[cod]
    piece=liste_pieces[cod]
    if piece!=7:
        co_roi=dico[7][0]
    else:
        co_roi=m
    nouvelles_listes=bouge_piece_listes(cod,m,liste_pieces,liste_couleurs)
    nouvelle_liste_pieces=nouvelles_listes[0]
    nouvelle_liste_couleurs=nouvelles_listes[1]
    if cherche_echec_case(nouvelle_liste_pieces,nouvelle_liste_couleurs,couleur_piece,co_roi):
        return False
    elif piece==7 and abs(cod-m)==2:
        nouvelles_listes=bouge_piece_listes(cod,(int)((m+cod)/2),liste_pieces,liste_couleurs)
        nouvelle_liste_pieces=nouvelles_listes[0]
        nouvelle_liste_couleurs=nouvelles_listes[1]
        if cherche_echec_case(nouvelle_liste_pieces,nouvelle_liste_couleurs,couleur_piece,(int)((m+cod)/2)):
           return False
    return True
    
def bouge_piece_listes(cod,cof,ancienne_liste_pieces,ancienne_liste_couleurs):

    nouv_p=ancienne_liste_pieces.copy()
    nouv_c=ancienne_liste_couleurs.copy()
    
    piece=ancienne_liste_pieces[cod]
    couleur=ancienne_liste_couleurs[cod]
    nouv_p[cod]=0
    nouv_c[cod]=0
    
    nouv_p[cof]=piece
    nouv_c[cof]=couleur
    
    return[nouv_p,nouv_c] 
    
def taille_liste_mobilite(liste_pieces,liste_couleurs,FEN,dico):
    mouvements=[]
    for type in dico:
        for i in dico[type]:
            mouvements=mouvements_pseudo_legaux(liste_pieces,liste_couleurs,i,FEN)
    return len(mouvements[0])+len(mouvements[1])

def liste_coups_conv_1012_alg(liste_coups):
    mouvements=[]
    for m in liste_coups:
        mouvements.append(conversion_1012_alg(m[0])+conversion_1012_alg(m[1]))
    return mouvements
