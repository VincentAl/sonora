# Sonora — scènes conversationnelles, prévalidation texte (révision sémantique, 1 novembre 2026)

**Statut : brouillons non approuvés. Zéro génération Suno autorisée.**

## Règle centrale

Le français et l'espagnol ne doivent ni :
- traduire la même phrase mot à mot ;
- ni simplement partager une ambiance.

Pour chaque cible, les deux langues doivent exprimer **la même idée sémantique**, dans deux formulations ou contextes naturels différents.

Exemple de mécanisme attendu :
- espagnol : « Dejé atrás la ciudad. »
- français : « J'ai laissé les clés sur la table. »

Le contenu concret change, mais l'idée cible — **laisser quelque chose derrière soi / abandonner en partant** — est bien présente des deux côtés.

Autre exemple :
- espagnol : « Añoro aquellas noches. »
- français : « Tes matins me manquent encore. »

Le souvenir change, mais l'idée cible — **ressentir le manque / la nostalgie de quelque chose** — est clairement répétée.

Cibles de ce lot :
- `dejar atrás` → laisser derrière soi / abandonner en partant
- `añorar` → regretter / ressentir le manque avec nostalgie

---

## D1 — Deux départs qui se répondent

```text
[Voix 1 — espagnol]
Dejé atrás la ciudad antes del amanecer.
Ni siquiera miré por el retrovisor.

[Voix 2 — français]
J'ai laissé tes clés sur la table,
à côté du café froid.

[Voix 1 — espagnol]
Añoro las noches en que llegabas tarde.

[Voix 2 — français]
Tes matins pressés me manquent encore.

[Voix 1 — espagnol]
Supongo que cada uno se fue a su manera.
```

### Paire sémantique
- `dejar atrás` : quitter la ville / laisser les clés en partant → même idée de laisser quelque chose derrière soi.
- `añorar` : regretter les nuits / les matins qui manquent → même idée de nostalgie.

Le dialogue avance : chacun révèle ce qu'il a laissé et ce qui lui manque.

---

## D2 — Ce qu'on croyait avoir quitté

```text
[Voix 1 — espagnol]
Dejé atrás la casa sin cerrar las cortinas.

[Voix 2 — français]
J'ai laissé les photos dans le dernier tiroir.

[Voix 1 — espagnol]
Pensé que eso bastaría.

[Voix 2 — français]
Moi aussi.

[Voix 1 — espagnol]
Añoro las cenas que terminaban demasiado tarde.

[Voix 2 — français]
Les silences après minuit me manquent davantage.

[Voix 1 — espagnol]
Entonces no era la casa.
```

### Paire sémantique
- `dejar atrás` : laisser la maison / laisser les photos → même action sémantique, objets différents.
- `añorar` : nostalgie des dîners / manque des silences → même sentiment appliqué à deux souvenirs du même passé.

Note : « Moi aussi » n'est pas ici utilisé comme mécanisme pédagogique ; c'est une réponse courte au constat « je pensais que ça suffirait ». À supprimer si ça sonne encore trop parlé/enfantin.

---

## D3 — Même voyage, souvenirs différents

```text
[Voix 1 — espagnol]
Dejé atrás el pueblo bajo la lluvia.
El tren salió con una hora de retraso.

[Voix 2 — français]
J'ai laissé ma valise sur le quai.
On s'en est aperçu après la frontière.

[Voix 1 — espagnol]
Añoro aquel café de la estación.

[Voix 2 — français]
Le vieux serveur me manque plus que son café.

[Voix 1 — espagnol]
Nunca fue por el café.

[Voix 2 — français]
Je sais.
```

### Paire sémantique
- `dejar atrás` : laisser le village derrière soi / laisser la valise derrière soi → même idée, deux objets différents dans la même scène.
- `añorar` : nostalgie du café comme souvenir / manque du serveur → même idée de nostalgie, mais la seconde voix précise ce qui comptait réellement.

D3 reste la piste la plus prometteuse parce que la répétition sémantique naît directement du souvenir partagé.

## Critère obligatoire avant Suno

Pour chaque cible, on doit pouvoir remplir cette phrase :

> En espagnol, la cible veut dire **X** dans la situation **A** ; en français, la même idée **X** réapparaît dans la situation **B**.

Si **X** n'est pas clairement identique, le texte est rejeté avant génération.

Aucune génération Suno avant validation explicite du texte par Vincent.
