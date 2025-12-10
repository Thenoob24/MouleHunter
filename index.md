---
layout: default
title: Accueil
permalink: /
---

# 🐚 Bienvenue sur MouleHunterAI

Votre assistant intelligent pour gagner la course aux moules !

---

## 🎮 C'est quoi ?

MouleHunterAI est un joueur automatique (un "bot") qui joue à un jeu de labyrinthe où le but est de collecter le plus de moules possible. Il prend les décisions à votre place et joue de manière intelligente pour gagner !

### Pourquoi c'est génial ?

**🏆 Gagne automatiquement**  
Pas besoin de réfléchir, le bot fait tout le travail ! Il choisit toujours les meilleurs chemins pour ramasser un maximum de moules.

**⚡ Réactions rapides**  
Le bot calcule instantanément la meilleure action à faire, plus vite qu'un humain ne pourrait le faire.

**🧠 Stratégie optimale**  
Il sait quand utiliser ses bonus (frites et bières) pour aller plus vite et collecter plus de moules.

---

## 🚀 Comment démarrer

### Étape 1 : Créer le fichier de configuration

Créez un fichier nommé `.env` et écrivez dedans :

```
SERVEUR_IP=127.0.0.1
SERVEUR_PORT=1337
NOM_EQUIPE=VotreNom
```

> 💡 **Astuce :** Remplacez "VotreNom" par le nom que vous voulez donner à votre équipe.

### Étape 2 : Lancer le programme

Ouvrez un terminal et tapez :

```bash
python main.py
```

### Étape 3 : Regarder le bot jouer

Le bot se connecte automatiquement au jeu et commence à jouer ! Vous verrez apparaître dans le terminal ce qu'il fait à chaque tour.

> 💡 **Astuce :** Gardez le terminal ouvert pour voir en temps réel ce que le bot décide de faire. C'est très instructif !

---

## 🎯 Comment ça marche

### Le but du jeu

Vous êtes dans un labyrinthe rempli de moules. Plus vous collectez de moules, plus vous gagnez de points ! Mais attention, d'autres joueurs essaient aussi d'en ramasser.

### Les éléments du jeu

#### 🐚 Les Moules

Ce sont vos objectifs principaux ! Chaque moule vaut des points (de 1 à 9). Plus le chiffre est élevé, plus elle vaut de points.

- `1` 🐚 → 1 point
- `5` 🐚 → 5 points
- `9` 🐚 → 9 points

#### 🧱 Les Murs

Vous ne pouvez pas passer à travers les murs. Il faut les contourner... sauf si vous avez des frites !

#### 🏃 Vos Déplacements

À chaque tour, vous pouvez bouger dans 4 directions :

- ⬆️ **Nord (N)**
- ⬇️ **Sud (S)**
- ➡️ **Est (E)**
- ⬅️ **Ouest (O)**

### Comment le bot choisit où aller

Le bot regarde toutes les moules disponibles sur le terrain et calcule pour chacune :

✓ Combien elle vaut en points  
✓ À quelle distance elle se trouve  
✓ S'il y a des bonus intéressants sur le chemin  
✓ S'il vaut mieux utiliser un bonus (frite ou bière) pour y arriver plus vite

Ensuite, il choisit automatiquement la moule qui lui rapportera le meilleur score !

---

## 🎁 Les Bonus Magiques

### 🍟 Les Frites (Bs)

**Pouvoir :** Sauter par-dessus un obstacle

Avec une frite, vous pouvez avancer de **2 cases en un seul mouvement**, même s'il y a un mur entre les deux ! C'est parfait pour prendre des raccourcis.

> 💡 **Bon à savoir :** Vous collectez automatiquement ce qui se trouve sur la case que vous sautez !

### 🍺 Les Bières (Bp)

**Pouvoir :** Sprint de 3 mouvements

Avec une bière, vous pouvez faire **3 mouvements d'affilée en un seul tour** ! C'est génial pour aller très loin très rapidement.

> 💡 **Exemple :** Vous pouvez faire Nord → Nord → Est pour avancer de 3 cases en un coup !

### 🤔 Comment le bot utilise les bonus

Le bot est malin ! Pour chaque moule qu'il veut collecter, il calcule deux chemins :

- **Chemin avec frites :** en utilisant des frites pour sauter par-dessus les obstacles
- **Chemin avec bières :** en utilisant des bières pour aller plus vite sur de longues distances

Ensuite, il compare les deux et choisit automatiquement la meilleure option ! Vous n'avez rien à faire, il gère tout seul.

---

## 💡 Astuces et Conseils

### 👀 Suivez les actions du bot

