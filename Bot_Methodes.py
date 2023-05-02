from Jeu import *
import time

class Cherche():
    
    def __init__(self):
        self.noeud_cherches=0
        self.partie=Partie("")
        
    def AlphaBeta_racine(self,profondeur,partie):
        
        self.noeud_cherches+=1
        beta=100000
        alpha=-100000 #faire plus propre
        
        self.partie=partie
        self.noeud_cherches=0
        self.temps_cherche=0
        start= time.time()
        
        ancienne_position=FEN_get_position(self.partie.FEN)
        ancien_cinquante=FEN_get_demicoup(self.partie.FEN)
        ancien_roque=FEN_get_roque(self.partie.FEN)
        ancien_passant=FEN_get_passant(self.partie.FEN)
        coups=[]
        for m in self.partie.liste_coups[0]+self.partie.liste_coups[1]:
            coups.append(m)
        for move in coups:
            infos_coup=self.partie.coup(move)
            cinquante=infos_coup[0]
            roque=infos_coup[1]
            passant=infos_coup[2]
            prise=infos_coup[3]
            fin=self.partie.fin_tour(cinquante,roque,passant)
            if fin[0]:
                if fin[1]==change_couleur_1012((str)(self.partie.couleur_active)):
                    score = 10000
                else:
                    score=0
            else:
                score=-1*self.AlphaBeta(-beta,-alpha,profondeur-1)
            if score>alpha:
                alpha=score
                meilleur_coup=move
            self.partie.retour(move,prise,ancienne_position,ancien_cinquante,ancien_roque,ancien_passant)
            
        end = time.time()
        self.temps_cherche=end-start
        meilleur_coup=conversion_coup_1012_alg(meilleur_coup)
        #print("je joue : "+meilleur_coup+" j'évalue la position à "+(str)(alpha)+" en ma faveur, profondeur de "+(str)(profondeur)+ " j'ai évalué "+(str)(self.noeud_cherches)+" noeuds en "+(str)(duree)+(" secondes"))
        return meilleur_coup

    def AlphaBeta(self,alpha,beta,profondeur):
        
        self.noeud_cherches+=1
        ancienne_position=FEN_get_position(self.partie.FEN)
        ancien_cinquante=FEN_get_demicoup(self.partie.FEN)
        ancien_roque=FEN_get_roque(self.partie.FEN)
        ancien_passant=FEN_get_passant(self.partie.FEN)
        coups=[]
        
        for m in self.partie.liste_coups[0]+self.partie.liste_coups[1]:
            coups.append(m)
            
        for move in coups:
            infos_coup=self.partie.coup(move)
            
            cinquante=infos_coup[0]
            roque=infos_coup[1]
            passant=infos_coup[2]
            prise=infos_coup[3]
            fin=self.partie.fin_tour(cinquante,roque,passant)
            if fin[0]:
                if fin[1]==change_couleur_1012((str)(self.partie.couleur_active)):
                    score = 1000*(10-profondeur)
                else:
                    score=0
            else:
                if profondeur-1==0:
                    score=-1*self.AlphaBeta_fin(-beta,-alpha)
                else:
                    score=-1*self.AlphaBeta(-beta,-alpha,profondeur-1)
            self.partie.retour(move,prise,ancienne_position,ancien_cinquante,ancien_roque,ancien_passant)                  
            if score>=beta:
                return beta
            if score>alpha:
                alpha=score
        return alpha
                
    def AlphaBeta_fin(self,alpha,beta):
        
        self.noeud_cherches+=1
        eval=self.eval_pos(self.partie.liste_pieces,self.partie.liste_couleurs,self.partie.FEN,self.partie.couleur_active)
        if eval>=beta:
            return beta
        if eval>alpha:
            alpha=eval
        coups_capture=[]
        for m in self.partie.liste_coups[0]:
            coups_capture.append(m)
        
        ancienne_position=FEN_get_position(self.partie.FEN)
        ancien_cinquante=FEN_get_demicoup(self.partie.FEN)
        ancien_roque=FEN_get_roque(self.partie.FEN)
        ancien_passant=FEN_get_passant(self.partie.FEN)
        
        for move in coups_capture:
            
            if eval+valeur_piece(self.partie.liste_pieces[move[1]])+1.5<alpha: #ne continue pas à chercher si prendre la pièce gratuitement n'est pas mieux que meilleur pos trouvée
                return alpha
            
            infos_coup=self.partie.coup(move)
            cinquante=infos_coup[0]
            roque=infos_coup[1]
            passant=infos_coup[2]
            prise=infos_coup[3]
            fin=self.partie.fin_tour(cinquante,roque,passant)
            if fin[0]:
                if fin[1]==change_couleur_1012((str)(self.partie.couleur_active)):
                    score = 1000
                else:
                    score=0
                    if score>alpha:
                        alpha=score
            else:
                score=-1*self.AlphaBeta_fin(-beta,-alpha)
            self.partie.retour(move,prise,ancienne_position,ancien_cinquante,ancien_roque,ancien_passant)                  
            if score>=beta:
                return beta
            if score>alpha:
                alpha=score
        return alpha  
            
    def eval_pos(self,liste_pieces,liste_couleurs,FEN,couleur):
        eval_score_secure_roi=0
        eval_score_materiel=0
        valeur_materiel_blanc=0
        valeur_materiel_noirs=0
        
        eval_score_mobilite=0.025*(taille_liste_mobilite(liste_pieces,liste_couleurs,FEN,self.partie.dico_pieces_blanches)-taille_liste_mobilite(liste_pieces,liste_couleurs,FEN,self.partie.dico_pieces_noires))

        nombre_pions=[len(self.partie.dico_pieces_blanches[1]),len(self.partie.dico_pieces_noires[2])]
        
        for type in self.partie.dico_pieces_blanches:
            for i in self.partie.dico_pieces_blanches[type]:
                valeur=valeur_piece_table(i,1,type,(int)(FEN_get_coup(self.partie.FEN)))
                pion_roi=0
                if type==7:
                    pion_roi=0
                    for d in [1,-1]:
                        if liste_pieces[i+d]==1:
                            pion_roi+=0.1
                    for d in [9,11]:
                        if liste_pieces[i+d]==1:
                            pion_roi+=0.15
                    for d in [19,20,21]:
                        if liste_pieces[i+d]==1:
                            pion_roi+=0.1
                    if liste_pieces[i+10]==1:
                        pion_roi+=0.2
                    eval_score_secure_roi+=pion_roi
                valeur_materiel_blanc+=valeur
                    
        for type in self.partie.dico_pieces_noires:
            for i in self.partie.dico_pieces_noires[type]:
                valeur=valeur_piece_table(i,2,type,(int)(FEN_get_coup(self.partie.FEN)))
                pion_roi=0
                if type==7:
                    pion_roi=0
                    for d in [1,-1]:
                        if liste_pieces[i+d]==2:
                            pion_roi+=0.1
                    for d in [-9,-11]:
                        if liste_pieces[i+d]==2:
                            pion_roi+=0.15
                    for d in [-19,-20,-21]:
                        if liste_pieces[i+d]==2:
                            pion_roi+=0.1
                    if liste_pieces[i-10]==2:
                        pion_roi+=0.2
                    eval_score_secure_roi-=pion_roi
                valeur_materiel_noirs-=valeur
        
        eval_score_materiel=valeur_materiel_blanc+valeur_materiel_noirs
        if couleur==1:
            if valeur_materiel_noirs+nombre_pions[1]>-10:
                eval_score_secure_roi=0
        else:
            if valeur_materiel_blanc-nombre_pions[0]<10:
                eval_score_secure_roi=0
        score=eval_score_materiel+eval_score_mobilite+eval_score_secure_roi
        if couleur==1:
            return score
        else:
            return -1*score

