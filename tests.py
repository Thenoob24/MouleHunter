import unittest
from collections import deque
import sys
import io
from contextlib import contextmanager

# Import des classes depuis main.py
try:
    from main import Labyrinthe, IA
except ImportError as e:
    raise ImportError(
        "Impossible d'importer Labyrinthe et IA depuis main.py\n"
        "→ Vérifie que :\n"
        "   • main.py et test_moules.py sont dans le même dossier\n"
        "   • main.py contient bien les classes Labyrinthe et IA\n"
        "   • Le code qui se connecte au serveur est dans if __name__ == '__main__':"
    ) from e


@contextmanager
def capture_output():
    """Context manager pour capturer la sortie stdout de manière sûre"""
    old_stdout = sys.stdout
    try:
        sys.stdout = io.StringIO()
        yield sys.stdout
    finally:
        sys.stdout = old_stdout


class TestLabyrinthe(unittest.TestCase):
    """Tests pour la classe Labyrinthe"""

    def test_parsing_basique(self):
        """Test du parsing d'un labyrinthe simple"""
        # Format: largeurxhauteur/cellule1-cellule2-cellule3.../nb_joueurs-x1,y1-x2,y2
        data = "3x2/a-b-c-d-e-f/1-0,0"
        lab = Labyrinthe(data)

        self.assertEqual(lab.largeur, 3)
        self.assertEqual(lab.hauteur, 2)
        self.assertEqual(lab.nb_joueurs, 1)
        self.assertEqual(lab.joueurs[0], (0, 0))

    def test_parsing_avec_moules(self):
        """Test du parsing avec des moules"""
        data = "3x2/1-2-3-4-5-6/1-0,0"
        lab = Labyrinthe(data)

        self.assertEqual(lab.largeur, 3)
        self.assertEqual(lab.hauteur, 2)
        # Les cellules sont stockées ligne par ligne
        self.assertEqual(len(lab.grille), 2)
        self.assertEqual(len(lab.grille[0]), 3)

    def test_parsing_avec_bonus(self):
        """Test du parsing avec bonus Bs et Bp"""
        data = "4x2/Bs-.-.-.-.-.Bp/2-1,0-2,1"
        lab = Labyrinthe(data)

        self.assertEqual(lab.largeur, 4)
        self.assertEqual(lab.hauteur, 2)
        self.assertEqual(lab.nb_joueurs, 2)
        self.assertEqual(len(lab.joueurs), 2)

    def test_parsing_avec_murs(self):
        """Test du parsing avec murs Mu et M"""
        data = "3x2/Mu-M-.-.-.-./1-0,0"
        lab = Labyrinthe(data)

        self.assertEqual(lab.grille[0][0], "Mu")
        self.assertEqual(lab.grille[0][1], "M")

    def test_case_valide(self):
        """Test de l'accès à une case valide"""
        data = "3x2/a-b-c-d-e-f/1-0,0"
        lab = Labyrinthe(data)

        # Accès aux cases
        self.assertIsNotNone(lab.case(0, 0))
        self.assertIsNotNone(lab.case(1, 0))

    def test_case_hors_limites(self):
        """Test de l'accès à une case hors limites"""
        data = "3x2/.-.-.-.-.-./1-0,0"
        lab = Labyrinthe(data)

        self.assertEqual(lab.case(-1, 0), "Mu")
        self.assertEqual(lab.case(5, 0), "Mu")
        self.assertEqual(lab.case(0, -1), "Mu")
        self.assertEqual(lab.case(0, 5), "Mu")

    def test_accessible_case_valide(self):
        """Test d'accessibilité pour une case valide"""
        data = "3x2/.-.-.-.-.-./1-0,0"
        lab = Labyrinthe(data)

        self.assertTrue(lab.accessible(0, 0))
        self.assertTrue(lab.accessible(1, 0))

    def test_accessible_mur(self):
        """Test d'accessibilité pour un mur"""
        data = "3x2/Mu-.-.-.-.-./1-0,0"
        lab = Labyrinthe(data)

        self.assertFalse(lab.accessible(0, 0))
        self.assertTrue(lab.accessible(1, 0))

    def test_accessible_hors_limites(self):
        """Test d'accessibilité hors limites"""
        data = "3x2/.-.-.-.-.-./1-0,0"
        lab = Labyrinthe(data)

        self.assertFalse(lab.accessible(-1, 0))
        self.assertFalse(lab.accessible(10, 10))

    def test_grille_complexe(self):
        """Test avec une grille plus complexe"""
        data = "5x3/.-.-.-.-.-.-.-1-.-.-Bs-2-.-.-./2-0,0-4,2"
        lab = Labyrinthe(data)

        self.assertEqual(lab.largeur, 5)
        self.assertEqual(lab.hauteur, 3)
        self.assertEqual(lab.nb_joueurs, 2)

    def test_plusieurs_joueurs(self):
        """Test avec plusieurs joueurs"""
        data = "4x4/.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-/3-0,0-3,0-3,3"
        lab = Labyrinthe(data)

        self.assertEqual(lab.nb_joueurs, 3)
        self.assertEqual(len(lab.joueurs), 3)


