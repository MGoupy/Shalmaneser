
from threading import Thread
from Jeu_Methodes import *

class Partie:

    def __init__(self,FEN):
        
        if not FEN:
            FEN="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        else:
            FEN=string_suppr_espaces(FEN)
            
        self.FEN=FEN
        if FEN_get_couleur(self.FEN)=='w':
            self.couleur_active=1
        else:
            self.couleur_active=2
        self.position=FEN_get_position(FEN)
        self.roques=FEN_get_roque(FEN)
        self.passant=FEN_get_passant(FEN)
        self.demicoup=(int)(FEN_get_demicoup(FEN))
        self.comptecoup=(int)(FEN_get_coup(FEN))
        
        listes=listes_from_FEN(self.FEN)
        self.liste_pieces=listes[0]
        self.liste_couleurs=listes[1]
        self.dico_pieces_blanches={
            1:[],
            3:[],
            4:[],
            5:[],
            6:[],
            7:[]
        }
        self.dico_pieces_noires={
            2:[],
            3:[],
            4:[],
            5:[],
            6:[],
            7:[]
        }
        self.update_dico()
        self.anciennes_positions=[FEN_get_position(self.FEN)]
        self.liste_coups=self.liste_coups_1012()
    
    def update_dico(self):
        for i in cases_sur_plateau():
            if self.liste_couleurs[i]==1:
                self.dico_pieces_blanches[self.liste_pieces[i]].append(i)
            if self.liste_couleurs[i]==2:
                self.dico_pieces_noires[self.liste_pieces[i]].append(i)

    def coup(self,coup): #coup en coordonées 10*12
        cod=coup[0]
        cof=coup[1]
        
        prise=0
        roque=""
        passant="-"
        cinquante=False
        
        piece=self.liste_pieces[cod]
        couleur=self.liste_couleurs[cod]

        # Retire roque si la tour bouge ou est prise
        if (cod==91) or (cof==91):
            roque+="q"
        if (cod==98) or (cof==98):
            roque+="k"
        if (cod==21) or (cof==21):
            roque+="Q"
        if (cod==28) or (cof==28):
            roque+="K"

        # Règles spéciales
        if piece==7:
            if couleur==1: # Retire roque si roi bouge
                roque+="KQ"
            else:
                roque +="kq"
            if abs(cod-cof)==2: #Roque
                if cof==27:
                    tour_posd=28
                    tour_posf=26
                elif cof==23:
                    tour_posd=21
                    tour_posf=24
                elif cof==93:
                    tour_posd=91
                    tour_posf=94
                else:
                    tour_posd=98
                    tour_posf=96
                self.bouge_piece_1012(tour_posd,tour_posf)
        elif piece==1 or piece==2:
            cinquante=True
            if abs(cod-cof)==20:
                if couleur==2:
                    passant=conversion_1012_alg(cof+10)
                else:
                    passant=conversion_1012_alg(cof-10)
            elif cod%10 != cof%10 and self.liste_pieces[cof]==0:
                if couleur==2:
                    self.prise_piece(cof+10)
                else:
                    self.prise_piece(cof-10)
        
        # Prise d"une pièce
        if not self.liste_pieces[cof]==0:
            prise=self.liste_pieces[cof]
            self.prise_piece(cof)
            cinquante=True
                
        # Mouvement
        self.bouge_piece_1012(cod,cof)
        
        # Promotion
        if coup[2]!="":
            self.change_type_promo(coup[2],cof)
        
        return([cinquante,roque,passant,prise])
    
    def retour(self,coup,prise,position,cinquante,roque,passant):
        
        cod=coup[0]
        cof=coup[1]
        
        piece=self.liste_pieces[cof]
        couleur=self.liste_couleurs[cof]
        
        if piece==7:
            if abs(cod-cof)==2: #Roque
                if cof==27:
                    tour_posd=28
                    tour_posf=26
                elif cof==23:
                    tour_posd=21
                    tour_posf=24
                elif cof==93:
                    tour_posd=91
                    tour_posf=94
                else:
                    tour_posd=98
                    tour_posf=96
                self.bouge_piece_1012(tour_posf,tour_posd)
        if passant != "-":
            if conversion_alg_1012(passant)==cof and (self.liste_pieces[cof]==1 or self.liste_pieces[cof]==2):   
                if couleur==1:
                    self.cree_piece(cof-10,2,2)
                else:
                    self.cree_piece(cof+10,1,1)
        
        self.bouge_piece_1012(cof,cod)
        
        if coup[2]!="":
            if couleur==1:
                self.change_type(1,cod)
            else:
                self.change_type(2,cod)
            
        if prise!=0:
            self.cree_piece(cof,prise,change_couleur_1012(couleur))
        
        
        self.couleur_active=change_couleur_1012(self.couleur_active)   
        self.FEN=self.FEN_deupdate(position,cinquante,roque,passant)
        self.anciennes_positions=self.anciennes_positions[:len(self.anciennes_positions)-1]

    def cree_piece(self,co,type,couleur):
        self.liste_pieces[co]=type
        self.liste_couleurs[co]=couleur
        if couleur==1:
            self.dico_pieces_blanches[type].append(co)
        else:
            self.dico_pieces_noires[type].append(co)
        
    def prise_piece(self,co):
        piece=self.liste_pieces[co]
        couleur=self.liste_couleurs[co]
        self.liste_pieces[co]=0
        self.liste_couleurs[co]=0
        if couleur==1:
            self.dico_pieces_blanches[piece].remove(co)
        else:
            self.dico_pieces_noires[piece].remove(co)
      
      
    def change_type_promo(self,type,co):
        piece_ancien=self.liste_pieces[co]
        couleur=self.liste_couleurs[co]
        if type=="q":
            piece=6
        elif type=="r":
            piece=5
        elif type=="b":
            piece=4
        elif type=="n":
            piece=3
        self.liste_pieces[co]=piece
        if couleur==1:
            self.dico_pieces_blanches[piece_ancien].remove(co)
            self.dico_pieces_blanches[piece].append(co)
        else:
            self.dico_pieces_noires[piece_ancien].remove(co)
            self.dico_pieces_noires[piece].append(co)
    
    def change_type(self,type,co):
        piece_ancien=self.liste_pieces[co]
        couleur=self.liste_couleurs[co]
        self.liste_pieces[co]=type
        if couleur==1:
            self.dico_pieces_blanches[piece_ancien].remove(co)
            self.dico_pieces_blanches[type].append(co)
        else:
            self.dico_pieces_noires[piece_ancien].remove(co)
            self.dico_pieces_noires[type].append(co)
        
    
    def bouge_piece_1012(self,cod,cof):
        piece=self.liste_pieces[cod]
        couleur=self.liste_couleurs[cod]
        self.liste_pieces[cof]=piece
        self.liste_couleurs[cof]=couleur
        self.liste_pieces[cod]=0
        self.liste_couleurs[cod]=0
        if couleur==1:
            self.dico_pieces_blanches[piece].remove(cod)
            self.dico_pieces_blanches[piece].append(cof)
        else:
            self.dico_pieces_noires[piece].remove(cod)
            self.dico_pieces_noires[piece].append(cof)
            
    def fin_tour(self,cinquante,roque,passant):
        
        self.FEN=self.FEN_update(self.FEN,self.liste_pieces,self.liste_couleurs,cinquante,roque,passant)     
        pos=FEN_get_position(self.FEN)
        self.anciennes_positions.append(pos)
        
        fin=False
        raison_fin=""
        self.couleur_active=change_couleur_1012(self.couleur_active)
        self.liste_coups=self.liste_coups_1012()
        moves=self.liste_coups[0]+self.liste_coups[1]
        if moves==[]:
            if self.couleur_active==1:
                case_roi=self.dico_pieces_blanches[7][0]
            else:
                case_roi=self.dico_pieces_noires[7][0]
            if cherche_echec_case(self.liste_pieces,self.liste_couleurs,self.couleur_active,case_roi):
                fin=True
                raison_fin=change_couleur_1012((str)(self.couleur_active))
            else:
                fin=True
                raison_fin="pat"
        elif self.demicoup>=75:
            fin=True
            raison_fin="50"
        elif self.anciennes_positions.count(pos)>=3:
            fin=True
            raison_fin="3"
        return [fin,raison_fin]

    def liste_coups_1012(self):
        mouvements=[]
        mouvements_capture=[]
        mouvements_promotion=[]
        mouvements_silencieux=[]
        if self.couleur_active==1:
            dico=self.dico_pieces_blanches
        else:
            dico=self.dico_pieces_noires
        for type_piece in dico:
            for i in dico[type_piece]:
                if danger_roi(self.liste_pieces,self.liste_couleurs,self.couleur_active,self.FEN,dico):
                    mouvements=mouvements_pseudo_legaux(self.liste_pieces,self.liste_couleurs,i,self.FEN)
                    mouvements[0]=enlever_mouvements_illegaux(i,mouvements[0],self.liste_pieces,self.liste_couleurs,self.FEN,dico)
                    mouvements[1]=enlever_mouvements_illegaux(i,mouvements[1],self.liste_pieces,self.liste_couleurs,self.FEN,dico)
                else:
                    mouvements=mouvements_pseudo_legaux(self.liste_pieces,self.liste_couleurs,i,self.FEN)
                for m in mouvements[0]:
                    if (m//10==9 and type_piece==1) or (m//10==2 and type_piece==2):
                        mouvements_promotion.append([i,m,"n"])
                        mouvements_promotion.append([i,m,"b"])
                        mouvements_promotion.append([i,m,"r"])
                        mouvements_promotion.append([i,m,"q"])
                    else:
                        mouvements_capture.append([i,m,""])
                for m in mouvements[1]:
                    if (m//10==9 and type_piece==1) or (m//10==2 and type_piece==2):
                        mouvements_promotion.append([i,m,"n"])
                        mouvements_promotion.append([i,m,"b"])
                        mouvements_promotion.append([i,m,"r"])
                        mouvements_promotion.append([i,m,"q"])
                    else:
                        mouvements_silencieux.append([i,m,""])

        return [mouvements_promotion+self.ordoner_captures(mouvements_capture),self.ordoner_mouvements(mouvements_silencieux)]
    
    def ordoner_captures(self,capture):
        return sorted(capture, key=lambda m: (valeur_piece(self.liste_pieces[m[1]])-valeur_piece(self.liste_pieces[m[0]])), reverse=True)

    def ordoner_mouvements(self,mouvements):
        return sorted(mouvements, key=lambda m: (valeur_mouvement(self.liste_pieces[m[0]],m[1],self.couleur_active)), reverse=True)

    def FEN_update(self,FEN,liste_pieces,liste_couleurs,cinquante,roque,passant):

            ancien_FEN=FEN
            ancienFEN_roque=FEN_get_roque(ancien_FEN)

            nouveauFEN_position=FEN_update_position(liste_pieces,liste_couleurs)

            if self.couleur_active==1:
                nouveauFEN_couleur="b"  
            else:
                nouveauFEN_couleur="w" 
                self.comptecoup+=1
                
            if cinquante:
                self.demicoup=0
            else:
                self.demicoup+=1

            if roque:
                for c in roque:
                    ancienFEN_roque=ancienFEN_roque.replace(c,"")
                    if not ancienFEN_roque:
                        ancienFEN_roque="-"
                nouveauFEN_roque=ancienFEN_roque
            else:
                nouveauFEN_roque=ancienFEN_roque
                
            nouveauFEN_passant=passant

            nouveauFEN=nouveauFEN_position+" "+nouveauFEN_couleur+" "+nouveauFEN_roque+" "+nouveauFEN_passant+" "+(str)(self.demicoup)+" "+(str)(self.comptecoup)
            return nouveauFEN

    def FEN_deupdate(self,FEN_precedent_position,FEN_precedent_cinquante,FEN_precedent_roque,FEN_precedent_passant):
        
            if self.couleur_active==1:
                couleur="w"
            else:
                couleur="b"
                self.comptecoup-=1

            nouveauFEN=FEN_precedent_position+" "+couleur+" "+FEN_precedent_roque+" "+FEN_precedent_passant+" "+FEN_precedent_cinquante+" "+(str)(self.comptecoup)
            return nouveauFEN
    
