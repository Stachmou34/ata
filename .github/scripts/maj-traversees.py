#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Met a jour data/traversees.json a partir des horaires publies par les compagnies.

Source actuelle : la grille horaire officielle de Corsica Linea
(https://www.corsicalinea.com/reserver/infos-lignes-et-horaires), publiee par la
compagnie elle-meme et autorisee par son robots.txt. On n'en garde que les
traversees qui ARRIVENT a Marseille ou a Sete depuis l'Algerie ou la Tunisie :
ce sont les seules qui concernent nos clients.

Les autres compagnies (Algerie Ferries, GNV, CTN, Balearia) ne publient pas de
grille exploitable automatiquement : leurs departs restent a saisir a la main
dans data/traversees.json, ou via une autre source branchee sur 'apiDeparts'.
Ce script ne touche jamais aux departs dont la source n'est pas la sienne.

Usage : python3 .github/scripts/maj-traversees.py [--dry-run]
"""

import io
import json
import os
import re
import sys
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

MOIS = {"janv": 1, "févr": 2, "fevr": 2, "mars": 3, "avr": 4, "mai": 5, "juin": 6,
        "juil": 7, "août": 8, "aout": 8, "sept": 9, "oct": 10, "nov": 11, "déc": 12, "dec": 12}

DATE_RE = re.compile(r"le\s+(\d{1,2})\s+([A-Za-zÀ-ÿ]+)\.?\s+(\d{4})\s+à\s+(\d{1,2}):(\d{2})")


def texte(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html)).replace("&#039;", "'").strip()


def parse_moment(s):
    """'Marseille le 31 juil. 2026 à 11:00' -> datetime, ou None."""
    m = DATE_RE.search(s)
    if not m:
        return None
    jour, mois, annee, h, mn = m.groups()
    num = MOIS.get(mois.lower().rstrip("."))
    if not num:
        return None
    try:
        return datetime(int(annee), num, int(jour), int(h), int(mn))
    except ValueError:
        return None


def duree(depart, arrivee):
    if not (depart and arrivee) or arrivee <= depart:
        return None
    total = int((arrivee - depart).total_seconds() // 60)
    h, mn = divmod(total, 60)
    return u"%d h %02d" % (h, mn) if mn else u"%d h" % h


def collecte():
    req = urllib.request.Request(URL, headers={"User-Agent": UA,
                                               "Accept-Language": "fr-FR,fr;q=0.9"})
    html = urllib.request.urlopen(req, timeout=45).read().decode("utf-8", "replace")

    i = html.find('<table id="table_gh"')
    if i < 0:
        sys.exit("Tableau des horaires introuvable : la page a change de structure.")

    lignes = re.findall(r"<tr[^>]*>(.*?)</tr>", html[i:], re.S)
    departs, ignorees = [], 0

    for ligne in lignes[1:]:
        cells = [texte(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", ligne, re.S)]
        if len(cells) < 10:
            continue
        de, vers = PORTS.get(cells[6]), PORTS.get(cells[7])
        if not de or not vers or vers not in ARRIVEES or de in ARRIVEES:
            continue

        d, a = parse_moment(cells[0]), parse_moment(cells[1])
        if not d:
            ignorees += 1
            continue

        departs.append({
            "de": de,
            "vers": vers,
            "depart": d.strftime("%Y-%m-%dT%H:%M"),
            "arrivee": a.strftime("%Y-%m-%dT%H:%M") if a else None,
            "duree": duree(d, a),
            "navire": cells[3] or None,
            "compagnie": COMPAGNIE.get(cells[8], cells[8].lower()),
            "source": SOURCE,
        })

    if ignorees:
        print("  %d ligne(s) sans date exploitable, ignorees" % ignorees)
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
    tous = sorted(autres + nouveaux, key=lambda d: (d.get("depart") or ""))

    data["departs"] = tous
    data["maj"] = datetime.utcnow().strftime("%Y-%m-%d")
    data["sources"] = {SOURCE: URL}

    print("  %d traversees depuis %s, %d conservees d'autres sources" %
          (len(nouveaux), SOURCE, len(autres)))
    par_ligne = {}
    for d in nouveaux:
        par_ligne[d["de"] + u" → " + d["vers"]] = par_ligne.get(d["de"] + u" → " + d["vers"], 0) + 1
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