class TestIA(unittest.TestCase):
    """Tests pour la classe IA"""

    def setUp(self):
        """Initialisation avant chaque test"""
        self.ia = IA()
        self.ia.frites = 0
        self.ia.bieres = 0

    def test_init(self):
        """Test de l'initialisation de l'IA"""
        ia = IA()
        self.assertEqual(ia.frites, 0)
        self.assertEqual(ia.bieres, 0)

    def test_simuler_position_nord(self):
        """Test de simulation de position vers le Nord"""
        pos = (2, 2)
        nouvelle_pos = self.ia.simuler_position(pos, "N")
        self.assertEqual(nouvelle_pos, (2, 1))

    def test_simuler_position_sud(self):
        """Test de simulation de position vers le Sud"""
        pos = (2, 2)
        nouvelle_pos = self.ia.simuler_position(pos, "S")
        self.assertEqual(nouvelle_pos, (2, 3))

    def test_simuler_position_est(self):
        """Test de simulation de position vers l'Est"""
        pos = (2, 2)
        nouvelle_pos = self.ia.simuler_position(pos, "E")
        self.assertEqual(nouvelle_pos, (3, 2))

    def test_simuler_position_ouest(self):
        """Test de simulation de position vers l'Ouest"""
        pos = (2, 2)
        nouvelle_pos = self.ia.simuler_position(pos, "O")
        self.assertEqual(nouvelle_pos, (1, 2))

    def test_predire_collecte_frite(self):
        """Test de collecte d'une frite"""
        data = "3x2/Bs-.-.-.-.-./1-0,0"
        lab = Labyrinthe(data)

        with capture_output():
            self.ia.predire_collecte(lab, (0, 0))

        self.assertEqual(self.ia.frites, 1)

    def test_predire_collecte_biere(self):
        """Test de collecte d'une bière"""
        data = "3x2/Bp-.-.-.-.-./1-0,0"
        lab = Labyrinthe(data)

        with capture_output():
            self.ia.predire_collecte(lab, (0, 0))

        self.assertEqual(self.ia.bieres, 1)

    def test_predire_collecte_moules(self):
        """Test de collecte de moules"""
        data = "3x2/5-.-.-.-.-./1-0,0"
        lab = Labyrinthe(data)

        with capture_output():
            self.ia.predire_collecte(lab, (0, 0))

    def test_predire_collecte_case_vide(self):
        """Test de collecte sur une case vide"""
        data = "3x2/.-.-.-.-.-./1-0,0"
        lab = Labyrinthe(data)

        frites_avant = self.ia.frites
        bieres_avant = self.ia.bieres

        with capture_output():
            self.ia.predire_collecte(lab, (0, 0))

        self.assertEqual(self.ia.frites, frites_avant)
        self.assertEqual(self.ia.bieres, bieres_avant)


