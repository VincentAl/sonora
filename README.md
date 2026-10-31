# Sonora

Sonora explore l'apprentissage passif de l'espagnol par de **vraies chansons courtes**, écoutables pour elles-mêmes. Le français doit aider à comprendre quelques idées sans devenir une traduction ou une leçon.

**[ROADMAP.md](ROADMAP.md) est la source de vérité** : priorités, tâches en cours, contraintes et statut de validation. Les runs autonomes la lisent en premier.

## État du POC — 31 octobre 2026

- Suno MCP officiel connecté ; le modèle disponible via MCP est actuellement `v6-mini`.
- Quatre prises ont été générées pour 20 crédits, mais leur **structure de paroles a été rejetée** après retour humain : passages français trop proches de traductions, répétitions artificielles.
- Trois [nouvelles variantes de paroles](songs/drafts/2026-10-31-lyrics-preflight.md) sont **en attente de validation textuelle par Vincent**. Aucune génération ne doit être lancée pour elles avant validation.
- L'écoute, les accents, l'intelligibilité et la qualité musicale sont jugés **uniquement par Vincent**, pas par une analyse audio GPT.
- Budget opérationnel : jusqu'à 50 crédits Suno disponibles par jour, répartis entre les runs, mais **pas d'audio tant que les paroles correspondantes ne sont pas validées**.

## Workflow

1. Choisir les cibles et écrire des paroles narratives, avec peu de répétitions forcées.
2. Faire relire **les paroles seules** par Vincent. Corriger avant de consommer des crédits.
3. Enregistrer l'approbation explicite des paroles dans le manifeste de l'expérience (voir garde-fou ci-dessous).
4. Générer un petit lot de variantes musicales via Suno MCP, puis enregistrer IDs, URLs et crédits.
5. Attendre le retour d'écoute humain avant toute conclusion sur l'audio.

### Garde-fou de génération

Pour une expérience structurée dans `songs/experiments/<pack>/`, le manifeste doit contenir :

```json
"human_lyrics_approval": {
  "status": "approved",
  "reviewer": "Vincent",
  "lyrics_sha256": "<empreinte calculée après validation>"
}
```

Le hash porte sur les fichiers de paroles exacts. Toute modification de paroles annule automatiquement cette approbation.

```bash
python3 scripts/check_generation_gate.py songs/experiments/<pack>
python3 scripts/validate_all_experiments.py
python3 -m unittest discover -s tests -v
```

**Un run autonome doit vérifier le garde-fou avant tout appel Suno.** L'exportateur `scripts/prepare_suno_batch.py` est strictement hors ligne et marque les jobs non approuvés comme `awaiting_human_lyrics_approval`.

## Documentation

- [Spécification](docs/SPEC.md)
- [Règles pédagogiques](docs/PEDAGOGY_RULES.md)
- [Profil musical](docs/MUSIC_PROFILE.md)
- [Intégration Suno](docs/SUNO_INTEGRATION.md)
- [Journal de la première expérience audio](songs/experiments/2026-10-31-semantic-reset/README.md)
- [Suivi du vocabulaire](docs/VOCABULARY_TRACKING.md)
