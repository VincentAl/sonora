# Sonora — contrat du cycle de vie d'un morceau (V0)

Objectif : éviter qu'un brouillon, une génération Suno, un like ou une PR ouverte soit pris pour une approbation. Ce document décrit un **contrat de workflow**, pas un nouvel état de validation. Les sources existantes restent les manifestes, les gates et le journal hebdomadaire.

## États et transitions

| État | Entrée vérifiable | Sortie permise | Interdit |
| --- | --- | --- | --- |
| `draft` | Paroles et cibles en cours de rédaction | `text_review` quand un texte exact est soumis | Appel Suno |
| `text_review` | Texte figé proposé à Vincent, aucune approbation présumée | `text_approved` uniquement sur accord explicite lié au SHA-256 des paroles ; retour à `draft` si réécriture | Déduire l'accord d'une PR ouverte ou d'une CI verte |
| `text_approved` | Hash exact approuvé et gate `APPROVED` | `generated` après précontrôles et appel Suno réussi | Générer après changement d'un seul caractère du texte |
| `generated` | IDs/URLs, modèle, paramètres, date et crédits réels journalisés | `audio_review` | Marquer publié, appris ou accepté par défaut |
| `audio_review` | Clip individuel soumis à Vincent | `kept` ou `rejected` sur feedback explicite ; sinon rester en attente | Inférer le rejet d'un unlike, ou l'approbation d'un like |
| `kept` | Décision `kept`, approbations audio **et** pédagogie distinctes | `published` après ajout Suno confirmé et journal mis à jour | Publication sur simple préférence musicale |
| `published` | Clip présent dans la playlist et journal `playlist_state=added` | Suivi des expositions de vocabulaire, retrait explicite éventuel | Confondre publication et mémorisation |

Le cycle est **par clip** à partir de la génération : un appel peut produire deux clips qui reçoivent deux décisions différentes. Les états ci-dessus ne remplacent pas les champs existants de `data/weekly_feedback.json`. Ils en sont une lecture opérationnelle.

## Préconditions exactes d'une génération

1. Vérifier que la PR du texte ne se contente pas d'être ouverte : l'approbation humaine concerne les **paroles exactes**, non une branche ou une idée.
2. Calculer/contrôler le hash des paroles et exécuter `scripts/check_generation_gate.py` sur le pack ; résultat obligatoire : `APPROVED`.
3. Lire le solde Suno actuel, puis exécuter `scripts/check_suno_budget.py --cost 10 --balance <solde_actuel>` ; résultat obligatoire : autorisé.
4. Ne faire qu'un appel de génération sur le run, sans achat, et journaliser `run_id`, clips, paramètres et consommation réelle. Si le solde n'a pas encore été débité, le revérifier avant de conclure que la consommation est nulle.

## Reprise après interruption / échec

| Interruption | Reprise sûre |
| --- | --- |
| Texte modifié après approbation | Retour `text_review`, nouvel accord lié au nouveau hash ; **aucune génération** |
| Gate ou budget bloqué | Pas d'appel Suno ; traiter une autre tâche indépendante |
| Appel Suno sans réponse claire | Consulter l'historique/IDs Suno avant tout nouvel appel, pour éviter un doublon facturé |
| Clips reçus, journal non commité | Reconstituer uniquement les faits vérifiables (IDs, URLs, crédits) ; pas d'avis humain inventé |
| Feedback partiel | Conserver les décisions réellement exprimées ; laisser les approbations manquantes à `false` |
| Ajout playlist incertain | Relire la playlist et comparer avec `scripts/check_weekly_playlist.py` avant tout nouvel ajout |
| PR non mergée | Continuer le travail indépendant sur une autre PR ; ne pas changer `main` |

## Invariants vérifiables à automatiser ensuite

- `playlist_state=added` implique `selection=kept`, `audio_approved=true` et `pedagogy_approved=true` (déjà contrôlé par `validate_weekly_feedback.py`).
- Un clip ne figure qu'une fois dans le journal ; un ID Suno ne vaut pas approbation (déjà contrôlé).
- Les transitions qui dépendent de Vincent doivent référencer son feedback explicite ; ne pas le synthétiser à partir de métriques ou d'une analyse GPT.
- La génération ne doit jamais précéder la validation du hash ni les contrôles du solde réel.
- Une reprise après échec doit être idempotente côté playlist et journal ; **à tester** avant automatisation de la publication.

## Cas d'acceptation manuels avant automatisation

1. Approuver un texte, modifier un caractère, constater le blocage du gate.
2. Simuler deux clips issus d'un appel : approuver l'un, laisser l'autre `pending`, constater qu'un seul peut être promu.
3. Simuler un like sans approbation pédagogique : publication refusée.
4. Simuler un ajout Suno réussi sans journal `added` : contrôle de cohérence en échec, puis réconciliation sur preuve.
5. Simuler un timeout après génération : la procédure doit retrouver les IDs existants, sans second appel automatique.

Aucune de ces simulations n'autorise une génération réelle. Le présent document ne modifie ni les validations en attente ni le budget Suno.
