# Bestiaire Sonora — mécanismes pédagogiques

**Statut : catalogue de travail, pas un classement de performances.** Un mécanisme est une raison narrative de réemployer une **même notion précise** dans des contextes différents. Le scénario est l'histoire particulière ; la voix et le style sont des variables musicales indépendantes.

| ID | Mécanisme | Pourquoi la reprise semble naturelle | Risque à surveiller | État |
| --- | --- | --- | --- | --- |
| M01 | Écho entre deux personnes | A raconte un départ ; B répond par un autre départ, avec le même sens de « laisser derrière soi » | faux ami lexical : `dejar atrás` ≠ simplement oublier des clés | **Prometteur** : D1, premier retour positif sur l'audio ; correction textuelle D1b encore à approuver |
| M02 | Rectification / malentendu | « Tu parles de la maison ? — Non, de la vie qu'on y menait » | dialogue scolaire ou réplique trop explicative | Hypothèse non testée |
| M03 | Souvenirs contrastés | Deux personnages évoquent des détails différents d'une même époque | ne partager qu'une ambiance au lieu du sens cible | Hypothèse non testée (D3 brouillon) |
| M04 | Question qui appelle une précision | La réponse resserre le sens d'un mot déjà apparu dans la question | répétition mot à mot artificielle | Hypothèse non testée |
| M05 | Désaccord puis décision commune | Une notion revient parce que les personnages négocient un choix | sonner comme une conversation de manuel | Hypothèse non testée |
| M06 | Refrain à réponses alternées | Un motif revient musicalement ; la seconde voix en change le point de vue | refrain saturé de vocabulaire cible | Hypothèse non testée |
| M07 | Découverte d'un objet / d'une trace | Chacun trouve un indice différent ; l'action `hallar` / « trouver » est reprise | répétition gratuite d'objets sans enjeu narratif | Hypothèse non testée |

## Fiche d'un mécanisme (pour les futures entrées)

- **Déclencheur narratif** : qu'est-ce qui rend la reprise crédible ?
- **Sens lexical exact** : quelle notion passe d'une langue à l'autre ?
- **Deux contextes distincts** : l'ancrage français n'est ni un sous-titre ni une idée voisine.
- **Emplacement musical** : couplet, réponse, pont ou refrain ; éviter de multiplier les bascules de langue.
- **Échec observable à la lecture** : phrase creuse, décalage sémantique, traduction littérale, dialogue artificiel.
- **Preuve humaine** : distinguer « texte jugé meilleur », « audio préféré », « prononciation validée » et « mémorisation démontrée ».

## Premier croisement à tester

**M01 (écho conversationnel) × deux anciens amoureux × dark indie acoustique** : le POC D1 a suscité un retour positif, avec préférence pour la prise 1, mais son premier ancrage lexical était imparfait. Le brouillon D1b corrige ce point à l'écrit. Le nouveau [texte complet](../songs/drafts/2026-11-01-la-luz-del-pasillo-full.md) utilise M01, avec des touches de M03 et M07, **sans prétendre valider ces mécanismes**.


## Cas observé — M08, refrain répété et breaks français (11 novembre 2026)

- **Scène** : une femme refuse de revenir sur sa décision après une confidence trahie ; refrain espagnol `No voy a dar marcha atrás`, avec deux breaks parlés français. Texte V2 approuvé puis généré via Suno v6-mini, deux prises lors d'un **même appel** ; [PR #5](https://github.com/VincentAl/sonora/pull/5).
- **Mécanismes candidats** : répétition rythmique du refrain et reformulation française de notions espagnoles dans la confrontation. Cette observation **ne valide pas** les mécanismes pédagogiques ni la mémorisation.
- **Feedback humain explicite** : [prise 2](https://suno.com/song/719e7126-276b-4460-83a4-9677baf81f0e) préférée pour le rythme et une voix française mieux réussie ; [prise 1](https://suno.com/song/4cb614fb-abb5-4c65-8c1f-e19aa6b21b88) jugée trop rauque. Pas de jugement IA sur l'audio.
- **Interprétation expérimentale** : les deux prises partagent paroles, prompt et modèle. La différence de voix et de rythme n'est **pas** attribuable à un changement de prompt ; elle illustre la variabilité de deux sorties d'un même appel. Ne pas régénérer M08 sans hypothèse nouvelle.
- **Prochaine comparaison discriminante** : après approbation d'un nouveau texte, tester un mécanisme distinct (M02) sans présenter le résultat comme une comparaison contrôlée avec M08, puisque histoire et paroles diffèrent. Pour isoler une identité musicale, comparer des générations à paroles inchangées et recueillir un nouveau feedback humain.

## Discipline expérimentale

Pour comparer les **mécanismes**, maintenir autant que possible histoire, cibles, longueur et style comparables. Pour comparer les **styles**, conserver exactement les mêmes paroles. Pour comparer les **voix**, conserver paroles et arrangement autant que possible. Ne jamais attribuer une préférence à une variable quand plusieurs ont changé ensemble.
