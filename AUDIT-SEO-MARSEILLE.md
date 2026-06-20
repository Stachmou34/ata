# Audit SEO & Plan d'action — assurancetemporaireauto.com
### Cible : assurance temporaire / frontière à MARSEILLE — voyageurs ferry du Maghreb, plaques étrangères, import
**Date :** 20 juin 2026
**Exploitant :** MCJ COURTAGE (ORIAS 26008651) — 12 rue Clément Ader, 34290 Abeilhan
**Langues cibles :** Français + Arabe

---

## 0. Résumé exécutif (TL;DR)

Le site est aujourd'hui un **one-pager générique** sur l'assurance temporaire. Il ne contient **aucune mention** de Marseille, du ferry, de la frontière, du Maghreb ni des plaques étrangères — alors que **c'est exactement le marché visé**. Les concurrents qui rankent (maghrebassurance.fr, assurance-voiture-temporaire-provisoire.com, elvire-broker.com, a2dassurances.fr) ont des **pages dédiées de 1 500–2 000 mots** par intention, avec FAQ, prix, ports cités et réassurance.

**Le levier n°1 = passer d'1 page à une architecture de pages dédiées (silo), bilingue FR/AR, géolocalisée Marseille + ports du Maghreb.**

Priorités :
1. **Quick wins techniques** (title/meta, canonical, Schema, NAP cohérent) — 1 semaine.
2. **Créer les pages piliers** (4 cibles) — 2 à 4 semaines.
3. **Contenu blog longue traîne + version arabe** — en continu.
4. **SEO local Marseille + netlinking** — en continu.

---

## 1. Audit technique de l'existant

### 1.1 Ce qui va
- HTTPS actif, HSTS, en-têtes de sécurité présents (X-Frame-Options, X-Content-Type-Options).
- `robots.txt` présent et propre, `sitemap.xml` déclaré.
- `lang="fr-FR"` correct, balise viewport mobile présente.
- Page légère (~59 Ko HTML).

### 1.2 Problèmes à corriger (par ordre d'impact)

| # | Problème | Impact SEO | Correctif |
|---|----------|-----------|-----------|
| 1 | `<title>` = « Assurance Temporaire Auto » (générique, pas de géo) | 🔴 Majeur | Réécrire avec Marseille + frontière (voir §3) |
| 2 | Aucune mention Marseille / ferry / frontière / Maghreb / plaque étrangère dans le contenu | 🔴 Majeur | Réécriture + nouvelles pages (§2, §4) |
| 3 | Site = 1 seule page de contenu (sitemap = 2 URL) | 🔴 Majeur | Architecture multi-pages (§2) |
| 4 | Aucune donnée structurée Schema.org | 🟠 Important | JSON-LD `InsuranceAgency` + `FAQPage` (§3.3) |
| 5 | Pas de version arabe, pas de `hreflang` | 🟠 Important | Sous-dossier `/ar/` + hreflang (§5) |
| 6 | NAP incohérent : tél. accueil `04 67 36 72 01` ≠ mentions `09 70 71 36 93` | 🟠 Important | Un seul numéro partout (NAP unique) |
| 7 | `canonical` en `www.` mais `og:url` en non-`www` | 🟡 Moyen | Choisir UNE version (recommandé : sans `www`) et rediriger l'autre en 301 |
| 8 | `og:title` = « ACCEUIL » (+ faute « ACCEUIL » dans le menu) | 🟡 Moyen | Corriger en « Accueil » + og:title descriptif |
| 9 | Hiérarchie Hn faible (plusieurs H2 sans H1 clair) | 🟡 Moyen | 1 seul H1 par page, structure logique |
| 10 | CSP potentiellement malformée (`script-src''`) | 🟡 À vérifier | Vérifier que le JS (formulaire, tracking) n'est pas bloqué |
| 11 | URLs en `.html` (`index.html`) | 🟢 Mineur | Idéalement URLs propres `/assurance-frontiere-marseille/` |
| 12 | Fautes d'orthographe (« Assitance », « ACCEUIL ») | 🟢 Mineur mais nuit à la confiance | Relecture complète |

### 1.3 À mesurer avant/après (mettre en place dès maintenant)
- **Google Search Console** + **Bing Webmaster Tools** : soumettre le sitemap, suivre l'indexation.
- **Google Analytics 4** (ou Matomo, RGPD-friendly).
- **PageSpeed Insights / Lighthouse** : mesurer les Core Web Vitals (LCP, CLS, INP) mobile.
- Vérifier l'indexation actuelle : `site:assurancetemporaireauto.com` sur Google.

---

## 2. Architecture cible (silo)

