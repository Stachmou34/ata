<?php
// ----------- Requete pour sql -------------
// SELECT societe,fax,CHAR_LENGTH(client) AS quota FROM `jl_app` WHERE `lettrage` LIKE 'GP' AND `proprietaire` = 0 AND status = 'V' AND client != '' AND fax != '' AND CHAR_LENGTH(client) > 50 order by quota DESC;
// -----------------------------------------

// Charger le JSON
$jsonData = file_get_contents("wordcloud.json");
$words = json_decode($jsonData, true);

if (!$words) {
    die("Erreur de chargement du JSON.");
}

// Mélanger l'ordre des mots
shuffle($words);

// Déterminer la valeur maximale pour ajuster les tailles
$maxValue = max(array_column($words, "quota"));
?>

<!DOCTYPE html>
<html lang="fr">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nuage de mots interactif</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 20px;
        }

        .wordcloud {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 10px;
            max-width: 800px;
            margin: auto;
        }

        .word {
            text-decoration: none;
            font-weight: bold;
            transition: transform 0.2s ease-in-out;
        }

        .word:hover {
            transform: scale(1.2);
        }
    </style>
</head>

<body>

    <div class="wordcloud">
        <?php foreach ($words as $word):
            $mot = $word["quota"];
            if ($word["quota"] >= '100000') {
                $size = (20 + ($word["quota"] / $maxValue)); // Taille relative
            } elseif ($word["quota"] >= '50000') {
                $size = (17 + ($word["quota"] / $maxValue)); // Taille relative
            } elseif ($word["quota"] >= '10000') {
                $size = (16 + ($word["quota"] / $maxValue)); // Taille relative
            } elseif ($word["quota"] >= '5000') {
                $size = (15 + ($word["quota"] / $maxValue)); // Taille relative
            } elseif ($word["quota"] >= '1000') {
                $size = (14 + ($word["quota"] / $maxValue)); // Taille relative 
            } elseif ($word["quota"] >= '500') {
                $size = (13 + ($word["quota"] / $maxValue)); // Taille relative  
            } elseif ($word["quota"] >= '100') {
                $size = (12 + ($word["quota"] / $maxValue)); // Taille relative
            } elseif ($word["quota"] >= '50') {
                $size = (11 + ($word["quota"] / $maxValue)); // Taille relative                                                             
            } else {
                $size = 10 + ($word["quota"] / $maxValue); // Taille relative
            }
            //$size = 10 + ($word["quota"] / $maxValue) * 25; // Taille relative
            $color = sprintf("#%06X", mt_rand(0, 0xFFFFFF)); // Couleur aléatoire
        ?>
            <a href="<?= htmlspecialchars($word['fax']) ?>"
                class="word"
                target="_blank"
                style="font-size: <?= $size ?>px; color: <?= $color ?>;">
                <?= htmlspecialchars($word['societe']) ?>
            </a>
        <?php endforeach; ?>
    </div>

</body>

</html>