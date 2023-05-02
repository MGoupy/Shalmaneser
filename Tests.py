from Bot_Methodes import *

if __name__ == "__main__":

    profondeur=4
    
    ##### Test de la reporiduction des mouvements en mémoire #####
    test_moves_data=[
        "e2e4 c7c5 d2d4 c5d4 d1d4 a7a6 b1c3 g8f6 c1g5 f6e4 d4e4 f7f6 h2h4 f6g5 e1c1 g5h4 e4h4 d7d6 h4e4",
        "e2e3 b7b6 g1f3 e7e6 d2d3 g8f6 f1e2 d7d5 b1d2 b8c6 h2h3 c8b7 e1g1 f8e7 a2a3 d8d7 f3h2 a8d8 f1e1 e8g8 e1f1 g7g6 d2b1 e6e5 b1c3 d5d4 c3a2 g8g7 c1d2 f8e8 d1b1 d4e3 f2e3 e7f8 a2c3 g6g5 f1f3 e5e4 f3f1 e4d3 c2d3 f8c5 f1e1 c5e3 d2e3 e8e3 c3d1 e3e8 d1c3 d7d4 g1h1 d4f4 h2f3 g5g4 e1f1 g4f3 f1f3 f4d2 b1d1 d2b2 d1e1 f6h5 a1b1 b2a3 f3f2 h5g3 h1g1 d8d3 b1c1 e8e3 f2f3 g3e2 c3e2 e3e2 e1e2 a3c1 f3f1 c1c4 f1f3 c4d4 g1h1 d3d1 f3f1 d1f1 e2f1 b7c8 f1e1 d4d6 h1g1 d6d4 g1h1 d4d6 h1g1 d6c5 g1h1 c5e5 e1f2 e5a1 f2g1 a1g1 h1g1 c6d4 g1f2 d4f5 f2f3 f5d4 f3f2 d4f5 f2f3 f5h4 f3f2 h4g6 g2g3 c8h3 f2e2 g6e5 e2e1 e5d3 e1d2 h3f1 d2c2 b6b5 c2c3 b5b4 c3c2 c7c5 c2d2 b4b3 d2c3 b3b2 c3c2 c5c4 c2b1 f1e2 b1c2"
    ]
    test_moves_FEN_attendus=[
        "rnbqkb1r/1p2p1pp/p2p4/8/4Q3/2N5/PPP2PP1/2KR1BNR b kq - 1 10",
        "8/p4pkp/8/8/2p5/3n2P1/1pK1b3/8 b - - 3 68"
    ]
    test_moves_themes=[
        "Grand roque",
        "Longue liste de coups"
    ]
    for i in range(len(test_moves_data)):
        partie=Partie("")
        partie=faire_moves(partie,test_moves_data[i])
        if partie.FEN != test_moves_FEN_attendus[i]:
            print("Erreur, test tactique n°"+(str)(i)+", thème : "+test_moves_themes[i])
            print("FEN : "+partie.FEN)
            print("FEN attendu : "+test_moves_FEN_attendus[i])
            print(" ")
        
    print("Moves ok")
    print(" ")
        
    ##### Tests de coups tactiques #####
    test_coups_FEN=[
        "R5B1/4k3/1N6/3KPp1N/8/8/8/6q1 w - f6 0 1",
        "3q1bk1/2Q2p2/6p1/8/8/2P4P/6PK/8 w - - 0 47",
        "rn1k1b1r/p3pBp1/2p2nNp/8/P2q4/5P2/1P1B1PPP/R2QK2R w KQ - 0 14"
    ]
    test_coups_reponses_attendues=[
        "e5f6",
        "c7d8",
        "d2a5"
    ]
    test_coups_theme=[
        "Mat en 1 - Prise en passant",
        "Recapture évidente",
        "Attauqe à la découverte - Echec"
    ]
    cherche=Cherche()
    for i in range(len(test_coups_FEN)):
        partie=Partie(test_coups_FEN[i])
        coup=cherche.AlphaBeta_racine(profondeur,partie)
        if coup != test_coups_reponses_attendues[i]:
            print("Erreur, test tactique n°"+(str)(i)+", thème : "+test_coups_theme[i])
            print("Coup choisi "+coup+" coup attendu "+test_coups_reponses_attendues[i])
            
            
    print("Problèmes ok")
    print(" ")

    tests_perf_FEN=[
        "2b4r/p1B3R1/2k5/p2r2pP/3K4/3P3P/P4P2/3R4 w - - 0 38",
        "6k1/pb3rp1/1n5p/1p1P1p1P/1qpQ1N2/5N2/P4PP1/2K1R3 b - - 0 27",
        "r2qkb1r/pp2pp1p/3p1np1/2p5/2BnP3/2NQB2P/PPP2PP1/R3K2R b KQkq - 1 9"
    ]
    tests_perf_noeuds=0
    tests_perf_temps=0
    for i in range(len(tests_perf_FEN)):
        partie=Partie(tests_perf_FEN[i])
        coup=cherche.AlphaBeta_racine(profondeur,partie)
        tests_perf_noeuds+=cherche.noeud_cherches
        tests_perf_temps+=cherche.temps_cherche
    pos_testees=len(tests_perf_FEN)
    noeud_moy=tests_perf_noeuds/pos_testees
    temps_moy=tests_perf_temps/pos_testees
    vit_moy=noeud_moy/temps_moy
    print("Sur "+(str)(pos_testees)+" position testées, je recherche en moyenne "+(str)(noeud_moy)+" noeuds en un temps de "+(str)(temps_moy)+" secondes soit une vitesse moyenne de "+(str)(vit_moy)+" noeuds par secondes")