Passer du one-pager à une arborescence claire. Chaque **page pilier** cible une intention et reçoit les articles de blog en maillage.

```
/ (accueil — repositionnée : assurance temporaire & frontière, mise en avant Marseille/Maghreb)
│
├── /assurance-frontiere-marseille/            ← PILIER 1 (ferry Maghreb) ⭐ priorité absolue
│     ├── /assurance-frontiere-algerie/        (plaque DZ, ports Oran/Alger/Béjaïa/Skikda/Mostaganem)
│     ├── /assurance-frontiere-tunisie/        (plaque TN, port de Tunis)
│     └── /assurance-frontiere-maroc/          (plaque MA)
│
├── /assurance-temporaire-plaque-etrangere/    ← PILIER 2 (véhicule immatriculé à l'étranger en France/UE)
│     └── /assurance-plaque-ww/                (plaque WW / transit)
│
├── /assurance-frontiere-import-vehicule/      ← PILIER 3 (import / passage frontière hors UE)
│
├── /assurance-temporaire-marseille/           ← PILIER 4 (local générique Marseille + Bouches-du-Rhône)
│
├── /souscription/   (tunnel de souscription, optimisé conversion)
├── /tarifs/         (grille de prix / durées 1–90 jours)
├── /faq/            (FAQ globale, balisée FAQPage)
├── /blog/           (longue traîne — voir §4.3)
├── /contact/
├── /mentions-legales.html
│
└── /ar/             ← miroir arabe des pages clés (hreflang)
```

**Maillage interne :** chaque pilier lie vers ses sous-pages + 2-3 articles de blog ; le blog renvoie vers le pilier (ancres descriptives, pas « cliquez ici »).

---

## 3. Quick wins techniques (semaine 1)

### 3.1 Balises title / meta à déployer (exemples prêts à l'emploi)

**Accueil :**
- `title` : `Assurance temporaire & frontière auto à Marseille | 1 à 90 jours`
- `meta description` : `Assurance auto temporaire et frontière à Marseille pour véhicule étranger (plaque DZ, TN, MA) arrivé en ferry. Attestation immédiate en ligne, de 1 à 90 jours. Devis gratuit.`

**Pilier 1 — Frontière Marseille :**
- `title` : `Assurance frontière Marseille : rouler en France avec une plaque DZ ou TN`
- `meta` : `Vous débarquez du ferry à Marseille avec votre voiture algérienne ou tunisienne ? Souscrivez une assurance frontière obligatoire, attestation immédiate, 30 ou 90 jours.`

**Pilier 2 — Plaque étrangère :**
- `title` : `Assurance temporaire véhicule plaque étrangère en France | Devis immédiat`
- `meta` : `Assurez temporairement (1 à 90 jours) un véhicule immatriculé à l'étranger circulant en France ou en Europe. Souscription en ligne, attestation immédiate.`

### 3.2 Cohérence technique
- Choisir **une version canonique** : `https://assurancetemporaireauto.com/` (sans `www`) → redirection 301 du `www` et alignement `canonical` + `og:url`.
- **Un seul numéro de téléphone** partout (homepage = mentions légales = GBP = Schema). C'est un signal NAP critique pour le local.
- Corriger « ACCEUIL » → « Accueil », « Assitance » → « Assistance ».

### 3.3 Données structurées (JSON-LD à injecter dans le `<head>`)

```json
{
  "@context": "https://schema.org",
  "@type": "InsuranceAgency",
  "name": "Assurance Temporaire Auto — MCJ Courtage",
  "url": "https://assurancetemporaireauto.com/",
  "telephone": "+33970713693",
  "image": "https://assurancetemporaireauto.com/logo.png",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "12 rue Clément Ader",
    "postalCode": "34290",
    "addressLocality": "Abeilhan",
    "addressCountry": "FR"
  },
  "areaServed": ["Marseille", "Bouches-du-Rhône", "France", "Europe"],
  "openingHours": "Mo-Fr 09:00-18:00",
  "knowsLanguage": ["fr", "ar"],
  "priceRange": "€€"
}
```
+ ajouter un bloc **`FAQPage`** sur chaque page comportant une FAQ (éligible aux résultats enrichis Google).

> ⚠️ **Note importante SEO local :** l'adresse officielle est à **Abeilhan (Hérault)**, pas à Marseille. Le *map pack* Google (top 3 cartes) se déclenche surtout sur proximité physique → difficile de l'emporter sur « assurance Marseille » sans présence à Marseille. Deux options (§6.2) : (a) **stratégie « zone desservie »** + contenu fort (réaliste, recommandé), ou (b) **adresse/partenaire à Marseille** si possible. Le SEO **organique** (pages + contenu) reste lui pleinement gagnable.

