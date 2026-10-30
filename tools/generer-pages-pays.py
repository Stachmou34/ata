#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genere les pages « assurance frontiere <pays> », en francais et en arabe.

Ces pages sont tres repetitives (meme plan, meme cadre legal, memes tarifs) et
seules quelques donnees changent d'un pays a l'autre : ports, compagnies,
plaque, ville d'arrivee. Ce fichier est la source de verite : pour corriger un
texte commun aux trois pays, on le modifie ici et on relance le script, plutot
que d'editer six fichiers HTML a la main.

    python3 tools/generer-pages-pays.py

Les fichiers produits sont versionnes : le script n'est pas appele au
deploiement, seulement quand on veut regenerer les pages.
"""

import io
import json
import os
import sys

# --------------------------------------------------------------------------
# Donnees propres a chaque pays
# --------------------------------------------------------------------------
PAYS = [
    dict(
        cle="algerie", slug="assurance-frontiere-algerie.html",
        fr=dict(nom=u"Algérie", adj=u"algérienne", adj_m=u"algérien", plaque=u"DZ",
                ports=[u"Alger", u"Oran", u"Béjaïa", u"Skikda", u"Annaba", u"Mostaganem"],
                arrivees=u"Marseille et à Sète",
                compagnies=u"Algérie Ferries, Corsica Linea et GNV"),
        ar=dict(nom=u"الجزائر", adj=u"الجزائرية", adj_m=u"الجزائري", plaque=u"DZ",
                ports=[u"الجزائر", u"وهران", u"بجاية", u"سكيكدة", u"عنابة", u"مستغانم"],
                arrivees=u"مرسيليا وسيت",
                compagnies=u"Algérie Ferries وCorsica Linea وGNV"),
    ),
    dict(
        cle="tunisie", slug="assurance-frontiere-tunisie.html",
        fr=dict(nom=u"Tunisie", adj=u"tunisienne", adj_m=u"tunisien", plaque=u"TN",
                ports=[u"Tunis — La Goulette"],
                arrivees=u"Marseille",
                compagnies=u"la CTN et Corsica Linea"),
        ar=dict(nom=u"تونس", adj=u"التونسية", adj_m=u"التونسي", plaque=u"TN",
                ports=[u"تونس — حلق الوادي"],
                arrivees=u"مرسيليا",
                compagnies=u"CTN وCorsica Linea"),
    ),
    dict(
        cle="maroc", slug="assurance-frontiere-maroc.html",
        fr=dict(nom=u"Maroc", adj=u"marocaine", adj_m=u"marocain", plaque=u"MA",
                ports=[u"Nador", u"Tanger Med"],
                arrivees=u"Sète",
                compagnies=u"GNV et Baleària"),
        ar=dict(nom=u"المغرب", adj=u"المغربية", adj_m=u"المغربي", plaque=u"MA",
                ports=[u"الناظور", u"طنجة المتوسط"],
                arrivees=u"سيت",
                compagnies=u"GNV وBaleària"),
    ),
]

TARIFS = [(u"≤ 30 CV", u"30", u"140 €", u"4,67 €"),
          (u"≤ 30 CV", u"90", u"340 €", u"3,78 €"),
          (u"> 30 CV", u"30", u"150 €", u"5,00 €"),
          (u"> 30 CV", u"90", u"370 €", u"4,11 €")]


# --------------------------------------------------------------------------
# Textes communs, en francais
# --------------------------------------------------------------------------
def textes_fr(c):
    p = c["fr"]
    ports_txt = u", ".join(p["ports"][:-1]) + (u" et " + p["ports"][-1] if len(p["ports"]) > 1 else p["ports"][0])
    return dict(
        lang="fr-FR", dir="ltr", locale="fr_FR", pfx="", home="/",
        other="ar/" + c["slug"], otherlang="ar", langlabel=u"🇸🇦 العربية",
        canonical="https://aman-frontiere.com/" + c["slug"],
        title=u"Assurance frontière %s dès 140 € | Aman Frontière" % p["nom"],
        desc=u"Assurance frontière %s : voiture %s en France dès 140 € les 30 jours, "
             u"soit 4,67 €/jour. Attestation immédiate par e-mail, France et Europe."
             % (p["nom"], p["adj"]),
        ogtitle=u"Assurance frontière %s — voiture %s en France dès 140 €" % (p["nom"], p["adj"]),
        brandalt=u"Aman Frontière — assurance en toute confiance, sans frontière",
        homelabel=u"Aman Frontière — accueil",
        navcta=u"Souscrire",
        crumb_home=u"Accueil", crumb_page=u"Assurance frontière " + p["nom"],
        crumb=u'<a href="/">Accueil</a> › Assurance frontière %s' % p["nom"],
        h1=u"Assurance frontière %s" % p["nom"],
        lead=u"Votre voiture est immatriculée %s et vous arrivez en France&nbsp;? Elle doit "
             u"être assurée dès sa sortie du bateau. Nous délivrons votre assurance "
             u"frontière <strong>à partir de 140&nbsp;€ les 30 jours</strong>, soit "
             u"4,67&nbsp;€ par jour, avec l'attestation par e-mail immédiatement après le "
             u"paiement." % (u"au " + p["nom"] if c["cle"] == "maroc" else u"en " + p["nom"]),
        cta1=u"⚡ Souscrire mon assurance frontière",

        s_quoi_eye=u"Définition",
        s_quoi_t=u"Qu'est-ce que l'assurance frontière %s&nbsp;?" % p["nom"],
        s_quoi=[
            u"L'assurance frontière — aussi appelée assurance temporaire frontière ou "
            u"assurance auto frontière — est un contrat d'assurance automobile de courte "
            u"durée destiné aux véhicules immatriculés hors de l'Espace économique "
            u"européen. Pour un véhicule %s, c'est le contrat qui vous permet de circuler "
            u"légalement en France dès votre débarquement." % p["adj_m"],
            u"Il couvre la <strong>responsabilité civile</strong>, c'est-à-dire les dommages "
            u"que vous pourriez causer à autrui. C'est la garantie que la loi française rend "
            u"obligatoire pour tout véhicule terrestre à moteur circulant sur son territoire "
            u"(article L.211-1 du Code des assurances).",
        ],

        s_pourquoi_eye=u"Pourquoi c'est obligatoire",
        s_pourquoi_t=u"Votre assurance %s suffit-elle en France&nbsp;?" % p["adj"],
        s_pourquoi=[
            u"Un véhicule immatriculé %s n'est couvert en France que s'il dispose d'une "
            u"carte verte — le certificat international d'assurance — explicitement valable "
            u"pour la France. En pratique, la plupart des contrats souscrits %s ne la "
            u"prévoient pas, et le conducteur se retrouve sans couverture dès le "
            u"débarquement." % (u"au " + p["nom"] if c["cle"] == "maroc" else u"en " + p["nom"],
                                u"au pays" if c["cle"] == "maroc" else u"sur place"),
            u"Vérifiez votre contrat avant de partir&nbsp;: si la France n'y figure pas, ou si "
            u"vous n'avez pas de carte verte en cours de validité, l'assurance frontière est "
            u"la solution. C'est d'ailleurs ce que vérifient la police aux frontières et la "
            u"douane à la sortie du ferry, à %s." % p["arrivees"],
            u"Sans attestation valable, vous ne pouvez pas prendre la route&nbsp;: le véhicule "
            u"reste immobilisé. Rouler sans assurance en France est par ailleurs un délit, "
            u"passible d'une amende forfaitaire de 500&nbsp;€ pouvant être portée à "
            u"3&nbsp;750&nbsp;€ devant le tribunal.",
        ],

        s_prix_eye=u"Nos tarifs",
        s_prix_t=u"Prix d'une assurance frontière %s" % p["nom"],
        s_prix_intro=u"Nos prix sont fixes, tout compris, sans frais de dossier. Ils "
                     u"dépendent uniquement de la puissance du véhicule et de la durée.",
        th_prix=[u"Véhicule", u"Durée", u"Prix TTC", u"Soit par jour"],
        prix=[(v, d + u" jours", t, j) for v, d, t, j in TARIFS],
        s_prix_apres=u"À titre de comparaison, les tarifs relevés le 19/08/2026 chez quatre "
                     u"courtiers spécialisés allaient de 158&nbsp;€ à 175&nbsp;€ les 30 jours, "
                     u"soit 5,27&nbsp;€ à 5,83&nbsp;€ par jour. "
                     u'<a href="/#tarifs">Voir le comparatif détaillé ›</a>',

        s_gar_eye=u"Vos garanties",
        s_gar_t=u"Ce que couvre le contrat",
        gar=[(u"Responsabilité civile",
              u"Les dommages corporels et matériels que vous causez à un tiers, pendant "
              u"toute la durée du contrat. Les dommages corporels sont couverts sans plafond."),
             (u"Défense pénale et recours",
              u"Si vous êtes poursuivi après un accident de la circulation, ou si vous devez "
              u"obtenir réparation auprès d'un tiers responsable&nbsp;: conseil juridique, "
              u"frais et honoraires d'avocat, expertises. Jusqu'à 10 000&nbsp;€ par litige."),
             (u"Attestation immédiate",
              u"Le document à présenter au contrôle vous est envoyé par e-mail dès le "
              u"paiement validé. Vous pouvez l'imprimer ou le montrer sur votre téléphone.")],
        gar_note=u"La garantie défense et recours ne concerne que les litiges liés à un "
                 u"accident de la circulation. Le contrat couvre la responsabilité civile&nbsp;: "
                 u"il ne prend pas en charge les dommages subis par votre propre véhicule.",

        s_duree_eye=u"Durées",
        s_duree_t=u"30 ou 90 jours, au choix",
        s_duree=[
            u"Deux durées sont disponibles. <strong>30 jours</strong> convient aux séjours "
            u"d'été et aux vacances familiales. <strong>90 jours</strong> couvre un séjour "
            u"long sans renouvellement, et revient nettement moins cher au jour&nbsp;: "
            u"3,78&nbsp;€ contre 4,67&nbsp;€.",
            u"Vous choisissez la date et l'heure de prise d'effet au moment de la "
            u"souscription. Vous pouvez donc souscrire avant d'embarquer et faire démarrer le "
            u"contrat le jour de votre arrivée&nbsp;: c'est ce que nous recommandons.",
            u"À savoir&nbsp;: un véhicule immatriculé %s peut circuler en France jusqu'à "
            u"6 mois sans immatriculation française, à condition d'être assuré pendant toute "
            u"la durée du séjour." % (u"au " + p["nom"] if c["cle"] == "maroc" else u"en " + p["nom"]),
        ],

        s_villes_eye=u"À l'arrivée",
        s_villes_t=u"Assurance frontière %s à %s" % (p["nom"], p["arrivees"]),
        s_villes=[
            u"Les liaisons depuis %s arrivent à %s. Le déroulement est le même dans chaque "
            u"port&nbsp;: à la sortie du navire, le contrôle vérifie la carte grise, "
            u"l'identité du conducteur et l'attestation d'assurance."
            % (ports_txt, p["arrivees"]),
            u"Rien ne vous oblige à souscrire sur place&nbsp;: une attestation obtenue en "
            u"ligne la veille, ou depuis %s, a exactement la même valeur. Souscrire à "
            u"l'avance vous évite la file d'attente et la pression du moment."
            % (u"le " + p["nom"] if c["cle"] == "maroc" else u"la " + p["nom"] if c["cle"] == "tunisie" else u"l'" + p["nom"]),
            u"C'est aussi le seul moyen d'être certain du prix&nbsp;: nos tarifs sont fixes "
            u"et affichés, quel que soit le port et quelle que soit la saison.",
        ],

        s_diff_eye=u"Ne pas confondre",
        s_diff_t=u"Assurance frontière ou assurance temporaire&nbsp;?",
        s_diff=[
            u"Les deux expressions sont souvent employées l'une pour l'autre. "
            u"L'<strong>assurance temporaire</strong> classique est un contrat court pour un "
            u"véhicule déjà immatriculé dans l'Espace économique européen&nbsp;: un prêt de "
            u"voiture, un essai, un convoyage.",
            u"L'<strong>assurance frontière</strong>, parfois appelée assurance auto "
            u"temporaire %s, s'adresse aux véhicules immatriculés hors de cet espace. C'est "
            u"le contrat qu'il vous faut si votre plaque est %s." % (p["nom"], p["adj"]),
            u"Un cas voisin&nbsp;: le véhicule acheté en Europe pour être exporté, qui circule "
            u"sous plaque provisoire WW. Il relève lui aussi de l'assurance frontière. En cas "
            u"de doute, appelez-nous avant de souscrire.",
        ],

        s_doc_eye=u"Documents",
        s_doc_t=u"Ce qu'il faut préparer",
        docs=[u"La carte grise du véhicule %s" % p["adj_m"],
              u"Une pièce d'identité du conducteur",
              u"Le permis de conduire du conducteur"],
        s_doc_apres=u"Rien d'autre. Pas de justificatif de domicile en France, pas de relevé "
                    u"d'information de votre assureur d'origine.",

        s_comment_eye=u"Souscription",
        s_comment_t=u"Comment souscrire en quelques minutes",
        etapes=[(u"Vous remplissez le formulaire",
                 u"Les informations du véhicule et du conducteur, la durée et la date de "
                 u"début que vous souhaitez."),
                (u"Vous réglez en ligne",
                 u"Paiement sécurisé. Le prix affiché est le prix final, sans frais ajoutés."),
                (u"Vous recevez votre attestation",
                 u"Par e-mail, immédiatement. Elle est valable dès la date de prise d'effet "
                 u"que vous avez choisie.")],
        s_comment_note=u"La souscription se fait uniquement en ligne, jamais par téléphone. "
                       u"Nos conseillers sont joignables du lundi au vendredi de 9h à 18h si "
                       u"vous bloquez sur une étape.",

        faq_eye=u"Questions fréquentes",
        faq_t=u"Assurance frontière %s&nbsp;: vos questions" % p["nom"],
        faq=[
            (u"Mon assurance %s est-elle valable en France ?" % p["adj"],
             u"Seulement si votre contrat prévoit une carte verte — le certificat international d'assurance — explicitement valable pour la France. La plupart des contrats souscrits sur place ne la prévoient pas. Vérifiez avant de partir : sans elle, il vous faut une assurance frontière."),
            (u"Combien coûte une assurance frontière %s ?" % p["nom"],
             u"À partir de 140 € pour 30 jours, soit 4,67 € par jour, et 340 € pour 90 jours, soit 3,78 € par jour, pour un véhicule jusqu'à 30 CV. 150 € et 370 € au-delà de 30 CV. Prix TTC, tout compris, sans frais de dossier."),
            (u"Puis-je souscrire avant de quitter %s ?" % (u"le Maroc" if c["cle"] == "maroc" else u"la Tunisie" if c["cle"] == "tunisie" else u"l'Algérie"),
             u"Oui, et c'est ce que nous recommandons. Vous choisissez la date de prise d'effet au moment de la souscription : faites-la démarrer le jour de votre débarquement."),
            (u"Quels documents faut-il fournir ?",
             u"La carte grise du véhicule %s, une pièce d'identité du conducteur et son permis de conduire. Rien d'autre." % p["adj_m"]),
            (u"Combien de temps puis-je rouler en France avec une voiture %s ?" % p["adj"],
             u"Jusqu'à 6 mois sans avoir à l'immatriculer en France, à condition d'être assuré pendant toute la durée du séjour."),
            (u"Que couvre exactement le contrat ?",
             u"La responsabilité civile, c'est-à-dire les dommages causés à autrui, avec les dommages corporels sans plafond. S'y ajoute la défense pénale et recours après un accident de la circulation, jusqu'à 10 000 € par litige. Le contrat ne couvre pas les dommages subis par votre propre véhicule."),
            (u"L'assurance est-elle valable ailleurs qu'en France ?",
             u"Oui, le contrat est valable en France et dans les pays de l'Espace économique européen figurant sur l'attestation."),
            (u"Que se passe-t-il si mon bateau a du retard ?",
             u"Votre contrat démarre à la date que vous avez choisie, pas à l'heure d'arrivée du navire. En cas de retard important, contactez-nous avant le débarquement pour décaler la date de prise d'effet."),
            (u"Puis-je prolonger mon contrat ?",
             u"Si votre séjour se prolonge, contactez-nous avant l'échéance. Mieux vaut anticiper : rouler ne serait-ce qu'un jour sans assurance vous expose à une amende et à l'immobilisation du véhicule."),
            (u"Est-ce que je risque quelque chose sans assurance frontière ?",
             u"Oui. Vous ne pourrez pas sortir du port, et rouler sans assurance en France est un délit : 500 € d'amende forfaitaire, jusqu'à 3 750 € devant le tribunal, avec immobilisation possible du véhicule."),
        ],

        cta_h=u"Votre voiture %s, assurée en quelques minutes" % p["adj"],
        cta_p=u"Attestation immédiate par e-mail, 30 ou 90 jours, à partir de 140 €.",
        cta_b=u"⚡ Souscrire en ligne",

        foot_nav=u"Navigation", foot_lang=u"Langue / اللغة",
        foot_desc=u"Assurance en toute confiance, sans frontière. Assurance frontière et "
                  u"temporaire pour véhicules étrangers (DZ, TN, MA) arrivant en ferry à "
                  u"Marseille et à Sète.",
        legal=u'© <span id="y"></span> Aman Frontière — aman-frontiere.com — propriété de '
              u'MCJ COURTAGE — Courtier en assurance immatriculé ORIAS n° 26008651 '
              u'(<a href="https://www.orias.fr" target="_blank" rel="noopener">orias.fr</a>)',
        modal_label=u"Souscription en ligne", modal_close=u"Fermer la fenêtre",
    )


# --------------------------------------------------------------------------
# Textes communs, en arabe
# --------------------------------------------------------------------------
def textes_ar(c):
    p = c["ar"]
    f = c["fr"]
    ports_txt = u"، ".join(p["ports"])
    return dict(
        lang="ar", dir="rtl", locale="ar_AR", pfx="../", home="../",
        other="../" + c["slug"], otherlang="fr", langlabel=u"🇫🇷 Français",
        canonical="https://aman-frontiere.com/ar/" + c["slug"],
        title=u"تأمين الحدود لـ%s ابتداءً من 140 € | أمان فرونتيير" % p["nom"],
        desc=u"تأمين الحدود لـ%s: سيارتك %s في فرنسا ابتداءً من 140 € لمدة 30 يوماً، أي 4,67 € "
             u"في اليوم. شهادة فورية عبر البريد الإلكتروني، فرنسا وأوروبا." % (p["nom"], p["adj"]),
        ogtitle=u"تأمين الحدود لـ%s — سيارتك %s في فرنسا ابتداءً من 140 €" % (p["nom"], p["adj"]),
        brandalt=u"أمان فرونتيير",
        homelabel=u"أمان فرونتيير — الرئيسية",
        navcta=u"اكتتب الآن",
        crumb_home=u"الرئيسية", crumb_page=u"تأمين الحدود لـ" + p["nom"],
        crumb=u'<a href="../">الرئيسية</a> › تأمين الحدود لـ%s' % p["nom"],
        h1=u"تأمين الحدود لـ%s" % p["nom"],
        lead=u"سيارتك مسجّلة في %s وستصل إلى فرنسا؟ يجب أن تكون مؤمّنة فور خروجها من الباخرة. "
             u"نصدر لك تأمين الحدود <strong>ابتداءً من 140 € لمدة 30 يوماً</strong>، أي 4,67 € "
             u"في اليوم، مع الشهادة عبر البريد الإلكتروني فور الدفع." % p["nom"],
        cta1=u"⚡ اكتتب تأمين الحدود",

        s_quoi_eye=u"التعريف",
        s_quoi_t=u"ما هو تأمين الحدود لـ%s؟" % p["nom"],
        s_quoi=[
            u"تأمين الحدود — ويسمّى أيضاً التأمين المؤقت للحدود أو تأمين السيارة عند الحدود — "
            u"عقد تأمين سيارات قصير المدة مخصّص للمركبات المسجّلة خارج المنطقة الاقتصادية "
            u"الأوروبية. بالنسبة لسيارة %s، هو العقد الذي يتيح لك التنقّل بشكل قانوني في فرنسا "
            u"فور نزولك." % p["adj"],
            u"يغطّي <strong>المسؤولية المدنية</strong>، أي الأضرار التي قد تلحقها بالغير. وهي "
            u"الضمانة التي يفرضها القانون الفرنسي على كل مركبة برية ذات محرّك تسير على أراضيه "
            u"(المادة L.211-1 من قانون التأمينات).",
        ],

        s_pourquoi_eye=u"لماذا هو إلزامي",
        s_pourquoi_t=u"هل يكفي تأمينك %s في فرنسا؟" % p["adj"],
        s_pourquoi=[
            u"السيارة المسجّلة في %s ليست مغطّاة في فرنسا إلا إذا كانت لديها بطاقة خضراء — "
            u"شهادة التأمين الدولية — صالحة صراحةً لفرنسا. وعملياً، أغلب العقود المبرمة في "
            u"البلد لا تنصّ عليها، فيجد السائق نفسه بلا تغطية فور النزول." % p["nom"],
            u"تحقّق من عقدك قبل السفر: إن لم تكن فرنسا مذكورة فيه، أو لم تكن لديك بطاقة خضراء "
            u"سارية، فتأمين الحدود هو الحل. وهذا بالضبط ما تتحقّق منه شرطة الحدود والجمارك عند "
            u"الخروج من الباخرة في %s." % p["arrivees"],
            u"بدون شهادة صالحة لا يمكنك أخذ الطريق: تبقى السيارة محجوزة. كما أن القيادة بدون "
            u"تأمين في فرنسا جنحة يعاقب عليها بغرامة جزافية قدرها 500 € قد ترتفع إلى 3 750 € "
            u"أمام المحكمة.",
        ],

        s_prix_eye=u"أسعارنا",
        s_prix_t=u"سعر تأمين الحدود لـ%s" % p["nom"],
        s_prix_intro=u"أسعارنا ثابتة وشاملة، بدون رسوم ملف. تتوقّف فقط على قوة السيارة والمدة.",
        th_prix=[u"السيارة", u"المدة", u"السعر شامل الضرائب", u"أي في اليوم"],
        prix=[(u"حتى 30 حصاناً" if v.startswith(u"≤") else u"أكثر من 30 حصاناً",
               d + u" يوماً", t, j) for v, d, t, j in TARIFS],
        s_prix_apres=u"للمقارنة، الأسعار المرصودة بتاريخ 19/08/2026 لدى أربعة وسطاء متخصصين "
                     u"تراوحت بين 158 € و175 € لمدة 30 يوماً، أي من 5,27 € إلى 5,83 € في اليوم. "
                     u'<a href="../#tarifs">شاهد المقارنة التفصيلية ›</a>',

        s_gar_eye=u"ضماناتك",
        s_gar_t=u"ما الذي يغطّيه العقد",
        gar=[(u"المسؤولية المدنية",
              u"الأضرار الجسدية والمادية التي تلحقها بالغير، طوال مدة العقد. الأضرار الجسدية "
              u"مغطّاة بدون سقف."),
             (u"الدفاع الجزائي والطعون",
              u"إذا تمت ملاحقتك إثر حادث سير، أو إذا احتجت إلى الحصول على تعويض من طرف ثالث "
              u"مسؤول: استشارة قانونية، مصاريف وأتعاب المحامي، الخبرات. حتى 10 000 € عن كل نزاع."),
             (u"شهادة فورية",
              u"الوثيقة التي تُقدَّم عند المراقبة تصلك عبر البريد الإلكتروني فور تأكيد الدفع. "
              u"يمكنك طباعتها أو عرضها على هاتفك.")],
        gar_note=u"ضمان الدفاع والطعون يقتصر على النزاعات المرتبطة بحادث سير. العقد يغطّي "
                 u"المسؤولية المدنية: فهو لا يتكفّل بالأضرار التي تلحق سيارتك أنت.",

        s_duree_eye=u"المدد",
        s_duree_t=u"30 أو 90 يوماً، حسب اختيارك",
        s_duree=[
            u"هناك مدّتان متاحتان. <strong>30 يوماً</strong> تناسب إقامات الصيف والعطل "
            u"العائلية. <strong>90 يوماً</strong> تغطّي إقامة طويلة دون تجديد، وتكلّف أقل "
            u"بكثير في اليوم: 3,78 € مقابل 4,67 €.",
            u"أنت من يختار تاريخ وساعة بدء السريان عند الاكتتاب. يمكنك إذن الاكتتاب قبل "
            u"الإبحار وجعل العقد يبدأ يوم وصولك: هذا ما ننصح به.",
            u"للعلم: يمكن لسيارة مسجّلة في %s أن تسير في فرنسا حتى 6 أشهر دون تسجيل فرنسي، "
            u"شرط أن تكون مؤمّنة طوال مدة الإقامة." % p["nom"],
        ],

        s_villes_eye=u"عند الوصول",
        s_villes_t=u"تأمين الحدود لـ%s في %s" % (p["nom"], p["arrivees"]),
        s_villes=[
            u"الرحلات القادمة من %s تصل إلى %s. والإجراء واحد في كل ميناء: عند الخروج من "
            u"السفينة، تتحقّق المراقبة من البطاقة الرمادية وهوية السائق وشهادة التأمين."
            % (ports_txt, p["arrivees"]),
            u"لا شيء يلزمك بالاكتتاب في عين المكان: شهادة حصلت عليها عبر الإنترنت في اليوم "
            u"السابق، أو من %s، لها القيمة نفسها تماماً. الاكتتاب المسبق يجنّبك الطابور وضغط "
            u"اللحظة." % p["nom"],
            u"وهو أيضاً الوسيلة الوحيدة للتأكّد من السعر: أسعارنا ثابتة ومعلنة، مهما كان "
            u"الميناء ومهما كان الموسم.",
        ],

        s_diff_eye=u"لا تخلط",
        s_diff_t=u"تأمين الحدود أم التأمين المؤقت؟",
        s_diff=[
            u"كثيراً ما تُستعمل العبارتان إحداهما مكان الأخرى. <strong>التأمين المؤقت</strong> "
            u"الكلاسيكي عقد قصير لسيارة مسجّلة أصلاً في المنطقة الاقتصادية الأوروبية: إعارة "
            u"سيارة، تجربة، أو نقل.",
            u"أما <strong>تأمين الحدود</strong>، الذي يسمّى أحياناً التأمين المؤقت لسيارات %s، "
            u"فيخصّ المركبات المسجّلة خارج هذه المنطقة. وهو العقد الذي تحتاجه إذا كانت لوحتك "
            u"%s." % (p["nom"], p["adj"]),
            u"وهناك حالة قريبة: السيارة المشتراة في أوروبا بغرض التصدير، والتي تسير بلوحة "
            u"مؤقتة WW. وهي بدورها تندرج تحت تأمين الحدود. في حال الشك، اتصل بنا قبل الاكتتاب.",
        ],

        s_doc_eye=u"الوثائق",
        s_doc_t=u"ما ينبغي تحضيره",
        docs=[u"البطاقة الرمادية للسيارة %s" % p["adj"],
              u"وثيقة هوية السائق",
              u"رخصة قيادة السائق"],
        s_doc_apres=u"لا شيء آخر. لا إثبات سكن في فرنسا، ولا كشف معلومات من مؤمّنك الأصلي.",

        s_comment_eye=u"الاكتتاب",
        s_comment_t=u"كيف تكتتب في بضع دقائق",
        etapes=[(u"تملأ الاستمارة",
                 u"معلومات السيارة والسائق، والمدة وتاريخ البدء الذي تريده."),
                (u"تدفع عبر الإنترنت",
                 u"دفع آمن. السعر المعروض هو السعر النهائي، بدون رسوم مضافة."),
                (u"تستلم شهادتك",
                 u"عبر البريد الإلكتروني، فوراً. وهي صالحة ابتداءً من تاريخ السريان الذي اخترته.")],
        s_comment_note=u"الاكتتاب يتم عبر الإنترنت فقط، وليس عبر الهاتف أبداً. مستشارونا "
                       u"متاحون من الاثنين إلى الجمعة من 9:00 إلى 18:00 إن واجهت صعوبة.",

        faq_eye=u"الأسئلة الشائعة",
        faq_t=u"تأمين الحدود لـ%s: أسئلتك" % p["nom"],
        faq=[
            (u"هل تأميني %s صالح في فرنسا؟" % p["adj"],
             u"فقط إذا كان عقدك ينصّ على بطاقة خضراء — شهادة التأمين الدولية — صالحة صراحةً لفرنسا. أغلب العقود المبرمة في البلد لا تنصّ عليها. تحقّق قبل السفر: بدونها تحتاج إلى تأمين حدود."),
            (u"كم يكلّف تأمين الحدود لـ%s؟" % p["nom"],
             u"ابتداءً من 140 € لمدة 30 يوماً، أي 4,67 € في اليوم، و340 € لمدة 90 يوماً، أي 3,78 € في اليوم، لسيارة حتى 30 حصاناً. و150 € و370 € لما فوق 30 حصاناً. أسعار شاملة الضرائب، بدون رسوم ملف."),
            (u"هل يمكنني الاكتتاب قبل مغادرة %s؟" % p["nom"],
             u"نعم، وهذا ما ننصح به. تختار تاريخ بدء السريان عند الاكتتاب: اجعله يبدأ يوم نزولك."),
            (u"ما الوثائق المطلوبة؟",
             u"البطاقة الرمادية للسيارة %s، ووثيقة هوية السائق، ورخصة قيادته. لا شيء آخر." % p["adj"]),
            (u"كم من الوقت يمكنني القيادة في فرنسا بسيارة %s؟" % p["adj"],
             u"حتى 6 أشهر دون الحاجة إلى تسجيلها في فرنسا، شرط أن تكون مؤمّنة طوال مدة الإقامة."),
            (u"ما الذي يغطّيه العقد بالضبط؟",
             u"المسؤولية المدنية، أي الأضرار التي تلحقها بالغير، مع تغطية الأضرار الجسدية بدون سقف. يضاف إليها الدفاع الجزائي والطعون إثر حادث سير، حتى 10 000 € عن كل نزاع. العقد لا يغطّي الأضرار التي تلحق سيارتك أنت."),
            (u"هل التأمين صالح خارج فرنسا؟",
             u"نعم، العقد صالح في فرنسا وفي دول المنطقة الاقتصادية الأوروبية المذكورة في الشهادة."),
            (u"ماذا يحدث إذا تأخّرت الباخرة؟",
             u"يبدأ عقدك في التاريخ الذي اخترته، لا في ساعة وصول السفينة. في حال تأخّر كبير، اتصل بنا قبل النزول لتأجيل تاريخ السريان."),
            (u"هل يمكنني تمديد عقدي؟",
             u"إذا طالت إقامتك، اتصل بنا قبل انتهاء المدة. من الأفضل الاستباق: القيادة ولو يوماً واحداً بدون تأمين تعرّضك لغرامة ولحجز السيارة."),
            (u"هل أخاطر بشيء بدون تأمين حدود؟",
             u"نعم. لن تتمكّن من الخروج من الميناء، والقيادة بدون تأمين في فرنسا جنحة: غرامة جزافية 500 €، تصل إلى 3 750 € أمام المحكمة، مع إمكانية حجز السيارة."),
        ],

        cta_h=u"سيارتك %s، مؤمَّنة في بضع دقائق" % p["adj"],
        cta_p=u"شهادة فورية عبر البريد الإلكتروني، 30 أو 90 يوماً، ابتداءً من 140 €.",
        cta_b=u"⚡ اكتتب عبر الإنترنت",

        foot_nav=u"التنقل", foot_lang=u"اللغة / Langue",
        foot_desc=u"تأمين بكل ثقة، بلا حدود. تأمين الحدود والتأمين المؤقت للسيارات الأجنبية "
                  u"(DZ، TN، MA) القادمة بالباخرة إلى مرسيليا وسيت.",
        legal=u'© <span id="y"></span> أمان فرونتيير — aman-frontiere.com — ملك لشركة '
              u'MCJ COURTAGE — وسيط تأمين مسجّل لدى ORIAS رقم 26008651 '
              u'(<a href="https://www.orias.fr" target="_blank" rel="noopener">orias.fr</a>)',
        modal_label=u"الاكتتاب عبر الإنترنت", modal_close=u"إغلاق النافذة",
    )


# --------------------------------------------------------------------------
# Navigation et pied de page : les liens entre pays
# --------------------------------------------------------------------------
def liens(c, lang):
    """Navigation et liens de pied de page, avec les pays frères."""
    autres = [a for a in PAYS if a["cle"] != c["cle"]]
    if lang == "fr":
        nav = [(u"Tarifs", u"/#tarifs")]
        nav += [(a["fr"]["nom"], a["slug"]) for a in autres]
        nav += [(u"Traversées", u"traversees.html")]
        foot = (u'<a href="/#tarifs">Tarifs</a><br />'
                + u"".join(u'<a href="%s">Assurance frontière %s</a><br />' % (a["slug"], a["fr"]["nom"])
                           for a in PAYS)
                + u'<a href="traversees.html">Traversées</a><br />'
                  u'<a href="/#contact">Contact</a>')
        langfoot = (u'<a href="ar/%s" lang="ar" hreflang="ar">🇸🇦 النسخة العربية</a><br />'
                    u'<a href="mentions-legales.html">Mentions Légales</a>' % c["slug"])
    else:
        nav = [(u"الأسعار", u"../#tarifs")]
        nav += [(a["ar"]["nom"], a["slug"]) for a in autres]
        nav += [(u"الرحلات البحرية", u"traversees.html")]
        foot = (u'<a href="../#tarifs">الأسعار</a><br />'
                + u"".join(u'<a href="%s">تأمين الحدود لـ%s</a><br />' % (a["slug"], a["ar"]["nom"])
                           for a in PAYS)
                + u'<a href="traversees.html">الرحلات البحرية</a><br />'
                  u'<a href="../#contact">اتصل بنا</a>')
        langfoot = (u'<a href="../%s" lang="fr" hreflang="fr">🇫🇷 Version française</a><br />'
                    u'<a href="../mentions-legales.html">الشروط القانونية</a>' % c["slug"])
    return nav, foot, langfoot


GABARIT = u'''<!DOCTYPE html>
<html lang="%(lang)s" dir="%(dir)s" prefix="og: http://ogp.me/ns#">
<head>
\t<meta charset="utf-8" />
\t<title>%(title)s</title>
\t<meta name="viewport" content="width=device-width, initial-scale=1" />
\t<meta name="description" content="%(desc)s" />
\t<meta name="theme-color" content="#0f2a52" />
\t<meta property="og:locale" content="%(locale)s" />
\t<meta property="og:type" content="website" />
\t<meta property="og:url" content="%(canonical)s" />
\t<meta property="og:title" content="%(ogtitle)s" />
\t<meta property="og:site_name" content="Aman Frontière" />
\t<meta property="og:description" content="%(desc)s" />
\t<meta property="og:image" content="https://aman-frontiere.com/images/aman-logo.png" />
\t<link rel="canonical" href="%(canonical)s" />
\t<link rel="alternate" hreflang="fr" href="https://aman-frontiere.com/%(slug)s" />
\t<link rel="alternate" hreflang="ar" href="https://aman-frontiere.com/ar/%(slug)s" />
\t<link rel="alternate" hreflang="x-default" href="https://aman-frontiere.com/%(slug)s" />
\t<link rel="icon" href="/favicon.svg" type="image/svg+xml" sizes="any" />
\t<link rel="apple-touch-icon" href="/favicon.svg" />
\t<link rel="stylesheet" href="%(pfx)sassets/aman.css?v=20260730" />
%(jsonld)s
\t<script type="text/javascript">
\t\t(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})(window,document,"clarity","script","x7huufw34g");
\t</script>
</head>
<body>
\t<header class="site">
\t\t<div class="wrap nav">
\t\t\t<a class="brand" href="%(home)s" aria-label="%(homelabel)s">
\t\t\t\t<img src="%(pfx)simages/aman-logo-header-320.png"
\t\t\t\t     srcset="%(pfx)simages/aman-logo-header-320.png 320w, %(pfx)simages/aman-logo-header-460.png 460w, %(pfx)simages/aman-logo-header.png 620w"
\t\t\t\t     sizes="(max-width:560px) 175px, (max-width:860px) 206px, 229px"
\t\t\t\t     width="620" height="163" fetchpriority="high" decoding="async"
\t\t\t\t     alt="%(brandalt)s" />
\t\t\t</a>
\t\t\t<nav class="nav-links">
%(nav)s
\t\t\t\t<a class="lang" href="%(other)s" lang="%(otherlang)s" hreflang="%(otherlang)s">%(langlabel)s</a>
\t\t\t\t<a class="nav-cta cta-open" href="%(home)s#tarifs">%(navcta)s</a>
\t\t\t</nav>
\t\t</div>
\t</header>

\t<main id="contenu">

\t<section class="page-head">
\t\t<div class="wrap">
\t\t\t<p class="crumb">%(crumb)s</p>
\t\t\t<h1>%(h1)s</h1>
\t\t\t<p>%(lead)s</p>
\t\t\t<p class="head-cta"><button type="button" class="btn btn-or cta-open">%(cta1)s</button></p>
\t\t</div>
\t</section>

\t<section>
\t\t<div class="wrap wrap-txt">
\t\t\t<div class="eyebrow">%(s_quoi_eye)s</div>
\t\t\t<h2 class="sec">%(s_quoi_t)s</h2>
%(s_quoi)s
\t\t</div>
\t</section>

\t<section class="sec-creme">
\t\t<div class="wrap wrap-txt">
\t\t\t<div class="eyebrow">%(s_pourquoi_eye)s</div>
\t\t\t<h2 class="sec">%(s_pourquoi_t)s</h2>
%(s_pourquoi)s
\t\t</div>
\t</section>

\t<section id="tarifs">
\t\t<div class="wrap wrap-txt">
\t\t\t<div class="eyebrow">%(s_prix_eye)s</div>
\t\t\t<h2 class="sec">%(s_prix_t)s</h2>
\t\t\t<p class="sec-intro">%(s_prix_intro)s</p>
\t\t\t<div class="tt-wrap" role="region" tabindex="0" aria-label="%(s_prix_t)s">
\t\t\t\t<table class="tt tt-prix">
\t\t\t\t\t<thead><tr>%(th)s</tr></thead>
\t\t\t\t\t<tbody>%(prix_rows)s</tbody>
\t\t\t\t</table>
\t\t\t</div>
\t\t\t<p class="txt">%(s_prix_apres)s</p>
\t\t</div>
\t</section>

\t<section class="sec-creme">
\t\t<div class="wrap">
\t\t\t<div class="eyebrow">%(s_gar_eye)s</div>
\t\t\t<h2 class="sec">%(s_gar_t)s</h2>
\t\t\t<div class="grid">
%(gar_cards)s
\t\t\t</div>
\t\t\t<p class="dr-note"><i aria-hidden="true">ⓘ</i><span>%(gar_note)s</span></p>
\t\t</div>
\t</section>

\t<section>
\t\t<div class="wrap wrap-txt">
\t\t\t<div class="eyebrow">%(s_duree_eye)s</div>
\t\t\t<h2 class="sec">%(s_duree_t)s</h2>
%(s_duree)s
\t\t</div>
\t</section>

\t<section class="sec-creme">
\t\t<div class="wrap wrap-txt">
\t\t\t<div class="eyebrow">%(s_villes_eye)s</div>
\t\t\t<h2 class="sec">%(s_villes_t)s</h2>
%(s_villes)s
\t\t\t<p class="txt">%(lien_traversees)s</p>
\t\t</div>
\t</section>

\t<section>
\t\t<div class="wrap wrap-txt">
\t\t\t<div class="eyebrow">%(s_diff_eye)s</div>
\t\t\t<h2 class="sec">%(s_diff_t)s</h2>
%(s_diff)s
\t\t</div>
\t</section>

\t<section class="sec-creme">
\t\t<div class="wrap wrap-txt">
\t\t\t<div class="eyebrow">%(s_doc_eye)s</div>
\t\t\t<h2 class="sec">%(s_doc_t)s</h2>
\t\t\t<ul class="liste">%(docs)s</ul>
\t\t\t<p class="txt">%(s_doc_apres)s</p>
\t\t</div>
\t</section>

\t<section>
\t\t<div class="wrap">
\t\t\t<div class="eyebrow">%(s_comment_eye)s</div>
\t\t\t<h2 class="sec">%(s_comment_t)s</h2>
\t\t\t<div class="steps">
%(etapes)s
\t\t\t</div>
\t\t\t<p class="sec-intro" style="margin-top:26px;margin-bottom:0">%(s_comment_note)s</p>
\t\t</div>
\t</section>

\t<section id="souscrire">
\t\t<div class="wrap">
\t\t\t<div class="cta-band">
\t\t\t\t<div class="orn"><span>✦</span></div>
\t\t\t\t<h2>%(cta_h)s</h2>
\t\t\t\t<p>%(cta_p)s</p>
\t\t\t\t<div class="hero-cta">
\t\t\t\t\t<button type="button" class="btn btn-or cta-open">%(cta_b)s</button>
\t\t\t\t</div>
\t\t\t</div>
\t\t</div>
\t</section>

\t<section class="sec-creme" id="faq">
\t\t<div class="wrap" style="max-width:880px">
\t\t\t<div class="eyebrow">%(faq_eye)s</div>
\t\t\t<h2 class="sec">%(faq_t)s</h2>
%(faq)s
\t\t</div>
\t</section>

\t</main>

\t<footer class="site">
\t\t<div class="wrap">
\t\t\t<div class="cols">
\t\t\t\t<div>
\t\t\t\t\t<img class="foot-logo" src="%(pfx)simages/aman-logo.png" width="420" height="420" alt="%(brandalt)s" onerror="this.style.display='none'" />
\t\t\t\t\t<h3>Aman Frontière</h3>
\t\t\t\t\t<p>%(foot_desc)s</p>
\t\t\t\t</div>
\t\t\t\t<div>
\t\t\t\t\t<h3>%(foot_nav)s</h3>
\t\t\t\t\t<p>%(foot)s</p>
\t\t\t\t</div>
\t\t\t\t<div>
\t\t\t\t\t<h3>%(foot_lang)s</h3>
\t\t\t\t\t<p>%(langfoot)s</p>
\t\t\t\t</div>
\t\t\t</div>
\t\t\t<div class="legal">%(legal)s</div>
\t\t</div>
\t</footer>

\t<div id="modal-souscription" class="modal-overlay" aria-hidden="true">
\t\t<div class="modal-content" role="dialog" aria-modal="true" aria-label="%(modal_label)s">
\t\t\t<div class="modal-header"><button type="button" id="btn-fermer-modal" aria-label="%(modal_close)s">&times;</button></div>
\t\t\t<div class="modal-body">
\t\t\t\t<iframe id="jl-tarificateur" src="https://www.jlassure.com/sousfiche/assure_tempo_rapide_mb.php?cat=&amp;&amp;tip=09.70.71.01.78&amp;&amp;id=800&amp;&amp;cd=7KAW433&amp;&amp;adrsite=https://www.assurancetemporaireauto.com" title="%(modal_label)s" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
\t\t\t</div>
\t\t</div>
\t</div>

\t<script>
\tdocument.getElementById('y').textContent = new Date().getFullYear();
\t(function(){
\t\tvar modal=document.getElementById('modal-souscription');
\t\tvar closeBtn=document.getElementById('btn-fermer-modal');
\t\tfunction open(){modal.classList.add('show');modal.setAttribute('aria-hidden','false');document.body.classList.add('no-scroll');}
\t\tfunction close(){modal.classList.remove('show');modal.setAttribute('aria-hidden','true');document.body.classList.remove('no-scroll');}
\t\tdocument.querySelectorAll('.cta-open').forEach(function(b){b.addEventListener('click',function(e){e.preventDefault();open();});});
\t\tif(closeBtn)closeBtn.addEventListener('click',close);
\t\tmodal.addEventListener('click',function(e){if(e.target===modal)close();});
\t\tdocument.addEventListener('keydown',function(e){if(e.key==='Escape')close();});
\t})();
\t</script>
</body>
</html>
'''


def jsonld(d):
    racine = "https://aman-frontiere.com/" + ("ar/" if d["lang"] == "ar" else "")
    fil = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": d["crumb_home"], "item": racine},
        {"@type": "ListItem", "position": 2, "name": d["crumb_page"], "item": d["canonical"]}]}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faq"]]}
    return (u'\t<script type="application/ld+json">%s</script>\n'
            u'\t<script type="application/ld+json">%s</script>'
            % (json.dumps(fil, ensure_ascii=False, indent=1),
               json.dumps(faq, ensure_ascii=False, indent=1)))


def construire(c, lang):
    d = textes_fr(c) if lang == "fr" else textes_ar(c)
    nav, foot, langfoot = liens(c, lang)
    paras = lambda xs: u"\n".join(u'\t\t\t<p class="txt">%s</p>' % x for x in xs)
    lien_trav = (u'Les compagnies qui desservent ces lignes sont %s. '
                 u'<a href="traversees.html">Consultez les horaires des traversées ›</a>'
                 % c["fr"]["compagnies"]) if lang == "fr" else (
                 u'الشركات التي تشغّل هذه الخطوط هي %s. '
                 u'<a href="traversees.html">اطّلع على مواعيد الرحلات ›</a>' % c["ar"]["compagnies"])
    return GABARIT % dict(
        d, slug=c["slug"], jsonld=jsonld(d),
        nav=u"\n".join(u'\t\t\t\t<a class="lk" href="%s">%s</a>' % (h, t) for t, h in nav),
        foot=foot, langfoot=langfoot, lien_traversees=lien_trav,
        th=u"".join(u'<th scope="col">%s</th>' % x for x in d["th_prix"]),
        prix_rows=u"".join(u'<tr><th scope="row">%s</th><td>%s</td><td class="p">%s</td>'
                           u'<td>%s</td></tr>' % r for r in d["prix"]),
        gar_cards=u"\n".join(u'\t\t\t\t<div class="card"><h3>%s</h3><p>%s</p></div>' % g
                             for g in d["gar"]),
        docs=u"".join(u'<li>%s</li>' % x for x in d["docs"]),
        etapes=u"\n".join(u'\t\t\t\t<div class="step"><div class="num">%d</div><h3>%s</h3>'
                          u'<p>%s</p></div>' % (i + 1, t, x)
                          for i, (t, x) in enumerate(d["etapes"])),
        faq=u"\n".join(u'\t\t\t<details><summary>%s</summary><div class="faq-a">%s</div>'
                       u'</details>' % q for q in d["faq"]),
        s_quoi=paras(d["s_quoi"]), s_pourquoi=paras(d["s_pourquoi"]),
        s_duree=paras(d["s_duree"]), s_villes=paras(d["s_villes"]), s_diff=paras(d["s_diff"]))


def main():
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(racine)
    for c in PAYS:
        for lang, chemin in (("fr", c["slug"]), ("ar", os.path.join("ar", c["slug"]))):
            html = construire(c, lang)
            io.open(chemin, "w", encoding="utf-8").write(html)
            print(u"%-44s %d octets" % (chemin, len(html.encode("utf-8"))))
    print(u"\nPensez a verifier : sitemap.xml, les liens dans index.html / ar/index.html,")
    print(u"et la liste PAGES de .github/scripts/inline-css.py.")


if __name__ == "__main__":
    main()
