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

## Contrôle lecture seule de la playlist réelle

Après une consultation Suno MCP de `Sonora — Hebdo`, appeler
`playlists_list_clips(id="152d06fb-bd76-4d7c-9eb3-b11bd3c90bde", limit=50)`
et **parcourir tous les `next_cursor`** jusqu'à épuisement. Fusionner les
`items` en un fichier JSON temporaire, par exemple `/tmp/sonora-playlist.json` :

```json
{
  "playlist_id": "152d06fb-bd76-4d7c-9eb3-b11bd3c90bde",
  "retrieved_at_utc": "2026-11-02T14:30:00Z",
  "complete": true,
  "items": []
}
```

Renseigner l'heure UTC **réelle de récupération** et `complete: true` uniquement
si toutes les pages ont été consultées. Garder les objets Suno bruts dans
`items` (le vérificateur utilise `id`). Ne pas commiter de snapshot
ponctuel : il périmerait. Le script refuse un snapshot de plus de 60 minutes,
un `next_cursor` non épuisé, une playlist différente ou des IDs dupliqués.

```sh
python3 scripts/check_weekly_playlist.py /tmp/sonora-playlist.json
python3 -m unittest discover -s tests -p 'test_weekly_playlist.py'
```

Ce contrôle **ne modifie ni Suno ni le journal**. Il bloque sur trois écarts :
clip Suno sans entrée de journal, clip marqué `added` mais absent de Suno,
ou clip présent dans Suno alors que le journal indique `not_added`/`removed`.
En cas d'écart, vérifier les deux sources et corriger seulement sur preuve ;
ne jamais créer de feedback humain ni d'approbation pour faire passer le check.
Les likes Suno ne servent pas de preuve d'approbation.
