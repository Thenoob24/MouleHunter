---
title: Comment ça marche
nav_order: 3
---

# Comment ça marche

### Le but du jeu
Labyrinthe + moules + autres joueurs = course aux points !

### Les éléments du terrain
| Symbole | Signification                  | Points |
|--------|--------------------------------|--------|
| `1`–`9`| Moules                         | 1 à 9  |
| `#`    | Mur                            | —      |
| ` `    | Case vide                      | —      |

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