---

## 4. Stratégie de contenu & mots-clés

### 4.1 Mots-clés français prioritaires (par intention)

**Pilier 1 — Ferry Maghreb (intention transactionnelle forte) :**
- assurance frontière Marseille
- assurance temporaire voiture algérienne / tunisienne
- assurance plaque DZ / TN en France
- assurance frontière Algérie / Tunisie / Maroc
- assurance voiture ferry Marseille
- assurance au débarquement du ferry Marseille
- assurance temporaire au passage de la frontière auto France-Algérie

**Pilier 2 — Plaque étrangère :**
- assurance temporaire véhicule plaque étrangère
- assurer une voiture immatriculée à l'étranger en France
- assurance plaque WW / véhicule en transit
- assurance temporaire voiture étrangère

**Pilier 3 — Import / frontière hors UE :**
- assurance frontière import véhicule
- assurance obligatoire entrée territoire français véhicule étranger
- assurance temporaire importation voiture
- assurance frontière Carte Verte

**Pilier 4 — Local Marseille :**
- assurance temporaire Marseille
- assurance auto provisoire Marseille / Bouches-du-Rhône
- assurance 1 jour / 7 jours / 30 jours Marseille

### 4.2 Mots-clés arabes (version /ar/)
- تأمين مؤقت سيارة فرنسا (assurance temporaire voiture France)
- تأمين الحدود مرسيليا (assurance frontière Marseille)
- تأمين سيارة جزائرية في فرنسا (assurer voiture algérienne en France)
- تأمين لوحة أجنبية فرنسا (assurance plaque étrangère France)
- تأمين سيارة عند النزول من الباخرة مرسيليا (assurance au débarquement du ferry Marseille)

