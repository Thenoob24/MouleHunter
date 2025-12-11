---
title: CLes règles du jeu
nav_order: 3
---

# Comment ça marche

### Le but du jeu
Un labyrinthe avec des moules et différent bonus sont générés aléatoirement 
et le but du jeu est de collecter toutes les moules pour obtenir le plus de point.


## 🗺️ Les éléments du terrain
| Symbole    | Signification   | Points |
|------------|-----------------|--------|
| `1`–`9`    | 🐚 Moules        | 1 à 9  |
| `#`        | 🧱 Mur           | —      |
| *(espace)* | ▫️ Case vide     | —      |
| `🍟`       | 🍟 Bonus frites  | —      |
| `🍺`       | 🍺 Bonus bières  | —      |



### Déplacements possibles
- **N**ord, **S**ud, **E**st, **O**uest  
- `Bs-X` → utiliser une frite pour sauter dans la direction X  
- `Bp-X-Y-Z` → utiliser une bière pour faire 3 mouvements d’un coup

### Intelligence du bot
À chaque tour, il :
1. Repère toutes les moules visibles
2. Calcule le coût (distance + bonus nécessaires)
3. Évalue le gain (valeur moule + bonus ramassés en chemin)
4. Choisit la cible qui donne le **meilleur ratio gain/coût**
5. Décide automatiquement s’il vaut mieux utiliser des **frites** ou une **bière**