# Sonora — scènes conversationnelles, prévalidation texte (31 octobre 2026)

**Statut : brouillons non approuvés. Zéro génération Suno autorisée.**

## Question testée

Comment une idée revient-elle naturellement entre deux personnages sans que le français ressemble à une traduction de l'espagnol ?

Retour explicite de Vincent : la variante C du lot précédent a davantage de potentiel ; **2 cibles par minute** conviennent aux prototypes, et une réponse qui réemploie la même notion **dans un autre contexte** est une bonne piste. Ce retour ne valide pas les paroles C existantes.

Ces trois essais gardent les **mêmes deux cibles** (`dejar atrás` et `añorar`) pour comparer surtout le mécanisme de dialogue. Chaque cible espagnole n'apparaît qu'une fois par version. Les répliques françaises doivent faire avancer la scène. Aucun de ces textes n'a encore été jugé naturel ou validé par Vincent.

## D1 — Écho, chacun laisse autre chose

*Mécanisme : deux départs de nature différente ; la seconde voix reprend une action, pas une phrase.*

```text
[Voix 1 — espagnol]
Dejé atrás la ciudad cuando amanecía.
No había nadie en la carretera.

[Voix 2 — français]
Moi, j'ai laissé tes clés sur le comptoir.
Tu pourras passer sans me voir.

[Voix 1 — espagnol]
Añoro tus pasos por el pasillo.

[Voix 2 — français]
C'est idiot, j'écoute encore l'escalier le soir.

[Voix 1 — espagnol]
Entonces no cierres todavía.
```

**Ancrages** : `dejar atrás` / « j'ai laissé tes clés » = départ vs objet abandonné ; `añorar` / « j'écoute encore l'escalier » = absence perceptible par une habitude. **Risque** : l'ancrage du manque est indirect ; la dernière réplique peut sembler forcée.

## D2 — Correction d'une interprétation

*Mécanisme : une personne croit avoir compris ; l'autre précise ce qu'elle regrette réellement.*

```text
[Voix 1 — espagnol]
Dejé atrás la casa, no la calle.
Aún sé dónde cruje el suelo.

[Voix 2 — français]
Tu dis que t'as tout quitté.
Mais tu connais encore chaque marche.

[Voix 1 — espagnol]
Añoro las noches en el balcón.

[Voix 2 — français]
Je croyais que c'était la ville qui te manquait.

[Voix 1 — espagnol]
No. Era cuando te quedabas conmigo.
```

**Ancrages** : `dejar atrás` / « tout quitté » = correction d'une généralisation ; `añorar` / « te manquait » = une supposition corrigée. **Risque** : « tout quitté » peut encore ressembler à une glose ; le dialogue peut paraître trop explicatif.

## D3 — Souvenir contradictoire

*Mécanisme : deux personnes se souviennent du même départ, mais pas des mêmes détails.*

```text
[Voix 1 — espagnol]
Dejé atrás el pueblo un martes de lluvia.
El tren llegó con una hora de retraso.

[Voix 2 — français]
Et moi j'ai laissé ma valise sur le quai.
Tu t'es moqué de moi tout le trajet.

[Voix 1 — espagnol]
Añoro aquel café de la estación.

[Voix 2 — français]
Il était imbuvable.
Tu me dis pourtant qu'il te manque encore.

[Voix 1 — espagnol]
No era por el café.
```

**Ancrages** : `dejar atrás` / « laissé ma valise » = parallèle comique ; `añorar` / « il te manque » = contradiction crédible entre goût et souvenir. **Risque** : le français peut sur-expliciter le second mot ; la chute devra être portée par la musique.

## Critère de décision (lecture seulement)

- Est-ce qu'on croirait ces répliques **dans une conversation réelle**, sans objectif pédagogique ?
- La réponse française apporte-t-elle une **nouvelle information** ou seulement un synonyme ?
- Peut-on retrouver le sens des deux cibles grâce à la scène entière ?
- Si une réplique est supprimée, perd-on quelque chose à l'histoire ? Sinon, elle est probablement décorative.

**Prochaine action :** obtenir une préférence et des corrections textuelles de Vincent, puis seulement préparer un pack validable par `scripts/check_generation_gate.py`. Ne pas traiter une préférence de mécanisme comme une approbation du texte final.