Dans le terminal, vous verrez des messages comme :

```
🎮 Tour à (5,3) | 🍟 2 | 🍺 1
🎯 Stratégie FRITES: 5 coups, 1 frites nécessaires
   Bonus en route: 🍟 1 | 🍺 0
🍟 UTILISE FRITE ! (reste 1)
  → 🐚 +5 moules
➡️  JOUE: Bs-N
```

Ces messages vous disent exactement ce que fait le bot !

### 📊 Comprendre les symboles

- 🎯 = L'objectif qu'il vise
- 🍟 = Nombre de frites en stock
- 🍺 = Nombre de bières en stock
- 🐚 = Moule collectée
- 🔍 = Mode exploration (cherche de nouvelles moules)

### 🔍 Mode exploration

Si le bot ne voit aucune moule, il passe en "mode exploration" et se déplace vers des zones inconnues pour découvrir de nouvelles moules.

Vous verrez le message :
```
🔍 Mode exploration
```

### 🏆 Stratégie gagnante du bot

Le bot prend toujours en compte :

✓ La **valeur des moules** : il préfère les grosses moules (7, 8, 9 points)  
✓ La **distance** : il évite d'aller trop loin pour une petite moule  
✓ Les **bonus sur le chemin** : s'il peut ramasser des frites ou bières en route, c'est encore mieux !  
✓ L'**économie de bonus** : il n'utilise pas bêtement toutes ses frites/bières, il les garde pour les meilleurs moments

> ⚠️ **Important :** Si le bot dit "Aucun mouvement possible", c'est qu'il est bloqué de tous les côtés. C'est rare, mais ça peut arriver dans des coins du labyrinthe !

---

## ❓ Questions Fréquentes

### Le bot peut-il perdre ?

Oui, si d'autres joueurs (humains ou bots) sont plus rapides ou collectent les meilleures moules avant lui. Mais il fait de son mieux pour gagner !

### Puis-je modifier la stratégie du bot ?

Oui ! En modifiant le fichier Python, vous pouvez changer comment le bot évalue les moules, combien il valorise les frites vs les bières, etc.

### Le bot apprend-il de ses erreurs ?

Non, pour l'instant il joue avec une stratégie fixe. Il ne "se souvient" pas des parties précédentes. Chaque partie est indépendante.

### Que faire si le bot ne se connecte pas ?

Vérifiez que :
- Le fichier `.env` existe bien dans le même dossier que `main.py`
- Les informations de connexion (IP et PORT) sont correctes
- Le serveur de jeu est bien lancé

---

## 📊 Exemple d'une partie

Voici à quoi ressemble une partie typique dans le terminal :

```
🎮 Connecté → GodMoules2025 (Joueur 0)

🎮 Tour à (2,3) | 🍟 0 | 🍺 0
🎯 Chemin: 3 coups
   Bonus en route: 🍟 1 | 🍺 0
  → 🍟 +1 frite (total: 1)
➡️  JOUE: E

🎮 Tour à (3,3) | 🍟 1 | 🍺 0
🎯 Stratégie FRITES: 2 coups, 1 frites nécessaires
   Bonus en route: 🍟 0 | 🍺 0
🍟 UTILISE FRITE ! (reste 0)
  → 🐚 +7 moules
➡️  JOUE: Bs-N

🎮 Tour à (3,1) | 🍟 0 | 🍺 1
🎯 Stratégie BIÈRES: 1 coups, 1 bières nécessaires
   Bonus en route: 🍟 0 | 🍺 0
🍺 UTILISE BIÈRE ! (reste 0)
  → 🐚 +9 moules
➡️  JOUE: Bp-E-E-N

🏁 Partie terminée
```

---

## 🔧 Structure du projet

```
mon-projet/
│
├── main.py          # Le code principal du bot
├── .env             # Vos paramètres de connexion
└── README.md        # Ce fichier !
```

---

## 🎓 Ce que vous apprenez avec ce projet

En utilisant et en étudiant ce bot, vous découvrez :

- 💭 Comment une "intelligence artificielle" prend des décisions
- 🗺️ Comment trouver le chemin le plus court dans un labyrinthe
- 🎯 Comment optimiser des choix entre plusieurs options
- 🔄 Comment un programme peut jouer à un jeu automatiquement
- 🧮 Comment comparer différentes stratégies pour choisir la meilleure

---

## 📝 Crédits

Projet étudiant développé pour apprendre le fonctionnement des intelligences artificielles appliquées aux jeux.

**Technologies utilisées :** Python, Socket (pour la connexion réseau)

---

[⬆️ Retour en haut](#-bienvenue-sur-godmoules2025)