def valeur_piece_table(co,couleur,piece,coup):
    if piece==1 or piece==2:
        table=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,0,0,0,0,-1,-1,0,0,0,-0.3,-0.3,0,0,0,-1,-1,0,0,0.03,0.05,0.05,0.03,0,0,-1,-1,0,0.05,0.05,0.15,0.15,0.05,0.05,0,-1,-1,0.05,0.1,0.15,0.18,0.18,0.15,0.1,0.05,-1,-1,0.15,0.15,0.15,0.2,0.2,0.15,0.15,0.15,-1,-1,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,-1,-1,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        valeur=1
    elif piece==3:
        table=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-0.2,-0.3,-0.2,-0.2,-0.2,-0.2,-0.3,-0.2,-1,-1,-0.2,-0.1,-0.1,0,0,-0.1,-0.1,-0.2,-1,-1,-0.2,0,0,0,0,0,0,-0.2,-1,-1,-0.2,0,0,0.1,0.1,0,0,-0.2,-1,-1,-0.2,0,0.1,0.2,0.2,0.1,0,-0.2,-1,-1,-0.2,0.1,0.2,0.2,0.2,0.2,0.1,-0.2,-1,-1,-0.2,0,0,0.1,0.1,0,0,-0.2,-1,-1,-0.2,-0.2,-0.2,-0.2,-0.2,-0.2,-0.2,-0.2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        valeur=3.1
    elif piece==4:
        table=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-0.3,0,-0.2,0,0,-0.2,0,-0.3,-1,-1,0,0.1,0,0,0,0,0.1,0,-1,-1,0.1,0,0,0,0,0,0,0.1,-1,-1,0,0,0,0,0,0,0,0,-1,-1,0,0,0.1,0,0,0.1,0,0,-1,-1,0,0.1,0,0,0,0,0.1,0,-1,-1,0,0,0,0,0,0,0,0,-1,-1,-0.3,0,0,0,0,0,0,-0.3,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        valeur=3.2
    elif piece==5:
        table=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-0.1,-0.1,0,0.1,0.1,0,-0.1,-0.1,-1,-1,0,0,0.1,0.1,0.1,0.1,0,0,-1,-1,0,0,0,0,0,0,0,0,-1,-1,0,0,0,0,0,0,0,0,-1,-1,0,0,0,0,0,0,0,0,-1,-1,0,0,0,0,0,0,0,0,-1,-1,0,0,0,0,0,0,0,0,-1,-1,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        valeur=5
    elif piece==6:
        if coup<10:
            table=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,-0.05,0,0,0,-1,-1,0,0,0,0,0,0,0,0,-1,-1,-0.2,-0.2,-0.2,-0.2,-0.2,-0.2,-0.2,-0.2,-1,-1,-0.3,-0.3,-0.3,-0.3,-0.3,-0.3,-0.3,-0.3,-1,-1,-0.3,-0.3,-0.3,-0.3,-0.3,-0.3,-0.3,-0.3,-1,-1,-0.3,-0.3,-0.3,-0.3,-0.3,-0.3,-0.3,-0.3,-1,-1,0,0,0,0,0,0,0,0,-1,-1,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        else:
            table=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-0.2,-0.2,-0.2,-0.2,-0.2,-0.2,-0.2,-0.2,-1,-1,-0.2,0,0,0,0,0,0,-0.2,-1,-1,-0.2,0,0,0,0,0,0,-0.2,-1,-1,-0.2,0,0,0,0,0,0,-0.2,-1,-1,-0.2,0,0,0,0,0,0,-0.2,-1,-1,-0.2,0,0,0,0,0,0,-0.2,-1,-1,-0.2,0,0,0,0,0,0,-0.2,-1,-1,-0.2,-0.2,-0.2,-0.2,-0.2,-0.2,-0.2,-0.2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        valeur=9
    elif piece==7:
        table=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,-0.1,-0.1,-0.1,-0.1,0,0,-1,-1,0,0,-0.2,-0.3,-0.3,-0.2,0,0,-1,-1,0,0,0,0,0,0,0,0,-1,-1,0,0,0,0,0,0,0,0,-1,-1,0,0,0,0,0,0,0,0,-1,-1,0,0,0,0,0,0,0,0,-1,-1,0,0,0,0,0,0,0,0,-1,-1,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        valeur=0
    
    if couleur==1:
        return table[co]+valeur
    else:
        return table[119-co]+valeur

def faire_moves(partie,data):
    i=1
    while not string_vide(data):
        i+=1
        while data[0]==" ":
            data=data[1:]
        if " " in data:
            move=data[:data.find(" ")+1]
            data=data[data.find(" "):]
        else:
            move=data
            data=""
        infos_coup=partie.coup(conversion_coup_alg_1012(move))
        cinquante=infos_coup[0]
        roque=infos_coup[1]
        passant=infos_coup[2]
        fin=partie.fin_tour(cinquante,roque,passant)
    return partie