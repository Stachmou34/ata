#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Met a jour data/traversees.json a partir des horaires publies par les compagnies.

Source actuelle : la grille horaire officielle de Corsica Linea
(https://www.corsicalinea.com/reserver/infos-lignes-et-horaires), publiee par la
compagnie elle-meme et autorisee par son robots.txt. On n'en garde que les
traversees qui ARRIVENT a Marseille ou a Sete depuis l'Algerie ou la Tunisie :
ce sont les seules qui concernent nos clients.

Les colonnes sont reperees par leur en-tete, pas par leur position : la
compagnie a deja reorganise son tableau une fois (juillet 2026) et cela suffit
a casser un parseur qui compte les colonnes.

Les autres compagnies (Algerie Ferries, GNV, CTN, Balearia) ne publient pas de
grille exploitable automatiquement : leurs departs restent a saisir a la main
dans data/traversees.json. Ce script ne touche jamais aux departs dont la
source n'est pas la sienne.

Usage : python3 .github/scripts/maj-traversees.py [--dry-run]
"""

import io
import json
import os
import re
import sys
import unicodedata
import urllib.request
from datetime import datetime

URL = "https://www.corsicalinea.com/reserver/infos-lignes-et-horaires"
SOURCE = "corsica-linea"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/126.0.0.0 Safari/537.36")

# Codes de la compagnie -> cles de notre fichier de donnees
PORTS = {
    "MRS": "marseille", "SET": "sete",
    "ALG": "alger", "BEJ": "bejaia", "SKI": "skikda", "ORA": "oran",
    "ANN": "annaba", "TUN": "tunis",
}
ARRIVEES = {"marseille", "sete"}          # on ne garde que les arrivees en France
COMPAGNIE = {"SNCM": "corsica-linea"}

# En-tetes acceptes pour chaque donnee dont on a besoin (accents et casse ignores)
COLONNES = {
    "depart":      ("date de depart",),
    "arrivee":     ("date d'arrivee",),
    "navire":      ("navire",),
    "code_depart": ("code depart",),
    "code_arrivee": ("code arrivee",),
    "code_cie":    ("code compagnie",),
}
# format "19.08.26 a 08:30"
MOMENT_RE = re.compile(r"(\d{2})\.(\d{2})\.(\d{2}).{0,4}?(\d{1,2}):(\d{2})")


def sans_accent(s):
    s = unicodedata.normalize("NFD", s)
    return u"".join(c for c in s if unicodedata.category(c) != "Mn").lower().strip()


def texte(html):
    html = re.sub(r"<[^>]+>", " ", html)
    html = html.replace("&#039;", "'").replace("&#39;", "'").replace("&amp;", "&")
    return re.sub(r"\s+", " ", html).strip()


def parse_moment(s):
    m = MOMENT_RE.search(s)
    if not m:
        return None
    j, mo, a, h, mn = (int(x) for x in m.groups())
    try:
        return datetime(2000 + a, mo, j, h, mn)
    except ValueError:
        return None


def duree(depart, arrivee):
    if not (depart and arrivee) or arrivee <= depart:
        return None
    h, mn = divmod(int((arrivee - depart).total_seconds() // 60), 60)
    return u"%d h %02d" % (h, mn) if mn else u"%d h" % h


def indices(entete_html):
    """Associe chaque donnee attendue a son numero de colonne, d'apres l'en-tete."""
    titres = [sans_accent(texte(x)) for x in re.findall(r"<th[^>]*>(.*?)</th>", entete_html, re.S)]
    idx = {}
    for cle, libelles in COLONNES.items():
        for i, titre in enumerate(titres):
            if titre in libelles:
                idx[cle] = i
                break
    manquantes = [c for c in COLONNES if c not in idx]
    if manquantes:
        sys.exit(u"Colonnes introuvables dans l'en-tete : %s\nEn-tete lu : %s"
                 % (u", ".join(manquantes), titres))
    return idx


def collecte():
    req = urllib.request.Request(URL, headers={"User-Agent": UA,
                                               "Accept-Language": "fr-FR,fr;q=0.9"})
    html = urllib.request.urlopen(req, timeout=45).read().decode("utf-8", "replace")

    i = html.find('<table id="table_gh"')
    if i < 0:
        sys.exit("Tableau des horaires introuvable : la page a change de structure.")

    lignes = re.findall(r"<tr[^>]*>(.*?)</tr>", html[i:], re.S)
    if not lignes:
        sys.exit("Tableau vide.")
    idx = indices(lignes[0])
    besoin = max(idx.values()) + 1

    departs, sans_date = [], 0
    for ligne in lignes[1:]:
        c = [texte(x) for x in re.findall(r"<td[^>]*>(.*?)</td>", ligne, re.S)]
        if len(c) < besoin:
            continue
        de = PORTS.get(c[idx["code_depart"]])
        vers = PORTS.get(c[idx["code_arrivee"]])
        if not de or not vers or vers not in ARRIVEES or de in ARRIVEES:
            continue

        d = parse_moment(c[idx["depart"]])
        a = parse_moment(c[idx["arrivee"]])
        if not d:
            sans_date += 1
            continue

        departs.append({
            "de": de,
            "vers": vers,
            "depart": d.strftime("%Y-%m-%dT%H:%M"),
            "arrivee": a.strftime("%Y-%m-%dT%H:%M") if a else None,
            "duree": duree(d, a),
            "navire": c[idx["navire"]] or None,
            "compagnie": COMPAGNIE.get(c[idx["code_cie"]], c[idx["code_cie"]].lower()),
            "source": SOURCE,
        })

    if sans_date:
        print("  %d ligne(s) sans date exploitable, ignorees" % sans_date)
    return departs


def main():
    racine = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    chemin = os.path.join(racine, "data", "traversees.json")
    data = json.load(io.open(chemin, encoding="utf-8"))

    nouveaux = collecte()
    if not nouveaux:
        sys.exit("Aucune traversee collectee : on ne remplace rien.")

    # on ne remplace que ce qui vient de cette source, le reste est preserve
    autres = [d for d in data.get("departs", []) if d.get("source") != SOURCE]
    data["departs"] = sorted(autres + nouveaux, key=lambda d: (d.get("depart") or ""))
    data["maj"] = datetime.utcnow().strftime("%Y-%m-%d")
    sources = data.get("sources") or {}
    sources[SOURCE] = URL
    data["sources"] = sources

    print("  %d traversees depuis %s, %d conservees d'autres sources"
          % (len(nouveaux), SOURCE, len(autres)))
    par_ligne = {}
    for d in nouveaux:
        k = d["de"] + u" -> " + d["vers"]
        par_ligne[k] = par_ligne.get(k, 0) + 1
    for k in sorted(par_ligne):
        print("    %-24s %d" % (k, par_ligne[k]))

    if "--dry-run" in sys.argv:
        print("  (dry-run : fichier non ecrit)")
        return

    with io.open(chemin, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=2) + u"\n")
    print("  %s mis a jour" % chemin)


if __name__ == "__main__":
    main()
