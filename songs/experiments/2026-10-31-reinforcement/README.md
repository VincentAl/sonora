# Expérience 02 — quand ancrer le sens ?

**Paroles originales uniquement. Aucun audio Suno généré.**

## Pourquoi ce deuxième lot

L'expérience 01 introduit quatre cibles, mais ne donne un ancrage français explicite qu'à **añorar** et **dejar atrás**. Ce nouveau morceau réemploie les quatre cibles et ancre les deux autres : **sosiego → quiétude** et **hallar → trouver**. Les deux phrases françaises sont autonomes, imagées et ne traduisent pas la phrase espagnole précédente.

## Hypothèse discriminante

À paroles constantes, placer les deux ancrages **après la première exposition espagnole, avant le refrain** (A) pourrait améliorer la compréhension immédiate ; les placer **après le refrain** (B) pourrait préserver davantage l'inférence initiale et la fluidité musicale. Ce sont des hypothèses, **pas des résultats**.

- A et B ont les mêmes 10 lignes espagnoles, dans le même ordre.
- A et B ont les mêmes 2 lignes françaises, dans le même ordre.
- Seule la position du pont français change ; le prompt indie-pop reste identique.
- Deux prises par variante sont prévues, soit **4 jobs hors ligne**. Aucun crédit n'est dépensé.

| Cible | Statut dans cette chanson | Ancrage français |
| --- | --- | --- |
| añorar / añoro | Réapparition en espagnol, sans traduction | déjà ancré dans le lot 01 |
| dejar atrás / dejo atrás | Réapparition en espagnol, sans traduction | déjà ancré dans le lot 01 |
| sosiego | Nouvel ancrage exact | « Le jardin garde sa quiétude après la pluie. » |
| hallar / hallo | Nouvel ancrage exact | « Au fond du tiroir, j'ai trouvé ta lettre. » |

## Comment comparer sans se tromper

Utiliser le protocole de `docs/EXPERIMENT_PROTOCOL.md` : écouter sans paroles affichées, noter la diction, les transitions et la naturalité ; mesurer le rappel immédiat et à 24 h. **Ne pas faire écouter A et B à la même personne** pour comparer la mémorisation : les expositions successives se contaminent. Ne pas faire écouter l'expérience 01 aux participants de cette comparaison, sauf si l'exposition antérieure est identique et documentée dans chaque groupe.

Les deux ancrages sont consécutifs et peuvent être plus difficiles à chanter que deux passages espacés. Si le rendu est précipité, noter le problème plutôt que changer seulement une variante : cela briserait le contrôle.

## Exécution

```sh
python3 scripts/validate_all_experiments.py
python3 -m unittest discover -s tests -v
python3 scripts/prepare_suno_batch.py songs/experiments/2026-10-31-reinforcement artifacts/suno-reinforcement
```

Les quatre JSON générés sont des instructions de copier-coller, pas des audios. La génération reste bloquée tant que le compte Suno n'a pas accès au MCP et qu'aucun budget de crédits n'est autorisé.
