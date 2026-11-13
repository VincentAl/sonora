# Sonora — shortlist déterministe de vocabulaire (V0)

Objectif : proposer des notions **à examiner** pour une prochaine chanson, sans demander à GPT de recompter l'historique à chaque run. Ce n'est ni un test de mémorisation, ni une décision éditoriale automatique.

## Sources et statuts

- `data/vocabulary.json` est un petit registre éditorial versionné : chaque cible possède un **ID de sens lexical** (pas seulement un mot), son expression espagnole, un sens français, une priorité manuelle de 1 à 5 et un statut `candidate` ou `retired`.
- `history` contient des événements datés : `draft`, `generated`, `published`. **Seul `published` constitue une exposition potentielle** pour la programmation de reprises. Même une publication ne prouve ni écoute ni apprentissage.
- Un mot réservé dans un brouillon ou une génération non publiée n'est pas proposé pour une autre chanson : on évite de dupliquer une expérience encore en revue. Une publication ultérieure le libère pour une reprise espacée.
- Les quatre mots de *La luz del pasillo* sont enregistrés uniquement comme `draft` ; les quatre nouveaux candidats sont des **propositions éditoriales**, non validées par Vincent.
- Lorsqu'une chanson est réellement diffusée, ajouter une ligne `published` par cible **après** vérification de la publication. Ne jamais inférer ce statut d'un brouillon, d'une génération, d'un like ou d'une simple présence dans la playlist non approuvée.

## Utilisation

Depuis la racine du repo :

```sh
python3 scripts/plan_vocabulary.py --as-of 2026-11-02 --limit 5 --revisit-days 14 --revisit-slots 1
python3 -m unittest discover -s tests -p 'test_plan_vocabulary.py'
```

La date est explicite pour rendre les sorties reproductibles. Le planificateur privilégie au plus une notion déjà publiée, dont la dernière publication remonte à au moins 14 jours ; il complète par de nouvelles notions classées par priorité manuelle puis ID. Si la réserve est insuffisante, il retourne **moins** de cinq notions au lieu d'en inventer. Les notions réservées sont exclues. Le résultat est une suggestion JSON, pas une modification du registre.

**Limites importantes :** 14 jours et une reprise par chanson sont des paramètres exploratoires, **pas** une courbe d'oubli validée. Le système n'observe pas encore l'écoute réelle, la compréhension ni les goûts de Vincent. Avant d'écrire une chanson, un humain doit vérifier l'utilité du vocabulaire, le sens exact, la cohérence narrative, les ancrages français et l'absence de traduction scolaire. Les validations de paroles et de génération Suno restent indépendantes.

## Réservations de vocabulaire dans les PR ouvertes

Le registre sur `main` ne contient pas les brouillons **non fusionnés**. Exemple réel : la [PR #3](https://github.com/VincentAl/sonora/pull/3) utilise déjà `darse cuenta`, `atreverse`, `aguantar` et `aprovechar`, alors que ces quatre cibles sont encore libres dans `data/vocabulary.json` sur `main`. Sans précaution, le planificateur pourrait les proposer une seconde fois.

Avant toute nouvelle sélection, consulter les PR ouvertes et leurs commentaires. Transmettre les IDs des notions déjà réservées dans les PR au planificateur :

```sh
python3 scripts/plan_vocabulary.py --as-of 2026-11-02 --limit 5 \
  --reserve-id darse-cuenta-realize \
  --reserve-id atreverse-dare \
  --reserve-id aguantar-endure \
  --reserve-id aprovechar-opportunity
```

Les quatre notions de M01 sont déjà réservées dans l'historique sur `main` ; les quatre de M02 sont exclues via ces arguments. Le résultat est donc une liste vide **jusqu'à ajout de nouveaux candidats** ou libération d'une réservation. `external_reserved` permet d'auditer les exclusions. Un ID inconnu ou dupliqué est une erreur, jamais ignorée silencieusement.

Cette interface est volontairement explicite : elle **ne lit pas automatiquement GitHub** et n'infère pas les cibles d'un texte libre. Les routines doivent relire les PR ouvertes et passer les réservations pertinentes à chaque sélection. Lorsqu'une PR est fusionnée et que ses événements `draft` figurent dans le registre sur `main`, ne plus passer ces IDs en réservation externe. Aucun statut `published` n'est créé par ce contrôle.
