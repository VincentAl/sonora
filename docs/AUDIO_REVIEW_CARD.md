# Sonora — fiche de revue d'une prise audio

**But :** obtenir une décision exploitable en moins de deux minutes d'écoute, sans analyse audio par GPT. Ce formulaire ne remplace **jamais** l'approbation préalable des paroles exactes. Aucun statut n'est déduit d'un like Suno.

## Avant de demander une écoute

- Fournir le titre, la PR/expérience, les liens **des deux clips** du même appel, le modèle, le texte figé et son SHA-256, ainsi que la question expérimentale.
- Si le texte n'est pas approuvé explicitement par Vincent : **rester en revue textuelle** ; ne pas générer pour remplir le questionnaire.
- Si la génération est issue de `v6-mini`, éviter toute conclusion définitive sur l'accent ou la prononciation.

## Réponse rapide à copier (une par clip, ou comparaison A/B)

```text
Expérience :
Clip(s) :
Écouté(s) : oui / non
Préférence : A / B / aucun / impossible à départager
Chanson naturelle (pas un exercice) : oui / mitigé / non
Énergie / style : bon / trop mou / trop sucré / autre :
Transitions français–espagnol : naturelles / gênantes / inaudibles
Ancrages de vocabulaire : clairs / incertains / incorrects (lesquels ?)
Prononciation : OK / à revoir / non évaluée (mini)
Décision : poursuivre / retravailler le texte / tester un autre style / rejeter
Commentaire libre (facultatif) :
```

## Interprétation autorisée

- Une **préférence A/B** est une préférence de Vincent entre ces prises, pas la preuve qu'un style est intrinsèquement meilleur : la génération est stochastique.
- `poursuivre` n'est **ni** une approbation automatique de toutes les notions, **ni** une autorisation de publier.
- `rejeté` doit venir d'un feedback explicite, jamais de l'absence de like ou d'un `unlike`.
- Une question non évaluée reste `unknown` ; ne jamais la convertir en `approved`.
- Le journal par clip doit conserver les mots de Vincent, la date, la décision et la question testée ; les conclusions synthétiques doivent renvoyer à ce retour.

## Deux validations indépendantes avant playlist

1. **Validation pédagogique** : correspondances FR/ES exactes et utilité des reprises, sur feedback explicite.
2. **Validation audio / publication** : écoute et accord explicite de Vincent pour ce clip précis.

Sans les deux, le clip reste candidat ou rejeté ; ne pas l'ajouter à la playlist hebdomadaire. Cette fiche ne modifie aucun état à elle seule.

## Ordre de revue recommandé

Prioriser **un seul texte complet** à valider pour débloquer le premier test musical long, puis comparer les mécanismes concurrents à vocabulaire constant. Ne pas demander à Vincent de relire toutes les PR d'un coup. Pendant l'attente, l'automatisation avance sur les chantiers indépendants.
