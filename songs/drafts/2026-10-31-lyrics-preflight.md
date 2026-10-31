# Prévalidation textuelle — 31 octobre 2026

**Statut : en attente de relecture humaine des paroles. Aucun audio à générer à ce stade.**

## Pourquoi cette expérience ?

Vincent a rejeté la structure A/B précédente : phrases françaises qui ressemblent à des traductions empilées et répétitions forcées des cibles. Ces problèmes se voient sur le texte et ne justifient pas de dépense Suno.

Ce lot teste trois architectures narratives, sans prétendre que l'une est déjà validée. Les cibles espagnoles n'apparaissent **qu'une fois chacune**. Les ancrages français ne sont pas des sous-titres immédiats ; ils doivent contribuer un nouvel élément à l'histoire.

Les deux premiers essais gardent trois cibles ; le troisième est un **contrôle exploratoire à deux cibles** pour isoler l'effet de la densité. **Mise à jour du 31/10 : Vincent a retenu 2 cibles/minute comme densité de travail, sans approuver les paroles C.**

## A — Deux voix, une histoire (3 cibles)

*Hypothèse : le français prend une fonction dramatique (la réponse de la personne restée), plutôt que celle d'un glossaire.*

```text
[Verse — voix qui part, espagnol]
Dejé atrás el barrio sin cerrar la persiana.
Añoro tus pasos al subir la escalera.
Hallé una foto en el bolsillo del abrigo,
tu número estaba escrito detrás.

[Reply — voix qui reste, français]
Moi, j'ai laissé la lampe allumée.
Tes appels me manquent à l'aube.

[Turn — espagnol]
El tren se detiene; no bajo.

[Reply — français]
J'ai retrouvé ton message. Je n'ai pas répondu.
```

Ancrages :
- `dejar atrás` → « j'ai laissé la lampe allumée » : abandonner / laisser derrière soi quelque chose au départ ; **ancrage à vérifier**, « laisser allumée » peut être interprété différemment.
- `añorar` → « tes appels me manquent » : manque d'une présence familière.
- `hallar` → « j'ai retrouvé ton message » : découvrir / retrouver quelque chose.

Risque : deux points de vue et trois changements de langue peuvent être trop complexes pour une minute. L'ancrage de `dejar atrás` est probablement trop indirect.

## B — Deux époques, même narrateur (3 cibles)

*Hypothèse : la reprise française change le temps de l'histoire et révèle une évolution, plutôt que de traduire le couplet.*

```text
[Verse — espagnol, le départ]
Dejé atrás la casa antes del alba.
Añoro la taza rota de la cocina.
Hallé tu llave bajo la alfombra,
pero no abrí la puerta.

[Bridge — français, des années plus tard]
Des années plus tard, j'ai laissé ce quartier derrière moi.
Les matins me manquent moins qu'avant.

[Verse — espagnol]
Un día volví por la calle de siempre.

[Outro — français]
J'ai retrouvé la clé dans mon vieux manteau.

[Final — espagnol]
Ya no había puerta.
```

Ancrages :
- `dejar atrás` → « j'ai laissé ce quartier derrière moi » : quitter / dépasser un lieu et un passé.
- `añorar` → « les matins me manquent moins qu'avant » : nostalgie devenue moins vive.
- `hallar` → « j'ai retrouvé la clé » : trouver quelque chose perdu / oublié.

Risque : le français pourrait encore donner une impression de résumé des trois mots ; c'est précisément ce qu'il faut juger avant toute génération.

## C — Contrôle : deux cibles, moins de pression pédagogique

*Hypothèse : l'obligation de trois ancrages en une minute contribue elle-même au caractère artificiel. Le **principe** de 2 cibles/minute est maintenant retenu, mais ces paroles ne sont toujours pas approuvées pour génération.*

```text
[Verse — espagnol]
Dejé atrás la ciudad con el coche sin radio.
Añoro tu risa en el asiento de al lado.
El cielo todavía huele a lluvia,
y el puente desaparece detrás.

[Chorus — français]
J'ai laissé nos clés sur la table.
Ton rire me manque au premier feu rouge.

[Outro — espagnol]
Me pregunto si vas a buscarlas.
Sigo conduciendo.
```

Ancrages :
- `dejar atrás` → « j'ai laissé nos clés sur la table » : abandonner quelque chose en partant.
- `añorar` → « ton rire me manque » : ressentir l'absence de quelqu'un.

Risque : deux lignes françaises restent très proches du couplet espagnol, mais elles ajoutent des objets et une action à l'histoire. À vérifier : peut-on réduire encore cet effet de traduction ?

## Décision humaine attendue

Lire les paroles **sans écouter de musique** et déterminer :
1. Est-ce que le français sonne comme une partie de la chanson ou comme une traduction déguisée ?
2. Laquelle des structures A / B / C a le plus de potentiel narratif ?
3. Pour les 2 cibles/minute désormais retenues : quelle forme de dialogue rend leur réemploi le plus naturel ? Voir [les scènes D1/D2/D3](2026-10-31-dialogue-mechanisms.md).

Ne pas déduire d'un contrôle lexical automatique que le résultat est naturel ou pédagogiquement efficace.

## Garde-fou d'exécution

- **0 crédit Suno** pour ce lot tant que la structure n'est pas explicitement approuvée.
- Aucun alignement, transcription, analyse audio ou scoring GPT.
- Après feedback, corriger le texte puis ne lancer qu'une expérience musicale discriminante sur des paroles approuvées.
