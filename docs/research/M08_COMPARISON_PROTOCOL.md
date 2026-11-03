# M08 — Protocole de comparaison contrôlée (préparatoire)

**Statut : protocole uniquement.** Aucun texte approuvé, aucune génération Suno. Le brouillon V0 de « No cierres la puerta » reste en revue dans la PR #5.

## Question testable

Le plaisir de réécoute provient-il surtout (a) de la densité rythmique de « No cierres la puerta », (b) des interruptions féminines parlées, ou (c) de leur combinaison ?

## Plan factoriel 2 × 2

| Variante | Refrain | Breaks féminins parlés | Usage |
| --- | --- | --- | --- |
| A | dense | oui | V0 actuel, à approuver |
| B | modéré | oui | isoler la répétition en gardant les breaks |
| C | dense | non | isoler les breaks en gardant la répétition |
| D | modéré | non | contrôle de l'interaction, facultatif après A/B/C |

**Ne pas lancer quatre générations d'un coup.** Préparer B/C/D sur papier seulement après les retours textuels sur A, puis sélectionner le plus petit contraste utile. Même scénario, quatre cibles, progression dramatique et ordre des sections ; éviter de remplacer une répétition par un nouveau mot cible. Sans break, déplacer les ancrages français vers des lignes chantées plausibles, sans traduction plaquée ; cette modification reste un facteur confondant à documenter. Pour tester strictement la présence du parlé, une alternative plus contrôlée consiste à chanter exactement les mêmes lignes françaises au lieu de les parler (conserver le texte et la voix).

## Contrôles déterministes avant Suno

- Compter les occurrences exactes de « no cierres la puerta » dans les paroles et déclarer les comptes par variante ; ne pas utiliser le plafond opt-in des POC courts comme jugement de musicalité pour M08.
- Vérifier la présence des quatre notions et des quatre ancrages français, sans prétendre valider leur naturel.
- Vérifier que le texte soumis correspond exactement au hash approuvé ; contrôle de génération et budget obligatoires.
- Conserver les mêmes paramètres de génération, modèle et prompt de style pour une paire comparée autant que l'outil le permet ; consigner les différences.
- Éviter de comparer les sorties de deux modèles différents comme si seule la répétition changeait.

## Questions de revue humaine

1. Est-ce que la répétition devient entraînante ou lassante ? À quel passage ?
2. Les breaks semblent-ils intimes et naturels, ou donnent-ils l'impression de réciter des traductions ?
3. Préfères-tu une voix parlée féminine, une voix chantée sur les mêmes lignes, ou aucun break ?
4. Quelles expressions espagnoles restent en tête après écoute sans regarder le texte ?
5. Aurais-tu envie d'ajouter cette prise à ta playlist hebdomadaire ?

## Critère de décision

Ne conclure qu'à partir des retours explicites de Vincent ; les comptes de répétition et la conformité du manifeste sont des faits structurels, **pas** des scores de qualité musicale. Si A n'est pas validée textuellement, corriger A avant de produire B/C. Si A est validée, sélectionner un contraste prioritaire, sans dépasser le budget ni l'appel Suno par run.
