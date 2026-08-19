# Veille concurrentielle — Assurance frontière (prix)

**Dernier relevé : 19/08/2026** — précédent : 24/07/2026. À rafraîchir tous les 1 à 2 mois.

**Usage : INTERNE.** Sur le site public les concurrents ne sont jamais nommés. La publicité
comparative est licite (art. L.122-1 s. du Code de la consommation) mais impose objectivité et
vérifiabilité : d'où l'anonymisation « Concurrent 1/2/3/4 » et la note datée sous le comparatif.

## Notre grille (aman-frontiere.com)
| Véhicule | 30 jours | €/jour | 90 jours | €/jour |
|---|---|---|---|---|
| ≤ 30 CV | **140 €** | **4,67 €** | **340 €** | **3,78 €** |
| > 30 CV | **150 €** | **5,00 €** | **370 €** | **4,11 €** |

## Prix concurrents constatés — 19/08/2026
Le prix par jour est recalculé par nous à partir de leur prix total, pour comparer à
méthode identique. Quand ils l'affichent eux-mêmes, la colonne le signale.

| Rang | Site | 30 jours | €/jour | 90 jours | €/jour | Où c'est affiché |
|---|---|---|---|---|---|---|
| Concurrent 1 | elvire-broker.com | **158 €** TTC | 5,27 € | sur devis | — | Article « Assurance frontière Algérie » — tableau tarifs |
| Concurrent 2 | atel.fr | **169 €** | 5,63 € | n.c. | — | `/page/assurance-frontiere` (219 € pour SUV/4x4) |
| Concurrent 3 | assurance-voiture-temporaire-provisoire.com (AED) | **171,30 €** | 5,71 € *(affiché)* | **376,35 €** | 4,18 € *(ils affichent 4,53 € — voir ci-dessous)* | `/assurance-frontiere.html` |
| Concurrent 4 | maghrebassurance.fr | **175,00 €** | 5,83 € *(affiché)* | **390,00 €** | 4,33 € *(affiché)* | `/assurance-auto/assurance-temporaire/assurance-frontiere/` |
| — | mon-assurance-tempo.fr | **plus affiché** | — | n.c. | — | Le « à partir de 182 € » de juillet a disparu |

**30 j : 158 € → 175 €** · moyenne **168 €** (soit **5,60 €/jour**)
**90 j : 376,35 € → 390 €** · soit **4,18 € → 4,33 €/jour**

### Incohérence relevée chez AED
Leur accroche annonce « dès 4,53 €/jour » pour 90 jours, mais leur propre exemple donne
376,35 € TTC sur 90 jours, soit **4,18 €/jour**. 4,53 × 90 = 407,70 €, pas 376,35 €.
Leur prix par jour réel est donc plus bas que celui qu'ils mettent en avant. À ne pas
utiliser contre eux sur le site : c'est une erreur de leur part, pas un argument
défendable, et elle peut être corrigée du jour au lendemain.

## Notre avantage
- 30 jours : **−18 € à −35 €** (−11 % à −20 %) — le tarif le plus bas relevé
- 90 jours : **−36 € à −50 €** (−10 % à −13 %)
- Au jour : **4,67 €** contre 5,27 € à 5,83 € ailleurs ; sur 90 jours **3,78 €** contre 4,18 € à 4,33 €
- C'est sur le prix par jour à 90 jours que l'écart est le plus net : **−10 % à −13 %**,
  et c'est l'argument que les concurrents mettent eux-mêmes en avant

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
3. Mettre à jour dans `index.html` **et** `ar/index.html` : `duel-p strike`, `.duel-day`,
   `duel-save`, `.mkt`, les `small` de prix par jour dans les `.price-line`, les 5 `bar-row`,
   `.perday`, `.compare-note`, la date de la `.legal-note`.
4. Largeur des barres proportionnelle au prix, base 0, plafond = prix max → 80 %
   (formule : `round(prix / prix_max * 80)`).
5. Reporter le relevé dans ce fichier avec la date.

> Si un prix cité sur le site n'est plus affiché chez le concurrent, il faut le retirer sans
> attendre : une comparaison non vérifiable est le principal risque juridique de cette page.
