# Sonora — machine d'états du morceau hebdomadaire (proposition V0)

> Document de conception uniquement. Aucune automatisation de publication, aucune approbation implicite et aucun appel Suno. `ROADMAP.md` sur `main` reste prioritaire.

## Unité suivie

Une **version de morceau** est identifiée par `song_id` et par le SHA-256 des **paroles exactes**. Une modification de paroles crée une nouvelle version et invalide l'approbation textuelle précédente. Un clip audio est une **prise** associée à cette version, jamais une nouvelle version des paroles.

## États et transitions

| État | Entrée vérifiable | Transition permise | Acteur |
| --- | --- | --- | --- |
| `draft` | Paroles + cibles + ancrages FR/ES documentés | `text_review` après prévalidation structurelle | Automatisation |
| `text_review` | Texte soumis, hash conservé | `text_approved` sur approbation explicite du texte exact, ou `draft` sur correction | Vincent / automatisation |
| `text_approved` | Preuve d'approbation liée au hash | `generation_ready` si pack figé et gate validé | Automatisation |
| `generation_ready` | Gate APPROVED, solde Suno vérifié, budget PASS | `generation_requested` au plus une fois par run | Automatisation |
| `generation_requested` | ID de requête ou identifiant de corrélation enregistré avant toute nouvelle tentative | `audio_review` lorsque les clips et la dépense réelle sont consignés ; sinon `generation_unknown` | Automatisation |
| `generation_unknown` | Réponse perdue / statut incertain | Réconciliation par IDs et compte Suno, **jamais de nouvelle génération aveugle** | Automatisation |
| `audio_review` | Clips, URLs, paramètres et crédits consignés | `audio_approved` ou `rejected` sur retour explicite | Vincent |
| `audio_approved` | Prise précisément désignée et validée | `published` uniquement si `selection=kept`, `audio_approved=true` et `pedagogy_approved=true` pour cette prise, puis ajout confirmé à la playlist et journal cohérent | Automatisation |
| `published` | Clip présent dans playlist et journal cohérent | État final pour cette prise ; le retrait est une action explicite distincte | Automatisation |
| `rejected` | Motif humain enregistré sans jugement GPT | État final pour la prise ; nouveau brouillon/version si nécessaire | Vincent |

Les états concernent deux niveaux : `draft` à `generation_requested` décrivent la **version des paroles** ; `audio_review` à `published` décrivent chaque **prise**. Plusieurs prises d'un même appel peuvent diverger en statut. Ne jamais considérer une prise approuvée parce que sa sœur l'est.

## Invariants bloquants

1. Aucun appel Suno sans approbation humaine explicite du hash exact, `check_generation_gate.py` = APPROVED et `check_suno_budget.py` = PASS avec solde frais.
2. Une PR ouverte, une CI verte, un texte corrigé ou un avis positif sur une autre prise **ne constituent pas** une approbation.
3. Pas de publication sans `selection=kept`, `audio_approved=true` **et** `pedagogy_approved=true` pour **la prise concernée**. Ces trois conditions sont distinctes ; le like Suno ne remplace aucune d'elles. Le validateur `scripts/validate_weekly_feedback.py` doit confirmer leur cohérence avant de considérer `playlist_state=added`.
4. Pas de double dépense après timeout : enregistrer le statut inconnu, retrouver la requête ou s'arrêter pour vérification.
5. Le journal de crédits contient les montants réellement constatés, y compris un décrément différé ; un solde inchangé juste après l'appel ne signifie pas zéro dépense.
6. Une notion n'entre dans la planification de réexposition qu'après publication vérifiée, pas après génération.
7. Ne jamais inférer un feedback musical à partir d'un traitement automatique du son.

## Reprises et erreurs

- **Paroles modifiées après approbation :** retour à `draft`, invalidation du hash et du pack ; aucune réutilisation de l'ancien feu vert.
- **Échec CI ou audit :** rester dans l'état actuel, corriger dans la PR existante et relancer les checks déterministes ; ne pas débloquer Suno.
- **Suno renvoie une erreur certaine sans génération :** conserver l'erreur et retenter seulement après précontrôles frais, dans la limite du run.
- **Suno timeout / réponse ambiguë :** `generation_unknown`, inspecter bibliothèque/usage/IDs avant toute autre dépense.
- **Clip généré, crédits non encore décrémentés :** consigner l'observation provisoire, revérifier et corriger le journal sur dépense confirmée.
- **Ajout playlist partiellement réussi :** vérifier les `clip_id` effectivement présents ; ne marquer `published` que ceux confirmés. Réconcilier avec `check_weekly_playlist.py`.
- **Feedback absent :** rester en revue, avancer sur un autre chantier ; pas de relance audio ou de promotion automatique.

## Données minimales pour une future implémentation

`song_id`, `lyrics_sha256`, `text_approval` (auteur/date/hash), `generation_request_id` (si fourni), `run_id`, `clip_id`, `credits.before/after/spent`, `audio_feedback` (auteur/date/prise/verdict), `playlist_id`, `published_at`.

Ne pas créer une seconde base de vérité : réutiliser les manifestes, journaux `songs/experiments/**/runs/*.json` et `data/weekly_feedback.json` existants. Cette spécification décrit les transitions, **pas** un nouveau format imposé.

## Cas d'acceptation à automatiser ultérieurement

- Approbation sur hash A, paroles modifiées en B : génération bloquée.
- Deux prises : A approuvée musicalement mais sans approbation pédagogique, B rejetée ; aucune ne peut être publiée. Après `selection=kept` et approbation pédagogique explicites pour A, seule A peut être publiée.
- Timeout Suno : aucune seconde requête tant que l'état n'est pas réconcilié.
- Ajout playlist confirmé mais journal absent : anomalie, pas de publication réputée cohérente.
- Génération réussie, audio non revu : aucun titre ajouté à la playlist.