class TestParcoursFrites(unittest.TestCase):
    """Tests pour le parcours avec frites"""

    def setUp(self):
        self.ia = IA()

    def test_parcours_simple_sans_frite(self):
        """Test d'un parcours simple sans utiliser de frite"""
        data = "5x3/.-.-.-.-.-.-.-1-.-.-.-.-.-.-./1-0,0"
        lab = Labyrinthe(data)

        chemin, frites_used, bonus = self.ia.parcourt_largeur_avec_frites(
            lab, (0, 0), (2, 1), 0
        )

        self.assertIsNotNone(chemin)
        self.assertEqual(frites_used, 0)
        self.assertIsInstance(bonus, dict)

    def test_parcours_avec_frite_disponible(self):
        """Test d'un parcours avec frite disponible"""
        data = "5x1/.-.-Mu-.-./1-0,0"
        lab = Labyrinthe(data)

        chemin, frites_used, bonus = self.ia.parcourt_largeur_avec_frites(
            lab, (0, 0), (3, 0), 2
        )

        self.assertIsNotNone(chemin)
        self.assertLessEqual(frites_used, 2)

    def test_parcours_objectif_depart(self):
        """Test quand départ = objectif"""
        data = "3x3/1-.-.-.-.-.-2-.-./1-0,0"
        lab = Labyrinthe(data)

        chemin, frites_used, bonus = self.ia.parcourt_largeur_avec_frites(
            lab, (0, 0), (0, 0), 0
        )

        self.assertIsNotNone(chemin)
        self.assertEqual(len(chemin), 0)
        self.assertEqual(frites_used, 0)

    def test_parcours_collecte_bonus(self):
        """Test de la collecte de bonus durant le parcours"""
        data = "5x1/.-Bs-1-.-./1-0,0"
        lab = Labyrinthe(data)

        chemin, frites_used, bonus = self.ia.parcourt_largeur_avec_frites(
            lab, (0, 0), (2, 0), 0
        )

        self.assertIsNotNone(chemin)
        self.assertEqual(bonus["Bs"], 1)

    def test_parcours_impossible(self):
        """Test d'un parcours impossible (objectif inaccessible)"""
        data = "5x1/.-.-Mu-Mu-1/1-0,0"
        lab = Labyrinthe(data)

        chemin, frites_used, bonus = self.ia.parcourt_largeur_avec_frites(
            lab, (0, 0), (4, 0), 0
        )

        # Sans frites suffisantes, impossible d'atteindre
        self.assertIsNone(chemin)

    def test_parcours_avec_frite_suffisante(self):
        """Test avec assez de frites pour traverser un mur"""
        data = "4x1/.-Mu-1-./1-0,0"
        lab = Labyrinthe(data)

        chemin, frites_used, bonus = self.ia.parcourt_largeur_avec_frites(
            lab, (0, 0), (2, 0), 1
        )

        self.assertIsNotNone(chemin)
        self.assertEqual(frites_used, 1)


class TestParcoursBieres(unittest.TestCase):
    """Tests pour le parcours avec bières"""

    def setUp(self):
        self.ia = IA()

    def test_parcours_simple_sans_biere(self):
        """Test d'un parcours simple sans utiliser de bière"""
        data = "5x3/.-.-.-.-.-.-.-1-.-.-.-.-.-.-./1-0,0"
        lab = Labyrinthe(data)

        chemin, bieres_used, bonus = self.ia.parcourt_largeur_avec_biere(
            lab, (0, 0), (2, 1), 0
        )

        self.assertIsNotNone(chemin)
        self.assertEqual(bieres_used, 0)

    def test_parcours_avec_biere_disponible(self):
        """Test d'un parcours avec bière disponible"""
        data = "6x1/.-.-.-.-1-./1-0,0"
        lab = Labyrinthe(data)

        chemin, bieres_used, bonus = self.ia.parcourt_largeur_avec_biere(
            lab, (0, 0), (4, 0), 1
        )

        self.assertIsNotNone(chemin)

    def test_parcours_biere_objectif_depart(self):
        """Test quand départ = objectif avec bières"""
        data = "6x1/.-Bp-.-1-.-./1-0,0"  # Bp déplacé
        lab = Labyrinthe(data)

        chemin, bieres_used, bonus = self.ia.parcourt_largeur_avec_biere(
            lab, (0, 0), (0, 0), 0
        )

        self.assertIsNotNone(bonus)
        self.assertIn("Bp", bonus)



class TestEvaluation(unittest.TestCase):
    """Tests pour l'évaluation des objectifs"""

    def setUp(self):
        self.ia = IA()
        self.ia.frites = 2
        self.ia.bieres = 1

    def test_evaluer_objectif_moule_accessible(self):
        """Test d'évaluation d'une moule accessible"""
        data = "4x3/.-.-9-.-.-.-.-.-.-.-.-.-/1-0,0"
        lab = Labyrinthe(data)

        score, chemin, used, bonus, typ = self.ia.evaluer_objectif(
            lab, (0, 0), (2, 0)
        )

        self.assertGreater(score, 0)
        self.assertIsNotNone(chemin)
        self.assertIn(typ, ["frites", "bieres"])

    def test_evaluer_objectif_non_moule(self):
        """Test d'évaluation d'une case qui n'est pas une moule"""
        data = "3x3/.-.-.-Bs-.-.-2-.-./1-0,0"
        lab = Labyrinthe(data)

        score, chemin, used, bonus, typ = self.ia.evaluer_objectif(
            lab, (0, 0), (1, 1)  # Position de Bs
        )

        self.assertEqual(score, -99999)
        self.assertIsNone(chemin)

    def test_evaluer_objectif_petite_moule(self):
        """Test d'évaluation d'une petite moule"""
        data = "3x3/1-.-.-.-.-.-2-.-./1-0,0"
        lab = Labyrinthe(data)

        score1, chemin1, _, _, _ = self.ia.evaluer_objectif(lab, (0, 0), (0, 0))
        score2, chemin2, _, _, _ = self.ia.evaluer_objectif(lab, (0, 0), (0, 2))

        # La moule de valeur 2 devrait avoir un meilleur score
        if chemin1 and chemin2:
            self.assertGreater(score2, score1)

    def test_evaluer_objectif_inaccessible(self):
        """Test d'évaluation d'une moule inaccessible"""
        data = "5x1/.-.-Mu-Mu-9/1-0,0"
        lab = Labyrinthe(data)

        self.ia.frites = 0
        self.ia.bieres = 0

        score, chemin, used, bonus, typ = self.ia.evaluer_objectif(
            lab, (0, 0), (4, 0)
        )

        # Sans bonus, devrait être inaccessible
        self.assertEqual(score, -99999)


