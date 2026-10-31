# Suno — connexion officielle (état au 31 octobre 2026)

## Connexion

Suno MCP est désormais **connecté et authentifié** dans la conversation Sonora principale.

- Serveur MCP officiel : `https://api.suno.com/mcp`
- Compte connecté : `vincent_alfaro`
- Plan observé : Free
- Crédits observés au moment de la vérification : 100 restants / 100 mensuels
- Les générations utilisent les crédits Suno du compte et apparaissent dans la bibliothèque Suno.

## Modèles disponibles via MCP

Au 31 octobre 2026, le MCP expose uniquement :

- `v6-mini`

Le modèle V6 complet n'est pas actuellement autorisé via ce MCP.

Conséquence pour Sonora :

- utiliser `v6-mini` pour les prototypes, essais d'arrangement, structure, rythme et comparaison de variantes ;
- **ne pas considérer la prononciation française ou espagnole comme validée sur mini** ;
- réserver la validation finale de la voix/prononciation au V6 complet dès qu'il devient accessible par un chemin autorisé.

## Stratégie de génération actuelle

Pendant la phase POC :

- viser environ **45 à 60 secondes** ;
- éviter les longues introductions ;
- éviter de générer 2m30 quand l'hypothèse peut être testée sur un extrait court ;
- générer peu de variantes, mais réellement discriminantes ;
- conserver dans le repo les paroles, prompts, paramètres, IDs/URLs et observations utiles.

La chanson doit rester une chanson normale. Elle ne doit jamais commencer par une consigne pédagogique du type « écoute les mots en français ».

## Priorités pédagogiques

Chaque morceau contient environ 3 à 4 mots ou idées cibles.

Les cibles doivent être comprises :

- en espagnol grâce au contexte narratif ;
- en français grâce à des ancrages naturels au cours du morceau.

Il ne faut **pas** traduire chaque phrase. Les ancrages français servent uniquement à verrouiller le sens des cibles sans transformer le morceau en dictée bilingue.

## Direction musicale

Référence actuelle :

- intime, organique, sombre ou brute ;
- voix au premier plan ;
- guitare acoustique / nylon, basse discrète, percussion sèche si utile ;
- légère texture ibérique possible.

À éviter explicitement :

- cute / twee / cozy ;
- pop sucrée ou enfantine ;
- petit beat rond « boum boum » ;
- longue intro ;
- énergie de chanson pédagogique.

## Politique de crédits et autonomie

La routine autonome peut utiliser Suno MCP directement pour avancer le POC, avec les règles suivantes :

- ne jamais acheter de crédits ;
- ne jamais changer d'abonnement ;
- rester dans les crédits déjà disponibles ;
- privilégier 1 à 3 générations discriminantes plutôt que des lots volumineux ;
- noter la consommation de crédits dans le récap quotidien ;
- si Suno devient indisponible ou si le quota est trop bas, continuer hors audio sur le repo, les prompts, les paroles, les tests et l'évaluation.

## Automatisation

La routine Sonora principale est rattachée à la conversation où Suno MCP est disponible.

Cadence : toutes les 3 heures.

Le run de 21:00 heure de Paris inclut le bilan quotidien : avancées, générations, apprentissages, hypothèses, crédits consommés, blocages et prochaines orientations.

## Premier test réel — 31 octobre 2026

- Deux appels de génération custom `v6-mini` ont produit **quatre clips privés** (deux prises par appel) pour l'expérience A/B `2026-10-31-semantic-reset`.
- Quota vérifié après génération : **80/100 crédits restants**, donc **20 crédits consommés**.
- Le paramètre `negative_style` a échoué avec `feature_not_on_plan` sur le compte Free ; les exclusions de style ont été placées dans le champ `style` à la place.
- Malgré « voix dans les 3 premières secondes », l'alignement automatique donne une première syllabe à ~8 s dans 3 prises sur 4. Un hard cap à 60 s a probablement coupé l'outro de l'une d'elles.
- Un appel Suno `audio_create` peut générer **deux morceaux**. Budgéter en conséquence et utiliser des clés d'idempotence pour les retries.
- Voir [le journal complet](../songs/experiments/2026-10-31-semantic-reset/runs/2026-10-31-mcp-smoke-test.json) ; l'évaluation humaine de la musique et de la prononciation reste à faire.
