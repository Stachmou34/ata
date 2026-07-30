#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Integre assets/aman.css directement dans le <head> de chaque page HTML.

Lance au moment du deploiement, jamais commite : le depot garde un simple
<link rel="stylesheet">, pratique pour travailler en local.

Pourquoi : l'hebergement ne compresse a la volee que le text/html. Un CSS
externe part donc en 27 Ko non compresses et bloque le rendu pendant ~400 ms.
Integre dans la page, il profite du gzip applique au HTML et la requete
bloquante du chemin critique disparait.
"""

import io
import os
import re
import sys

CSS_PATH = "assets/aman.css"
PAGES = ["index.html", "ar/index.html", "mentions-legales.html", "erreur-404.html"]

# <link rel="stylesheet" href="...aman.css?v=..." /> quel que soit le chemin relatif
LINK_RE = re.compile(
    r'[ \t]*<link\s+rel="stylesheet"\s+href="[^"]*aman\.css(?:\?[^"]*)?"\s*/?>\s*\n'
)


def main():
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.chdir(root)

    if not os.path.exists(CSS_PATH):
        sys.exit("Introuvable : %s" % CSS_PATH)
    css = io.open(CSS_PATH, encoding="utf-8").read()

    # </style> dans le CSS fermerait la balise par accident
    if "</style" in css.lower():
        sys.exit("Le CSS contient une sequence </style, integration annulee")

    style = u"\t<style>%s</style>\n" % css.strip()
    failures = []

    for page in PAGES:
        if not os.path.exists(page):
            failures.append("%s : fichier absent" % page)
            continue
        html = io.open(page, encoding="utf-8").read()
        html, n = LINK_RE.subn(style, html)
        if n != 1:
            failures.append("%s : %d balise(s) <link> trouvee(s), 1 attendue" % (page, n))
            continue
        io.open(page, "w", encoding="utf-8").write(html)
        print("%-24s CSS integre (%d octets)" % (page, len(css)))

    if failures:
        # On echoue le deploiement plutot que de mettre en ligne une page sans style
        sys.exit("Integration du CSS impossible :\n  " + "\n  ".join(failures))


if __name__ == "__main__":
    main()
