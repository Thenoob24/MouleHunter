---
title: Astuces & Conseils
nav_order: 5
---

# Astuces & Conseils

### Suivre les actions du bot en direct

Le bot est très bavard (dans le bon sens !). Voici un exemple de ce que tu verras :

Tour à (5,3) | 2 frites | 1 bière
Stratégie FRITES: 5 coups, 1 frite nécessaire
Bonus en route: +1 frite | +0 bière
UTILISE FRITE ! (reste 1)
+5 moules
JOUE: Bs-N


### Comprendre les symboles dans les logs

| Symbole | Signification                          |
|--------|----------------------------------------|
| Target | La moule que le bot vise actuellement             |
| Fries  | Nombre de frites en stock                |
| Beer   | Nombre de bières en stock                |
| Mussel | Moule collectée                          |
| Search | Mode exploration activé                  |

### Mode exploration

Quand plus aucune moule n’est visible à proximité :

→ Le bot se dirige intelligemment vers les zones encore inexplorées pour trouver de nouvelles moules.

### La stratégie gagnante du bot

Il priorise toujours dans cet ordre :
1. Moules 7-8-9 points en priorité absolue
2. Distance raisonnable (il n’ira pas à l’autre bout de la carte pour une moule 1)
3. Bonus ramassés en chemin (une frite ou bière gratuite = jackpot)
4. Économie de bonus : il garde précieusement ses frites/bièges pour les gros coups

**Important** : Si tu vois ce message (très rare) :

### Aucun mouvement possible

→ Le bot est coincé dans un coin. Ça arrive parfois, mais il se libérera dès qu’un chemin s’ouvre.
