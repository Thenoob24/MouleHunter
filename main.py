import socket
import random
from collections import deque


def load_env_file(filename='.env'):
    env = {}
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    env[k.strip()] = v.strip()
    except FileNotFoundError:
        print("Crée un fichier .env avec :")
        print("SERVEUR_IP=127.0.0.1")
        print("SERVEUR_PORT=1337")
        print("NOM_EQUIPE=GodMoules2025")
        exit(1)
    return env


class Labyrinthe:
    def __init__(self, data):
        parts = data.split('/')
        taille = parts[0].split('x')
        self.largeur, self.hauteur = int(taille[0]), int(taille[1])

        cellules = parts[1].split('-')
        self.grille = [cellules[i * self.largeur:(i + 1) * self.largeur] for i in range(self.hauteur)]

        joueurs = parts[2].split('-')
        self.nb_joueurs = int(joueurs[0])
        self.joueurs = [tuple(map(int, p.split(','))) for p in joueurs[1:]]

    def case(self, x, y):
        if 0 <= x < self.largeur and 0 <= y < self.hauteur:
            return self.grille[y][x]
        return "Mu"

    def accessible(self, x, y):
        c = self.case(x, y)
        return c != "Mu"


class IA:
    def __init__(self):
        self.frites = 0
        self.bieres = 0

    def parcourt_largeur_avec_frites(self, lab, depart, objectif, nb_frites_dispo):
        """
        Parcourt largeur modifié qui trouve le chemin le plus court en tenant compte des frites.
        État = (position, nb_frites_utilisées)
        Retourne : (chemin, nb_frites_utilisées, bonus_ramasses)
        """
        # File : (position, chemin, frites_utilisées, bonus_collectés)
        q = deque([(depart, [], 0, {"Bs": 0, "Bp": 0})])
        # Visité : {(pos, frites_utilisées): meilleur_cout}
        visite = {(depart, 0): 0}

        meilleur_chemin = None
        meilleur_cout = float('inf')
        meilleur_frites = 0
        meilleur_bonus = {"Bs": 0, "Bp": 0}

        while q:
            pos, chemin, frites_used, bonus = q.popleft()

            # Si on a atteint l'objectif
            if pos == objectif:
                cout_actuel = len(chemin)
                if cout_actuel < meilleur_cout:
                    meilleur_cout = cout_actuel
                    meilleur_chemin = chemin
                    meilleur_frites = frites_used
                    meilleur_bonus = bonus.copy()
                continue

            x, y = pos

            # Pour chaque direction
            for direction, (dx, dy) in [("N", (0, -1)), ("S", (0, 1)), ("E", (1, 0)), ("O", (-1, 0))]:
                # OPTION 1 : Mouvement normal
                nx1, ny1 = x + dx, y + dy
                if lab.accessible(nx1, ny1):
                    etat = ((nx1, ny1), frites_used)
                    nouveau_cout = len(chemin) + 1

                    if etat not in visite or visite[etat] > nouveau_cout:
                        visite[etat] = nouveau_cout

                        # Calculer les bonus collectés
                        nouveaux_bonus = bonus.copy()
                        cell = lab.case(nx1, ny1)
                        if cell == "Bs":
                            nouveaux_bonus["Bs"] += 1
                        elif cell == "Bp":
                            nouveaux_bonus["Bp"] += 1

                        q.append(((nx1, ny1), chemin + [direction], frites_used, nouveaux_bonus))

                # OPTION 2 : Utiliser une frite (sauter 2 cases)
                if frites_used < nb_frites_dispo:
                    nx2, ny2 = x + 2 * dx, y + 2 * dy

                    # La case d'arrivée (2 cases plus loin) doit être accessible
                    if lab.accessible(nx2, ny2):
                        etat = ((nx2, ny2), frites_used + 1)
                        nouveau_cout = len(chemin) + 1

                        if etat not in visite or visite[etat] > nouveau_cout:
                            visite[etat] = nouveau_cout

                            # Calculer les bonus collectés (sur la case intermédiaire ET finale)
                            nouveaux_bonus = bonus.copy()

                            # Case intermédiaire (peut être un mur, mais on collecte quand même si bonus)
                            cell_inter = lab.case(nx1, ny1)
                            if cell_inter == "Bs":
                                nouveaux_bonus["Bs"] += 1
                            elif cell_inter == "Bp":
                                nouveaux_bonus["Bp"] += 1

                            # Case finale
                            cell_final = lab.case(nx2, ny2)
                            if cell_final == "Bs":
                                nouveaux_bonus["Bs"] += 1
                            elif cell_final == "Bp":
                                nouveaux_bonus["Bp"] += 1

                            q.append(((nx2, ny2), chemin + [f"Bs-{direction}"], frites_used + 1, nouveaux_bonus))

                    # Si case 2 bloquée mais case 1 accessible, on avance juste d'1 case
                    elif lab.accessible(nx1, ny1) and not lab.accessible(nx2, ny2):
                        etat = ((nx1, ny1), frites_used + 1)
                        nouveau_cout = len(chemin) + 1

                        if etat not in visite or visite[etat] > nouveau_cout:
                            visite[etat] = nouveau_cout

                            nouveaux_bonus = bonus.copy()
                            cell = lab.case(nx1, ny1)
                            if cell == "Bs":
                                nouveaux_bonus["Bs"] += 1
                            elif cell == "Bp":
                                nouveaux_bonus["Bp"] += 1

                            q.append(((nx1, ny1), chemin + [f"Bs-{direction}"], frites_used + 1, nouveaux_bonus))

        return meilleur_chemin, meilleur_frites, meilleur_bonus

    def parcourt_largeur_avec_biere(self, lab, depart, objectif, nb_bieres_dispo):
        """
        Parcourt en largeur qui intègre l'utilisation de bières (3 pas d'un coup).
        Retourne : (chemin, nb_bieres_utilisées, bonus_ramasses)
        """
        q = deque([(depart, [], 0, {"Bs": 0, "Bp": 0})])
        visite = {(depart, 0): 0}

        meilleur_chemin = None
        meilleur_cout = float('inf')
        meilleur_bieres = 0
        meilleur_bonus = {"Bs": 0, "Bp": 0}

        while q:
            pos, chemin, bieres_used, bonus = q.popleft()

            if pos == objectif:
                cout_actuel = len(chemin)
                if cout_actuel < meilleur_cout:
                    meilleur_cout = cout_actuel
                    meilleur_chemin = chemin
                    meilleur_bieres = bieres_used
                    meilleur_bonus = bonus.copy()
                continue

            x, y = pos

            # Mouvement normal
            for direction, (dx, dy) in [("N", (0, -1)), ("S", (0, 1)), ("E", (1, 0)), ("O", (-1, 0))]:
                nx, ny = x + dx, y + dy
                if lab.accessible(nx, ny):
                    etat = ((nx, ny), bieres_used)
                    nouveau_cout = len(chemin) + 1

                    if etat not in visite or visite[etat] > nouveau_cout:
                        visite[etat] = nouveau_cout

                        nouveaux_bonus = bonus.copy()
                        cell = lab.case(nx, ny)
                        if cell == "Bs":
                            nouveaux_bonus["Bs"] += 1
                        elif cell == "Bp":
                            nouveaux_bonus["Bp"] += 1

                        q.append(((nx, ny), chemin + [direction], bieres_used, nouveaux_bonus))

            # Utiliser une bière (3 mouvements)
            if bieres_used < nb_bieres_dispo:
                # Essayer toutes les combinaisons de 3 directions
                for d1 in ["N", "S", "E", "O"]:
                    dx1 = {"N": 0, "S": 0, "E": 1, "O": -1}[d1]
                    dy1 = {"N": -1, "S": 1, "E": 0, "O": 0}[d1]
                    pos1 = (x + dx1, y + dy1)

                    if not lab.accessible(*pos1):
                        continue

                    for d2 in ["N", "S", "E", "O"]:
                        dx2 = {"N": 0, "S": 0, "E": 1, "O": -1}[d2]
                        dy2 = {"N": -1, "S": 1, "E": 0, "O": 0}[d2]
                        pos2 = (pos1[0] + dx2, pos1[1] + dy2)

                        if not lab.accessible(*pos2):
                            continue

                        for d3 in ["N", "S", "E", "O"]:
                            dx3 = {"N": 0, "S": 0, "E": 1, "O": -1}[d3]
                            dy3 = {"N": -1, "S": 1, "E": 0, "O": 0}[d3]
                            pos3 = (pos2[0] + dx3, pos2[1] + dy3)

                            if not lab.accessible(*pos3):
                                continue

                            etat = (pos3, bieres_used + 1)
                            nouveau_cout = len(chemin) + 1

                            if etat not in visite or visite[etat] > nouveau_cout:
                                visite[etat] = nouveau_cout

                                nouveaux_bonus = bonus.copy()
                                for p in [pos1, pos2, pos3]:
                                    cell = lab.case(*p)
                                    if cell == "Bs":
                                        nouveaux_bonus["Bs"] += 1
                                    elif cell == "Bp":
                                        nouveaux_bonus["Bp"] += 1

                                q.append((pos3, chemin + [f"Bp-{d1}-{d2}-{d3}"], bieres_used + 1, nouveaux_bonus))

        return meilleur_chemin, meilleur_bieres, meilleur_bonus

    def simuler_position(self, pos, direction):
        """Calcule la position après un mouvement"""
        dx = {"N": 0, "S": 0, "E": 1, "O": -1}[direction]
        dy = {"N": -1, "S": 1, "E": 0, "O": 0}[direction]
        return (pos[0] + dx, pos[1] + dy)

    def evaluer_objectif(self, lab, ma_pos, objectif_pos):
        """Évalue un objectif avec le meilleur chemin possible (compare frites ET bières)"""
        cell = lab.case(*objectif_pos)
        if not cell.isdigit():
            return -99999, None, 0, None, None

        valeur_moule = int(cell)

        # Chercher le meilleur chemin avec frites
        chemin_frites, nb_frites_needed, bonus_frites = self.parcourt_largeur_avec_frites(
            lab, ma_pos, objectif_pos, self.frites
        )

        # Chercher le meilleur chemin avec bières
        chemin_bieres, nb_bieres_needed, bonus_bieres = self.parcourt_largeur_avec_biere(
            lab, ma_pos, objectif_pos, self.bieres
        )

        # Comparer les deux stratégies
        meilleur_score = -99999
        meilleur_chemin = None
        meilleur_bonus_used = 0
        meilleur_bonus_collectes = None
        type_bonus = None

        # Évaluer le chemin avec frites
        if chemin_frites:
            bonus_score_f = bonus_frites["Bs"] * 3 + bonus_frites["Bp"] * 5
            score_frites = (valeur_moule * 10 + bonus_score_f - len(chemin_frites) * 0.3
                            - nb_frites_needed * 0.5)
            if score_frites > meilleur_score:
                meilleur_score = score_frites
                meilleur_chemin = chemin_frites
                meilleur_bonus_used = nb_frites_needed
                meilleur_bonus_collectes = bonus_frites
                type_bonus = "frites"

        # Évaluer le chemin avec bières
        if chemin_bieres:
            bonus_score_b = bonus_bieres["Bs"] * 3 + bonus_bieres["Bp"] * 5
            # Les bières permettent 3 mouvements en 1 coup, donc très efficace
            score_bieres = (valeur_moule * 10 + bonus_score_b - len(chemin_bieres) * 0.3
                            - nb_bieres_needed * 0.4)  # Légèrement moins pénalisant que les frites
            if score_bieres > meilleur_score:
                meilleur_score = score_bieres
                meilleur_chemin = chemin_bieres
                meilleur_bonus_used = nb_bieres_needed
                meilleur_bonus_collectes = bonus_bieres
                type_bonus = "bieres"

        if not meilleur_chemin:
            return -99999, None, 0, None, None

        return meilleur_score, meilleur_chemin, meilleur_bonus_used, meilleur_bonus_collectes, type_bonus

    def trouver_meilleur_objectif(self, lab, ma_pos):
        """Trouve la meilleure moule avec le meilleur chemin (compare frites ET bières)"""
        meilleur_score = -99999
        meilleur_chemin = None
        meilleur_bonus_used = 0
        meilleur_bonus_collectes = None
        meilleur_type = None

        for y in range(lab.hauteur):
            for x in range(lab.largeur):
                cell = lab.case(x, y)
                if cell.isdigit():
                    score, chemin, bonus_used, bonus_collectes, type_bonus = self.evaluer_objectif(
                        lab, ma_pos, (x, y)
                    )
                    if score > meilleur_score:
                        meilleur_score = score
                        meilleur_chemin = chemin
                        meilleur_bonus_used = bonus_used
                        meilleur_bonus_collectes = bonus_collectes
                        meilleur_type = type_bonus

        return meilleur_chemin, meilleur_bonus_used, meilleur_bonus_collectes, meilleur_type

    def predire_collecte(self, lab, pos):
        """Prédit et met à jour l'inventaire pour la case donnée"""
        cell = lab.case(*pos)
        if cell == "Bs":
            self.frites += 1
            print(f"  → 🍟 +1 frite (total: {self.frites})")
        elif cell == "Bp":
            self.bieres += 1
            print(f"  → 🍺 +1 bière (total: {self.bieres})")
        elif cell.isdigit():
            print(f"  → 🐚 +{cell} moules")

    def executer_mouvement_frite(self, lab, ma_pos, coup):
        """Simule un mouvement avec frite et collecte les bonus"""
        # Format: "Bs-N" ou "Bs-S" etc.
        direction = coup.split("-")[1]
        dx = {"N": 0, "S": 0, "E": 1, "O": -1}[direction]
        dy = {"N": -1, "S": 1, "E": 0, "O": 0}[direction]

        pos_inter = (ma_pos[0] + dx, ma_pos[1] + dy)
        pos_final = (ma_pos[0] + 2 * dx, ma_pos[1] + 2 * dy)

        # Collecter sur la case intermédiaire (si accessible ou mur avec bonus)
        self.predire_collecte(lab, pos_inter)

        # Collecter sur la case finale (si on y arrive)
        if lab.accessible(*pos_final):
            self.predire_collecte(lab, pos_final)
        elif lab.accessible(*pos_inter):
            # On s'arrête à la case intermédiaire
            pass

    def executer_mouvement_biere(self, lab, ma_pos, coup):
        """Simule un mouvement avec bière et collecte les bonus"""
        # Format: "Bp-N-S-E"
        parts = coup.split("-")
        directions = parts[1:4]

        pos = ma_pos
        for direction in directions:
            pos = self.simuler_position(pos, direction)
            self.predire_collecte(lab, pos)

    def choisir_coup(self, lab, moi):
        ma_pos = lab.joueurs[moi]

        print(f"\n🎮 Tour à {ma_pos} | 🍟 {self.frites} | 🍺 {self.bieres}")

        # Chercher le meilleur chemin en comparant frites ET bières
        chemin, bonus_needed, bonus_collectes, type_bonus = self.trouver_meilleur_objectif(lab, ma_pos)

        if chemin and len(chemin) > 0:
            premier_coup = chemin[0]

            if type_bonus == "frites":
                print(f"🎯 Stratégie FRITES: {len(chemin)} coups, {bonus_needed} frites nécessaires")
            elif type_bonus == "bieres":
                print(f"🎯 Stratégie BIÈRES: {len(chemin)} coups, {bonus_needed} bières nécessaires")
            else:
                print(f"🎯 Chemin: {len(chemin)} coups")

            print(f"   Bonus en route: 🍟 {bonus_collectes['Bs']} | 🍺 {bonus_collectes['Bp']}")

            # Exécuter le premier coup du chemin optimal
            if premier_coup.startswith("Bs-"):
                # C'est un mouvement avec frite
                self.frites -= 1
                print(f"🍟 UTILISE FRITE ! (reste {self.frites})")
                self.executer_mouvement_frite(lab, ma_pos, premier_coup)
                return premier_coup

            elif premier_coup.startswith("Bp-"):
                # C'est un mouvement avec bière
                self.bieres -= 1
                print(f"🍺 UTILISE BIÈRE ! (reste {self.bieres})")
                self.executer_mouvement_biere(lab, ma_pos, premier_coup)
                return premier_coup

            else:
                # Mouvement normal
                prochaine_pos = self.simuler_position(ma_pos, premier_coup)
                self.predire_collecte(lab, prochaine_pos)
                return premier_coup

        # EXPLORATION si aucune moule visible
        print("🔍 Mode exploration")
        meilleur_score = -1
        meilleure_direction = None

        for d, (dx, dy) in [("N", (0, -1)), ("S", (0, 1)), ("E", (1, 0)), ("O", (-1, 0))]:
            nx, ny = ma_pos[0] + dx, ma_pos[1] + dy

            if lab.accessible(nx, ny):
                score = random.random()
                cell = lab.case(nx, ny)

                if cell == "Bs":
                    score += 10
                elif cell == "Bp":
                    score += 15
                elif cell.isdigit():
                    score += int(cell) * 20

                if score > meilleur_score:
                    meilleur_score = score
                    meilleure_direction = d

        if meilleure_direction:
            prochaine_pos = self.simuler_position(ma_pos, meilleure_direction)
            self.predire_collecte(lab, prochaine_pos)
            return meilleure_direction

        print("⚠️ Aucun mouvement possible")
        return "C"


def main():
    env = load_env_file('.env')
    ip = env.get('SERVEUR_IP', '127.0.0.1')
    port = int(env.get('SERVEUR_PORT', '1337'))
    nom = env.get('NOM_EQUIPE', 'GodMoules2025')

    s = socket.socket()
    s.connect((ip, port))
    f = s.makefile('rw', encoding='utf-8')

    f.write(nom + '\n')
    f.flush()
    joueur = int(f.readline().strip())
    print(f"🎮 Connecté → {nom} (Joueur {joueur})")

    ia = IA()

    try:
        while True:
            msg = f.readline().strip()
            if not msg or msg == "FIN":
                print("\n🏁 Partie terminée")
                break

            lab = Labyrinthe(msg)
            coup = ia.choisir_coup(lab, joueur)
            print(f"➡️  JOUE: {coup}\n")
            f.write(coup + '\n')
            f.flush()

    except Exception as e:
        print("❌ Erreur:", e)
        import traceback
        traceback.print_exc()
    finally:
        s.close()


if __name__ == "__main__":
    main()