# Sonora — protocole de comparaison musicale à paroles constantes

**Statut : plan de test uniquement. Aucun audio autorisé tant que Vincent n'a pas approuvé les paroles intégrales exactes.**

## Question expérimentale

Une chanson bilingue complète utilisant M01 (écho conversationnel) fonctionne-t-elle musicalement sans donner l'impression d'un exercice ? Une fois le texte validé, quel traitement musical est préféré ?

## Conditions fixes

- **Paroles identiques** dans chaque condition (fichier et SHA-256 conservés) : [La luz del pasillo V0](../songs/drafts/2026-11-01-la-luz-del-pasillo-full.md) ou sa future version approuvée.
- Même modèle Suno disponible, mêmes paramètres de durée, même répartition des voix et mêmes indications de langue.
- Pas de modification des quatre cibles, du scénario ou des reprises françaises pendant la comparaison de styles.
- Conserver les deux prises produites par appel et leurs identifiants, sans choisir automatiquement la meilleure.

## Variable étudiée : arrangement musical seulement

| Condition | Style (direction, pas imitation) | Hypothèse |
| --- | --- | --- |
| A | Indie acoustique sombre : guitare sèche, basse discrète, percussion organique | Préserve la proximité du dialogue |
| B | Folk ibérique brut : guitare plus rythmique, percussions sèches, tension croissante | Donne plus d'élan sans pop sucrée |
| C (optionnelle) | Minimalisme nocturne : piano parcimonieux, textures graves, batterie contenue | Rend les paroles plus intelligibles |

**Séquence** : après approbation explicite du texte, créer un pack avec manifeste et hash d'approbation ; exécuter `check_generation_gate.py` et `check_suno_budget.py` avant chaque appel. Générer A et B lors de runs séparés si le solde le permet ; C uniquement si A/B ne départagent pas l'hypothèse. Ne pas présumer d'un rechargement quotidien du solde Free.

## Grille de retour humain (sans jugement IA de l'audio)

Vincent écoute à l'aveugle si possible et note : préférence globale, chanson naturelle ou exercice déguisé, énergie, clarté des bascules FR/ES, refrain mémorable, prononciation (à ne pas conclure sur mini). Enregistrer la préférence par clip et la raison donnée ; ne pas attribuer à un style un effet dû à une variation aléatoire de génération.

## Après comparaison

- Si le texte échoue : réécrire et refaire valider ; ne pas masquer le problème avec un style différent.
- Si un style est prometteur : le conserver comme candidat, sans le déclarer vainqueur sur deux clips.
- **Voix récurrente** : expérience séparée. Vérifier d'abord les fonctions réellement exposées par Suno et leur coût ; ne pas promettre une chanteuse identique d'un titre à l'autre.
- **Playlist hebdomadaire** : chantier distinct, après validation d'au moins une chanson complète et vérification des intégrations disponibles.

## Limites du contrôle statique

`scripts/audit_full_draft.py` compte sections, lignes, mots et occurrences exactes des cibles. Il ne valide ni le sens précis des ancrages, ni le naturel, ni la durée audio. Le validateur des packs accepte désormais davantage de lignes françaises pour les chansons longues, sans accorder d'approbation humaine.
