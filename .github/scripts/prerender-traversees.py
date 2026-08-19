#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Injecte le contenu de la page Traversees dans le HTML, au moment du deploiement.

Sans cela, la page est vide pour un moteur de recherche : le tableau des
departs, l'annuaire des lignes et la flotte sont construits en JavaScript a
partir de data/traversees.json. Un robot qui n'execute pas le JS ne voit ni les
noms de ports, ni les compagnies, ni les navires — seulement le message
"Le planning detaille n'est pas encore connecte".

Le script ecrit ce meme contenu directement dans le HTML. Le JavaScript reprend
la main au chargement pour le filtrage et la pagination : le rendu est
identique, l'utilisateur ne voit aucune difference.

Lance au deploiement, jamais commite : le depot garde les gabarits vides.

Usage : python3 .github/scripts/prerender-traversees.py [--dry-run]
"""

import io
import json
import os
import re
import sys
from datetime import datetime

PAGES = [
    ("traversees.html", "fr"),
    ("ar/traversees.html", "ar"),
]
MAX_LIGNES = 25          # meme tranche que la pagination cote navigateur

SHIP = ('<svg class="ic" viewBox="0 0 24 24" aria-hidden="true">'
        '<path d="M3 18.6c1.5 0 1.5 1.3 3 1.3s1.5-1.3 3-1.3 1.5 1.3 3 1.3 1.5-1.3 3-1.3 1.5 1.3 3 1.3"/>'
        '<path d="M5.6 16.2 4 10.8h16l-3.1 5.4H5.6Z"/><path d="M7.8 10.8V6.2h8.4v4.6"/>'
        '<path d="M12 6.2V3.4"/></svg>')
ANCHOR = ('<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="4.6" r="2.1"/>'
          '<path d="M12 6.7V21M6.6 10.2h10.8"/>'
          '<path d="M3.4 14.2c0 4 3.9 6.8 8.6 6.8s8.6-2.8 8.6-6.8"/></svg>')

MOIS = {"fr": ["janv.", "févr.", "mars", "avr.", "mai", "juin",
               "juil.", "août", "sept.", "oct.", "nov.", "déc."],
        "ar": ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو",
               "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]}
JOURS = {"fr": ["lun.", "mar.", "mer.", "jeu.", "ven.", "sam.", "dim."],
         "ar": ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]}
T = {
    "fr": {"track": "Voir la position",
           "meta": u"Horaires mis à jour le <b>%(maj)s</b>, d'après les grilles publiées "
                   u"par %(sources)s. Les autres compagnies figurent dans les lignes ci-dessous.",
           "more": u"Voir les %d traversées suivantes"},
    "ar": {"track": u"عرض الموقع",
           "meta": u"المواعيد محدّثة بتاريخ <b>%(maj)s</b>، وفق الجداول المنشورة من %(sources)s. "
                   u"الشركات الأخرى مذكورة ضمن الخطوط أدناه.",
           "more": u"عرض الرحلات الـ %d التالية"},
}


def esc(s):
    return (u"" if s is None else str(s)).replace("&", "&amp;").replace("<", "&lt;") \
        .replace(">", "&gt;").replace('"', "&quot;")


def remplace(html, balise_id, contenu, chemin):
    """Remplace le contenu interne de l'element portant cet id."""
    m = re.search(r'(<[a-z]+[^>]*\bid="%s"[^>]*>)(.*?)(</[a-z]+>)' % re.escape(balise_id),
                  html, re.S)
    if not m:
        sys.exit(u"%s : element #%s introuvable" % (chemin, balise_id))
    return html[:m.start(2)] + contenu + html[m.end(2):]


def nom_port(data, cle, lang):
    p = data["ports"].get(cle) or {}
    return p.get(lang) or p.get("fr") or cle


def bloc_lignes(data, lang):
    out = []
    for l in data.get("lignes", []):
        cies = u"".join(
            u'<li><a href="%s" target="_blank" rel="noopener">%s ↗</a></li>'
            % (esc((data["compagnies"].get(c) or {}).get("site", "")),
               esc((data["compagnies"].get(c) or {}).get("nom", c)))
            for c in l.get("compagnies", []) if data["compagnies"].get(c))
        out.append(
            u'<div class="line-c"><h3><i>%s</i>%s → %s</h3><span class="flag">%s → FR</span>'
            u'<ul>%s</ul></div>'
            % (ANCHOR, esc(nom_port(data, l["de"], lang)), esc(nom_port(data, l["vers"], lang)),
               esc((data["ports"].get(l["de"]) or {}).get("pays", "")), cies))
    return u"".join(out)