> La concurrence en **arabe est quasi inexistante** sur ce créneau → **opportunité forte** pour capter les voyageurs avant le départ (recherches faites depuis l'Algérie/Tunisie sur mobile).

### 4.3 Idées d'articles de blog (longue traîne, à publier régulièrement)
1. « Débarquer en ferry à Marseille avec sa voiture : quelle assurance ? » (FR + AR)
2. « Combien de temps peut-on rouler en France avec une plaque algérienne / tunisienne ? » (6 mois max)
3. « Ports Algérie/Tunisie → Marseille : durées, compagnies, formalités »
4. « Assurance frontière vs assurance temporaire : laquelle choisir ? »
5. « Que faire en cas de contrôle police/douane à la sortie du ferry à Marseille ? »
6. « Importer un véhicule du Maghreb : assurance, carte grise, délais »
7. « Plaque WW / véhicule en transit : comment l'assurer en France ? »
8. « Tarifs assurance frontière 2026 : 1, 7, 30, 90 jours »

Chaque page/article doit contenir : un **H1 unique**, des **H2 structurés**, une **FAQ** (3-6 questions), des **prix/durées concrets**, les **ports cités** (Oran, Alger, Béjaïa, Skikda, Mostaganem, Tunis), un **CTA clair** (« Souscrire — attestation immédiate ») et un visuel. Cible : **1 200–2 000 mots** pour les piliers.

### 4.4 Réassurance / E-E-A-T (à afficher partout)
- N° **ORIAS 26008651** + mention ACPR (crédibilité réglementaire = clé sur l'assurance « YMYL »).
- Attestation **immédiate**, souscription **en ligne**, support FR/AR.
- Avis clients (Google / Trustpilot) — à collecter activement.
- Page « À propos » avec l'entreprise, les garanties, la transparence des prix.

---

## 5. Bilingue FR / AR (mise en œuvre)
- Créer un sous-dossier **`/ar/`** miroir des pages clés (pas une simple traduction auto : relecture par locuteur natif).
- `dir="rtl"` et `lang="ar"` sur les pages arabes.
- Balises **`hreflang`** réciproques sur chaque paire :
  ```html
  <link rel="alternate" hreflang="fr" href="https://assurancetemporaireauto.com/assurance-frontiere-marseille/" />
  <link rel="alternate" hreflang="ar" href="https://assurancetemporaireauto.com/ar/assurance-frontiere-marseille/" />
  <link rel="alternate" hreflang="x-default" href="https://assurancetemporaireauto.com/assurance-frontiere-marseille/" />
  ```
- Sélecteur de langue visible (FR / العربية) dans l'en-tête.

---

## 6. SEO local Marseille

### 6.1 Google Business Profile (GBP)
- Créer / optimiser la fiche : catégorie principale **« Agence d'assurance »**, zone desservie **Marseille + Bouches-du-Rhône**, horaires, téléphone NAP unique, site, photos, langues FR/AR.
- Publier des **posts GBP** réguliers (offres, FAQ ferry).
- Collecter des **avis** + y répondre (FR/AR).

### 6.2 Le point clé sur l'adresse
- Adresse officielle à **Abeilhan (34)** → la fiche GBP rankera localement autour de Béziers, pas Marseille.
- **Option A (réaliste)** : jouer la **zone desservie** + le SEO organique (les pages piliers peuvent ranker sur « assurance frontière Marseille » même sans bureau là-bas, comme le font des concurrents nationaux).
- **Option B** : disposer d'une **adresse / partenaire physique à Marseille** (bureau, point relais près du port) → ouvre le *map pack* Marseille. À évaluer selon le business.

### 6.3 Citations / annuaires (NAP cohérent partout)
- PagesJaunes, Yelp, annuaires assurance, ORIAS, annuaires communautaires maghrébins en France.
- Forums/groupes Facebook « Algériens/Tunisiens en France », communautés voyage ferry.

---

## 7. Netlinking (hors-site)
- Articles invités / partenariats avec sites de **voyage ferry Maghreb**, agences de traversée, forums de la diaspora.
- Liens depuis les partenaires existants (JL Assure, Australdev, Seguro-Temporal) — déjà liés, vérifier la réciprocité.
- Communiqués / présence sur annuaires d'assurance et de courtage.
- Contenu « linkable » : guide complet « Venir en ferry au Maghreb → France avec sa voiture » (FR/AR).

---

## 8. Plan d'action priorisé (roadmap)

### 🟢 Semaine 1 — Quick wins (impact immédiat, faible effort)
- [ ] Mettre en place Search Console + GA4 + soumettre sitemap.
- [ ] Réécrire `title` + `meta description` de l'accueil (Marseille + frontière).
- [ ] Ajouter Marseille / ferry / frontière / Maghreb / plaque étrangère dans le contenu de l'accueil.
- [ ] Corriger NAP (un seul téléphone), canonical/og:url cohérents, fautes (« ACCEUIL », « Assitance »).
- [ ] Injecter le JSON-LD `InsuranceAgency` + `FAQPage`.
- [ ] Créer / optimiser la fiche Google Business Profile.

### 🟠 Semaines 2–4 — Pages piliers
- [ ] Pilier 1 : `/assurance-frontiere-marseille/` (1 500–2 000 mots, FAQ, ports, prix). ⭐
- [ ] Sous-pages DZ / TN / MA.
- [ ] Pilier 2 : plaque étrangère. Pilier 4 : Marseille local.
- [ ] Page tarifs + FAQ globale, mise à jour du sitemap.

### 🔵 Mois 2 — Bilingue + import
- [ ] Version arabe `/ar/` des pages clés + hreflang.
- [ ] Pilier 3 : import / frontière hors UE.
- [ ] Lancer le blog (2 premiers articles).

### 🟣 En continu — Autorité & contenu
- [ ] 2–4 articles de blog / mois (longue traîne FR + AR).
- [ ] Collecte d'avis, posts GBP, citations annuaires.
- [ ] Netlinking (partenariats ferry / diaspora).
- [ ] Suivi mensuel des positions et des Core Web Vitals.

---

## 9. KPIs de suivi (mensuel)
- Pages indexées (Search Console) — objectif : passer de ~2 à 15+.
- Positions sur les requêtes cibles (« assurance frontière Marseille », etc.).
- Clics / impressions organiques (Search Console), part FR vs AR.
- Conversions : souscriptions / demandes de devis depuis l'organique.
- Avis Google (nombre + note).
- Core Web Vitals mobile (LCP < 2,5 s, INP < 200 ms, CLS < 0,1).

---

## 10. Concurrents de référence (à surveiller / dépasser)
| Concurrent | Force principale |
|-----------|------------------|
| maghrebassurance.fr | Basé à Marseille, pages dédiées DZ/TN, fort sur le local |
| assurance-voiture-temporaire-provisoire.com | Contenu très riche (1 800+ mots/page), ACPR, 22 ans, gros blog |
| elvire-broker.com | Souscription en ligne immédiate, contenu frontière Algérie |
| a2dassurances.fr | Ciblage géo précis (« frontière auto France-Algérie à Marseille ») |
| mon-assurance-tempo.fr | Page frontière + plaques étrangères |

**Levier de différenciation pour toi : la version ARABE** (concurrence quasi nulle) + un contenu pratique ferry/port ultra-ciblé Marseille.