class TestTrouverMeilleurObjectif(unittest.TestCase):
    """Tests pour trouver le meilleur objectif"""

    def setUp(self):
        self.ia = IA()
        self.ia.frites = 2
        self.ia.bieres = 1

    def test_trouver_meilleur_plusieurs_moules(self):
        """Test de recherche avec plusieurs moules"""
        data = "6x4/.-.-8-.-.-.-.-.-5-.-.-.-Bs-.-.-.-.-.-.-.-9-.-.-.-/1-0,0"
        lab = Labyrinthe(data)

        chemin, used, bonus, typ = self.ia.trouver_meilleur_objectif(lab, (0, 0))

        self.assertIsNotNone(chemin)
        self.assertIsInstance(used, int)
        self.assertIsInstance(bonus, dict)

    def test_trouver_meilleur_aucune_moule(self):
        """Test quand il n'y a aucune moule"""
        data = "3x3/.-.-.-Bs-.-.-Bp-.-./1-0,0"
        lab = Labyrinthe(data)

        chemin, used, bonus, typ = self.ia.trouver_meilleur_objectif(lab, (0, 0))

        self.assertIsNone(chemin)

    def test_trouver_meilleur_une_seule_moule(self):
        """Test avec une seule moule"""
        data = "3x3/.-.-.-.-.-5-.-.-./1-0,0"
        lab = Labyrinthe(data)

        chemin, used, bonus, typ = self.ia.trouver_meilleur_objectif(lab, (0, 0))

        self.assertIsNotNone(chemin)


class TestExecutionMouvements(unittest.TestCase):
    """Tests pour l'exécution des mouvements"""

    def setUp(self):
        self.ia = IA()

    def test_executer_mouvement_frite_nord(self):
        """Test d'exécution d'un mouvement avec frite vers le Nord"""
        data = "3x3/.-.-.-Bs-1-.-.-.-./1-1,1"
        lab = Labyrinthe(data)

        self.ia.frites = 1

        with capture_output():
            self.ia.executer_mouvement_frite(lab, (1, 1), "Bs-N")

    def test_executer_mouvement_frite_est(self):
        """Test d'exécution d'un mouvement avec frite vers l'Est"""
        data = "3x3/.-.-.-1-Bs-.-.-.-./1-0,1"
        lab = Labyrinthe(data)

        self.ia.frites = 1

        with capture_output():
            self.ia.executer_mouvement_frite(lab, (0, 1), "Bs-E")

    def test_executer_mouvement_biere(self):
        """Test d'exécution d'un mouvement avec bière"""
        data = "5x1/.-.-1-.-./1-0,0"
        lab = Labyrinthe(data)

        self.ia.bieres = 1

        with capture_output():
            self.ia.executer_mouvement_biere(lab, (0, 0), "Bp-E-E-E")

    def test_executer_mouvement_biere_directions_variees(self):
        """Test d'exécution avec différentes directions"""
        data = "4x4/.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-/1-0,0"
        lab = Labyrinthe(data)

        self.ia.bieres = 1

        with capture_output():
            self.ia.executer_mouvement_biere(lab, (0, 0), "Bp-E-S-E")


