# Veille concurrentielle — Assurance frontière (prix)

**Dernier relevé : 19/08/2026** — précédent : 24/07/2026. À rafraîchir tous les 1 à 2 mois.

**Usage : INTERNE.** Sur le site public les concurrents ne sont jamais nommés. La publicité
comparative est licite (art. L.122-1 s. du Code de la consommation) mais impose objectivité et
vérifiabilité : d'où l'anonymisation « Concurrent 1/2/3/4 » et la note datée sous le comparatif.

## Notre grille (aman-frontiere.com)
| Véhicule | 30 jours | 90 jours |
|---|---|---|
| ≤ 30 CV | **140 €** | **340 €** |
| > 30 CV | **150 €** | **370 €** |

## Prix concurrents constatés — 19/08/2026
| Rang | Site | 30 jours | 90 jours | Où c'est affiché |
|---|---|---|---|---|
| Concurrent 1 | elvire-broker.com | **158 €** TTC | sur devis | Article « Assurance frontière Algérie » — tableau tarifs |
| Concurrent 2 | atel.fr | **169 €** | n.c. | `/page/assurance-frontiere` — « à partir de 169 € pour 30 jours » (219 € pour SUV/4x4) |
| Concurrent 3 | assurance-voiture-temporaire-provisoire.com (AED) | **171,30 €** (5,71 €/j) | **376,35 €** (4,53 €/j) | `/assurance-frontiere.html` — tableau Durée / Tarif TTC |
| Concurrent 4 | maghrebassurance.fr | **175,00 €** (5,83 €/j) | **390,00 €** (4,33 €/j) | `/assurance-auto/assurance-temporaire/assurance-frontiere/` — tableau tarifs |
| — | mon-assurance-tempo.fr | **plus affiché** | n.c. | Le « à partir de 182 € » de juillet a disparu du site |

**Fourchette marché 30 j : 158 € → 175 €** · **moyenne 168 €**
**Fourchette marché 90 j : 376,35 € → 390 €**

## Notre avantage
- 30 jours : **−18 € à −35 €** (−11 % à −20 %) — nous restons le tarif le plus bas relevé
- 90 jours : **−36 € à −50 €** (−10 % à −13 %)

## Évolution depuis le 24/07/2026
| Point | Juillet | Août | Conséquence |
|---|---|---|---|
| Plancher du marché | 169 € | **158 €** | l'écart se resserre, nous restons devant |
| Plafond affiché | 182 € | **175 €** | le 182 € n'était plus vérifiable → retiré du site |
| atel.fr | inaccessible (403) | accessible, 169 € | nouveau concurrent identifié |
| maghrebassurance 90 j | n.c. | 390 € | permet enfin de comparer sur 90 jours |
| elvire-broker | prix non publiés | 158 € | devient le concurrent le moins cher |

## Concurrence SEO (hors prix)
- **assurance-voiture-temporaire-provisoire.com** publie une page dédiée
  « Assurance frontière Marseille : rouler en France avec un véhicule algérien ou tunisien » :
  concurrent frontal sur notre mot-clé principal.
- **elvire-broker.com** a une arborescence par port
  (`/assurance-auto-temporaire-frontiere-algerie-port/alger`, `/oran`, `/bejaia`, `/annaba`,
  `/mostaganem`…) : stratégie de pages locales que nous n'avons pas.

## Ce qui est affiché sur le site public
- Bandeau héros : « Prix moyen constaté chez nos concurrents **168 €** » (moyenne des 4 relevés)
  barré, face à nos 140 €, et « Jusqu'à 35 € d'économie ».
- Section `#tarifs` : « Ailleurs : de 158 € à 175 € les 30 jours* », 5 barres comparatives
  anonymisées, « Jusqu'à 35 € d'économie sur 30 jours — et jusqu'à 50 € sur 90 jours ».
- Note légale datée du 19/08/2026 sous le comparatif, FR et AR.

## Checklist de mise à jour
1. Re-relever les 5 sites ci-dessus (les tableaux de prix, pas les pages d'accueil).
2. Recalculer moyenne, min et max sur 30 jours ; idem sur 90 jours.
3. Mettre à jour dans `index.html` **et** `ar/index.html` : `duel-p strike`, `duel-save`,
   `.mkt`, les 5 `bar-row`, `.compare-note`, la date de la `.legal-note`.
4. Largeur des barres proportionnelle au prix, base 0, plafond = prix max → 80 %
   (formule : `round(prix / prix_max * 80)`).
5. Reporter le relevé dans ce fichier avec la date.

> Si un prix cité sur le site n'est plus affiché chez le concurrent, il faut le retirer sans
> attendre : une comparaison non vérifiable est le principal risque juridique de cette page.
