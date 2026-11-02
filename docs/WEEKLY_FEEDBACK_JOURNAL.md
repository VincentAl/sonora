# Sonora — journal hebdomadaire de sélection

Le journal machine-readable est [`data/weekly_feedback.json`](../data/weekly_feedback.json).
Il commence **vide** : les prises D1 sont des tests, pas des titres approuvés
pour la playlist hebdomadaire. Ajouter une entrée par **clip Suno**, jamais une
entrée par génération (un appel peut produire deux clips).

## Champs

- `clip_id` : identifiant Suno réel, unique.
- `generated_at_utc` : date UTC de génération ; `song` : titre ;
  `mechanism` : ID du bestiaire, par exemple `M01` ;
  `targets` : notions espagnoles réellement visées.
- `selection` : `pending`, `liked`, `rejected` ou `kept`.
  `liked` exprime une préférence, **pas** une approbation de l'audio
  ou de la pédagogie. `rejected` nécessite un retour humain explicite :
  l'absence d'un like Suno ne prouve rien.
- `human_feedback` : `null` tant qu'il n'y a pas de décision ; sinon
  `{"quote":"citation exacte","source":"conversation Sonora","at_utc":"2026-11-02T12:00:00Z"}`.
  Ne pas fabriquer de citation ni déduire un avis d'une métrique Suno.
- `audio_approved` et `pedagogy_approved` : deux décisions **distinctes**
  et explicites de Vincent, `false` par défaut. La validation textuelle
  par hash reste gérée séparément par `check_generation_gate.py`.
- `playlist_state` : `not_added`, `added`, `removed`.
  `added` est autorisé uniquement avec `kept` et les deux approbations.
  Cela n'ajoute **pas** automatiquement un titre sur Suno.

## Cycle opérationnel

1. Après génération autorisée, enregistrer les clips en `pending`.
2. À réception du feedback explicite de Vincent, mettre à jour la sélection,
   conserver sa citation et ne renseigner les approbations que si elles sont
   réellement exprimées.
3. Quand un clip est `kept` et approuvé musicalement **et** pédagogiquement,
   l'ajouter à [Sonora — Hebdo](https://suno.com/playlist/152d06fb-bd76-4d7c-9eb3-b11bd3c90bde)
   via Suno MCP, vérifier l'ajout, puis seulement inscrire `added`.
4. Vérifier localement : `python3 scripts/validate_weekly_feedback.py`.
   Tests : `python3 -m unittest discover -s tests -p 'test_weekly_feedback.py'`.

Ce journal est un historique de décisions, **pas** un moteur de SRS ni un
système de mesure de mémorisation. Les likes Suno ne sont pas synchronisés
automatiquement et ne remplacent jamais le feedback explicite.