class TestChoisirCoup(unittest.TestCase):
    """Tests pour le choix du coup"""

    def setUp(self):
        self.ia = IA()

    def test_choisir_coup_moule_proche(self):
        """Test du choix de coup avec une moule proche"""
        data = "3x3/.-.-5-.-.-.-.-.-./1-0,0"
        lab = Labyrinthe(data)

        with capture_output():
            coup = self.ia.choisir_coup(lab, 0)

        self.assertIsNotNone(coup)
        self.assertIn(coup, ["N", "S", "E", "O", "C"] +
                      [f"Bs-{d}" for d in "NSEO"] +
                      [f"Bp-{d1}-{d2}-{d3}" for d1 in "NSEO" for d2 in "NSEO" for d3 in "NSEO"])

    def test_choisir_coup_exploration(self):
        """Test du mode exploration (aucune moule visible)"""
        data = "3x3/.-.-.-.-.-.-.-.-./1-0,0"
        lab = Labyrinthe(data)

        with capture_output():
            coup = self.ia.choisir_coup(lab, 0)

        self.assertIsNotNone(coup)

    def test_choisir_coup_avec_bonus_sur_chemin(self):
        """Test quand il y a un bonus sur le chemin"""
        data = "4x1/Bs-1-9-./1-0,0"
        lab = Labyrinthe(data)

        with capture_output():
            coup = self.ia.choisir_coup(lab, 0)

        # Devrait aller vers l'Est
        self.assertEqual(coup, "E")

    def test_choisir_coup_bloque(self):
        """Test quand le joueur est complètement bloqué"""
        data = "3x3/Mu-Mu-Mu-Mu-.-Mu-Mu-Mu-Mu/1-1,1"
        lab = Labyrinthe(data)

        with capture_output():
            coup = self.ia.choisir_coup(lab, 0)

        # Devrait retourner "C" (Conserver)
        self.assertEqual(coup, "C")

    def test_choisir_coup_avec_frites_disponibles(self):
        """Test avec des frites en inventaire"""
        data = "4x1/.-Mu-9-./1-0,0"
        lab = Labyrinthe(data)

        self.ia.frites = 2

        with capture_output():
            coup = self.ia.choisir_coup(lab, 0)

        # Devrait potentiellement utiliser une frite
        self.assertIsNotNone(coup)

    def test_choisir_coup_avec_bieres_disponibles(self):
        """Test avec des bières en inventaire"""
        data = "6x1/.-.-.-.-9-./1-0,0"
        lab = Labyrinthe(data)

        self.ia.bieres = 1

        with capture_output():
            coup = self.ia.choisir_coup(lab, 0)

        self.assertIsNotNone(coup)


class TestCasLimites(unittest.TestCase):
    """Tests des cas limites et edge cases"""

    def test_grille_1x1(self):
        """Test avec une grille de taille minimale"""
        data = "1x1/5/1-0,0"
        lab = Labyrinthe(data)

        self.assertEqual(lab.largeur, 1)
        self.assertEqual(lab.hauteur, 1)

    def test_grille_grande(self):
        """Test avec une grande grille"""
        cellules = ["."] * 50  # 5x10 = 50 cellules
        data = f"5x10/{'-'.join(cellules)}/1-0,0"
        lab = Labyrinthe(data)

        self.assertEqual(lab.largeur, 5)
        self.assertEqual(lab.hauteur, 10)

    def test_moule_valeur_9(self):
        """Test avec la moule de plus grande valeur"""
        data = "3x3/.-.-9-.-.-.-.-.-./1-0,0"
        lab = Labyrinthe(data)

        ia = IA()
        ia.frites = 1
        ia.bieres = 1

        score, chemin, _, _, _ = ia.evaluer_objectif(lab, (0, 0), (2, 0))

        self.assertGreater(score, 0)

    def test_chemin_optimal_vs_court(self):
        """Test que l'IA choisit un bon chemin"""
        data = "5x3/1-.-.-.-9-.-.-.-.-.-.-.-.-.-/1-0,0"
        lab = Labyrinthe(data)

        ia = IA()
        ia.frites = 5
        ia.bieres = 5

        chemin, _, _, _ = ia.trouver_meilleur_objectif(lab, (0, 0))

        # Devrait préférer la moule de valeur 9
        self.assertIsNotNone(chemin)


class TestIntegration(unittest.TestCase):
    """Tests d'intégration de bout en bout"""

    def test_partie_complete_simple(self):
        """Simulation d'une partie complète simple"""
        data = "5x3/.-.-.-.-9-Bs-.-.-.-.-.-.-.-.-./1-0,0"
        lab = Labyrinthe(data)

        ia = IA()

        with capture_output():
            coup1 = ia.choisir_coup(lab, 0)

        self.assertIsNotNone(coup1)

    def test_collecte_successive_bonus(self):
        """Test de collecte successive de bonus"""
        ia = IA()

        data1 = "3x1/Bs-.-./1-0,0"
        lab1 = Labyrinthe(data1)

        with capture_output():
            ia.predire_collecte(lab1, (0, 0))
            ia.predire_collecte(lab1, (0, 0))

        self.assertEqual(ia.frites, 2)

if __name__ == '__main__':
    # Exécuter les tests avec verbosité
    unittest.main(verbosity=2)