def bloc_flotte(data, lang):
    out = []
    for i, n in enumerate(data.get("navires", [])):
        cie = (data["compagnies"].get(n.get("compagnie")) or {}).get("nom", "")
        out.append(
            u'<button type="button" class="ship-c" data-i="%d">%s'
            u'<span><b>%s</b><small>%s — %s ›</small></span></button>'
            % (i, SHIP, esc(n.get("nom")), esc(cie), esc(T[lang]["track"])))
    return u"".join(out)


def date_lisible(iso, lang):
    try:
        d = datetime.strptime(iso[:16], "%Y-%m-%dT%H:%M")
    except (ValueError, TypeError):
        return esc(iso)
    return u"%s %02d/%02d %02d:%02d" % (JOURS[lang][d.weekday()], d.day, d.month, d.hour, d.minute)


def bloc_departs(data, lang, aujourdhui):
    futurs = [d for d in data.get("departs", []) if (d.get("depart") or "")[:10] >= aujourdhui]
    futurs.sort(key=lambda d: d.get("depart") or "")
    lignes = []
    for x in futurs[:MAX_LIGNES]:
        cie = (data["compagnies"].get(x.get("compagnie")) or {}).get("nom", x.get("compagnie") or "")
        lignes.append(
            u'<tr><td class="route">%s<i>→</i>%s</td>'
            u'<td class="when"><b>%s</b></td><td class="when"><b>%s</b></td>'
            u'<td>%s</td><td><span class="ship">%s</span><span class="co">%s</span></td></tr>'
            % (esc(nom_port(data, x["de"], lang)), esc(nom_port(data, x["vers"], lang)),
               date_lisible(x.get("depart"), lang),
               date_lisible(x["arrivee"], lang) if x.get("arrivee") else u"—",
               esc(x.get("duree") or u"—"), esc(x.get("navire") or u"—"), esc(cie)))
    return u"".join(lignes), len(futurs)


def bloc_meta(data, lang):
    noms = u", ".join(
        u'<a href="%s" target="_blank" rel="noopener">%s</a>'
        % (esc(url), esc((data["compagnies"].get(k) or {}).get("nom", k)))
        for k, url in (data.get("sources") or {}).items())
    if not noms:
        return u""
    return T[lang]["meta"] % {"maj": esc(data.get("maj", "")), "sources": noms}


def main():
    racine = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.chdir(racine)
    data = json.load(io.open(os.path.join("data", "traversees.json"), encoding="utf-8"))
    aujourdhui = datetime.utcnow().strftime("%Y-%m-%d")

    for chemin, lang in PAGES:
        if not os.path.exists(chemin):
            sys.exit(u"%s : fichier absent" % chemin)
        html = io.open(chemin, encoding="utf-8").read()

        html = remplace(html, "lignes-grid", bloc_lignes(data, lang), chemin)
        html = remplace(html, "fleet", bloc_flotte(data, lang), chemin)

        corps, total = bloc_departs(data, lang, aujourdhui)
        if corps:
            html = remplace(html, "tt-body", corps, chemin)
            # le tableau prend la place du message "planning non connecte"
            # le message d'attente est vide ET masque : il ne doit pas etre indexe,
            # mais l'element reste present, le JavaScript s'appuie dessus
            html = remplace(html, "tt-empty", u"", chemin)
            html = html.replace('<div class="empty" id="tt-empty">',
                                '<div class="empty" id="tt-empty" hidden>', 1)
            html = re.sub(r'(<div class="tt-wrap" id="tt-wrap"[^>]*?)\s+hidden(>)', r'\1\2', html, 1)
            reste = total - MAX_LIGNES
            if reste > 0:
                html = re.sub(r'(<button type="button" class="btn btn-navy" id="tt-more")\s+hidden(>)(</button>)',
                              lambda m: m.group(1) + m.group(2)
                              + (T[lang]["more"] % min(reste, MAX_LIGNES)) + m.group(3),
                              html, 1)

        meta = bloc_meta(data, lang)
        if meta:
            html = remplace(html, "tt-meta", meta, chemin)
            html = re.sub(r'(<p class="tt-meta" id="tt-meta")\s+hidden(>)', r'\1\2', html, 1)

        if "--dry-run" in sys.argv:
            print(u"%-24s %d lignes, %d navires, %d/%d departs (dry-run)"
                  % (chemin, len(data.get("lignes", [])), len(data.get("navires", [])),
                     min(total, MAX_LIGNES), total))
            continue
        io.open(chemin, "w", encoding="utf-8").write(html)
        print(u"%-24s %d lignes, %d navires, %d/%d departs pre-rendus"
              % (chemin, len(data.get("lignes", [])), len(data.get("navires", [])),
                 min(total, MAX_LIGNES), total))


if __name__ == "__main__":
    main()
