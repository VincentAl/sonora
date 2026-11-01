# Sonora — Roadmap autonome

> Source de vérité pour les priorités courantes de Sonora.
>
> Chaque run autonome doit lire ce fichier **avant de choisir son travail**.
> Le prompt de l'automatisation définit le harnais stable ; ce fichier contient les objectifs, priorités et tâches mouvantes.
> Les discussions avec Vincent peuvent modifier cette roadmap à tout moment.

## Vision

Créer des chansons qu'on peut écouter normalement en travaillant, qui enseignent passivement du vocabulaire espagnol à un francophone.

La musique est le vecteur. L'objectif produit reste l'apprentissage.

## Règles produit stables

- Une chanson doit sonner comme une vraie chanson, jamais comme un exercice.
- Pour les tests d'une minute : viser **2 mots / idées cibles**. Sur une chanson finale d'environ 3 minutes, viser environ **4–5 notions** avec répétitions naturelles.
- Chaque cible doit être compréhensible en espagnol dans le contexte et recevoir un ancrage français naturel à l'échelle du morceau.
- Pas de traduction phrase par phrase.
- Pas d'introduction pédagogique parlée.
- POC : viser environ 45–60 secondes et une intro très courte.
- Direction musicale actuelle : intime, organique, sombre ou brute ; éviter cute/twee/cozy, pop sucrée et petit beat rond « boum boum ».
- `v6-mini` sert au prototypage ; ne pas valider les accents/prononciations sur mini.
- V6 complet reste la cible de validation finale lorsqu'il devient accessible.

## Répartition des responsabilités

### Automatisation / GPT

Peut :
- préparer paroles, prompts et variantes ;
- sélectionner les expériences discriminantes ;
- générer via Suno MCP ;
- enregistrer paramètres, IDs, URLs et crédits consommés ;
- maintenir le repo, les scripts, tests et données ;
- tirer des conclusions à partir du **feedback explicite de Vincent**.

Ne doit PAS :
- analyser subjectivement l'audio ;
- transcrire/aligner automatiquement l'audio dans le seul but d'évaluer la qualité ;
- utiliser des modèles IA pour juger « trop mimi », accent, qualité musicale, émotion, intelligibilité ou préférence ;
- consommer des tokens GPT pour des métriques qu'un script déterministe peut calculer.

### Vincent

Est la référence pour l'écoute :
- qualité musicale ;
- style ;
- voix ;
- accent français / espagnol ;
- intelligibilité ;
- naturel des transitions ;
- efficacité pédagogique ressentie.

Un audio généré reste « en attente de revue humaine » jusqu'à son feedback.

## Budget Suno

Objectif opérationnel : **utiliser jusqu'à 50 crédits Suno disponibles par jour**, sans achat ni changement de plan.

La routine tourne toutes les 3 heures, soit 8 runs par jour.

Comme un appel de génération observé coûte environ 10 crédits et produit 2 morceaux :
- viser environ **5 appels de génération par jour** au total ;
- répartir ces appels entre les runs plutôt que les lancer tous d'un coup ;
- les ~3 autres runs sont principalement consacrés au repo, aux paroles, au vocabulaire, aux tests et à la préparation ;
- maximum 1 appel de génération par run sauf raison exceptionnelle documentée ;
- vérifier le solde réel Suno avant de générer ;
- exécuter **avant chaque appel** `python3 scripts/check_suno_budget.py --cost 10 --balance <solde_Suno_actuel>` ; si le résultat est BLOCKED, ne pas générer ;
- après chaque appel réussi, enregistrer et commiter immédiatement un journal `songs/experiments/<expérience>/runs/*.json` avec `run_id`, `generated_at_utc` et `credits.before/after/spent` ; le contrôle additionne ces journaux sur la journée de Paris ;
- ne jamais dépasser le solde disponible ;
- ne jamais acheter de crédits.

Le chiffre de 50/jour est le budget de travail actuel demandé par Vincent. Si le comportement réel du quota Suno diffère, consigner l'observation et respecter le solde réellement disponible.

## État actuel — 31 octobre 2026

### Suno

- MCP connecté au compte `vincent_alfaro`.
- Modèle exposé via MCP : `v6-mini`.
- Premier smoke test réel effectué.
- 4 clips générés pour 20 crédits.
- 80 crédits restaient après le test.
- Ces 4 clips ont reçu un premier feedback humain sur la structure bilingue.

### Compatibilité du pipeline

- Le validateur `scripts/validate_experiment.py` accepte désormais **2–5 cibles** : auparavant il imposait 3–4 et aurait bloqué les POC à 2 cibles pourtant retenus dans cette roadmap.
- Les règles de densité restent éditoriales : viser 2 cibles/minute en POC et 4–5 sur ~3 min ; le validateur contrôle seulement le nombre déclaré, pas le naturel des paroles.
- Pour les **nouveaux POC d'une minute**, définir `common.max_target_occurrences_per_variant: 2` dans le manifeste : le validateur bloque alors les répétitions exactes d'une cible au-delà de deux occurrences par variante. Ce contrôle est **opt-in** pour ne pas réécrire l'historique ; il ne détecte ni conjugaisons différentes ni répétitions sémantiques, qui restent à juger à la lecture.
- Les packs longs peuvent maintenant déclarer **1 à 5 lignes françaises** avec `french_anchor_count` et utiliser `anchor_line_map` si plusieurs cibles partagent des lignes. Cela n'impose aucune répétition.
- Ce changement **n'approuve aucun texte** et ne déverrouille pas Suno sans le garde-fou d'approbation humaine.

### Prévalidation en cours

- [3 variantes de paroles sans audio](songs/drafts/2026-10-31-lyrics-preflight.md) : A = deux voix, B = deux époques, C = contrôle à deux cibles.
- **Statut : à relire par Vincent**. Aucune des trois variantes n'est validée.
- Les ancrages français risquent encore de ressembler à des traductions ; c'est l'objet du test textuel.
- Vincent a **validé le principe de 2 cibles/minute** et la piste de la reprise naturelle d'une notion dans un autre contexte ; il **n'a pas validé les paroles C**.
- [3 mini-scènes dialoguées D1/D2/D3 réécrites](songs/drafts/2026-10-31-dialogue-mechanisms.md) après feedback : ton plus adulte, elliptique et chantable ; suppression des formulations littérales type « moi aussi » et des images artificielles. D3 reste la piste la plus prometteuse, mais **aucun texte n'est encore validé**.
- **Ne pas utiliser Suno pour ces variantes avant validation explicite des paroles.**
- Garde-fou ajouté : `scripts/check_generation_gate.py` vérifie l'approbation humaine **liée au hash des paroles** ; les exports hors ligne restent marqués en attente si l'approbation manque.

### Expérience active

`songs/experiments/2026-10-31-semantic-reset/`

Conclusion actuelle :
- la variante B est préférable à A uniquement parce que l'effet « bloc de traduction » est moins visible ;
- le vrai problème est en amont : les phrases françaises restent des traductions / paraphrases trop directement empilées ;
- les cibles ont aussi été répétées trop souvent dans une seule minute, ce qui sonne artificiel ;
- ces faiblesses sont détectables **sur les paroles seules**, sans génération audio.

Nouvelle règle de process :
- **ne pas générer sur Suno tant que les paroles n'ont pas passé une revue textuelle humaine de Vincent** pour les nouvelles structures pédagogiques ;
- avant chaque appel Suno, exécuter `python3 scripts/check_generation_gate.py <répertoire-expérience>` ; le résultat doit être APPROVED. Si les paroles ne sont pas encore dans un pack structuré avec manifeste, aucun appel Suno ;
- l'audio sert ensuite à tester musique, voix, rythme, accent et naturel — pas à découvrir un problème évident de rédaction.

## Objectifs immédiats

1. Faire valider à la lecture les nouvelles versions D1/D2/D3, désormais réécrites dans un ton adulte et moins littéral.
2. Réduire fortement la répétition intra-morceau : une cible peut n'apparaître qu'une fois en espagnol si le contexte est clair, avec un ancrage français naturel ailleurs ; la répétition se fait surtout entre plusieurs chansons.
3. **En attente de revue textuelle humaine** : D1/D2/D3 réécrites dans [dialogue-mechanisms](songs/drafts/2026-10-31-dialogue-mechanisms.md). D3 sert de référence de direction ; les anciens textes A/B/C restent historiques. **Aucun texte n'est approuvé pour génération**.
4. Une fois une structure textuelle validée, tester plusieurs traitements musicaux cohérents avec le profil Deezer en gardant les paroles constantes.
5. Utiliser progressivement le budget Suno quotidien uniquement sur des hypothèses déjà valides sur papier.
6. Préparer un chemin de validation V6 complet dès qu'il devient accessible.

## Règle de répétition

- Ne pas forcer 3–4 répétitions d'un même mot cible dans une chanson d'une minute.
- Nouvelle piste validée par Vincent : chercher la répétition **dans des contextes conversationnels naturels**, où deux personnes se répondent, se corrigent, reformulent ou reprennent une idée avec un autre exemple. Trois micro-scènes D1/D2/D3 sont disponibles pour prévalidation.
- Par défaut, viser **1 occurrence espagnole claire par cible** dans le morceau, puis éventuellement une reprise naturelle dans un autre contexte ou par une autre voix.
- Un ancrage français naturel peut apparaître ailleurs dans la chanson sans répéter mécaniquement le mot.
- Une deuxième occurrence espagnole n'est utile que si elle tombe naturellement dans un refrain ou une reprise crédible.
- La vraie répétition pédagogique doit surtout se faire **entre plusieurs chansons espacées**, pas à l'intérieur du même morceau.

## Piste d'écriture à explorer — répétition conversationnelle naturelle

Chercher des scènes où, dans la vraie vie, des gens répètent naturellement un mot ou une idée sans donner l'impression de réciter :

- **Reprise / écho** : « J'ai laissé la ville. » — « Moi, j'ai laissé les clés. »
- **Confirmation** : « Tu veux dire que tu l'as trouvé ? » — « Oui, je l'ai trouvé sous le siège. »
- **Correction** : « Tu regrettes la maison ? » — « Non, surtout les matins là-bas. »
- **Renchérissement** : « J'ai tout laissé derrière moi. » — « Même les photos ? »
- **Parallèle entre deux personnes** : chacun raconte une situation différente avec la même notion.
- **Question / réponse** : la question contient l'idée, la réponse la réemploie avec un nouveau contexte.
- **Malentendu / précision** : un mot revient parce qu'il faut préciser ce qu'on voulait dire.
- **Souvenir partagé** : deux personnes se rappellent le même événement avec des détails différents.
- **Décision commune** : « On laisse ça derrière nous ? » — « Oui, on avance. »
- **Refrain dialogué** : la seconde voix répond au motif de la première sans répéter la phrase exacte.

Objectif : obtenir une répétition qui sert la scène et le dialogue, pas la pédagogie visible.

## Backlog

- améliorer la sélection de vocabulaire et le SRS léger ;
- journal d'écoute / feedback humain structuré ;
- distinguer clairement « candidat préparé », « généré », « écouté », « validé » ;
- historique des crédits Suno par jour et par expérience (précontrôle déterministe `scripts/check_suno_budget.py` implémenté ; maintenir les journaux à jour) ;
- étendre les checks déterministes de paroles / manifestes (garde-fou d'approbation déjà implémenté ; validation des packs étendue à **2–5 cibles**, avec tests 2/1/6 cibles, pour couvrir les POC 1 min et les chansons finales 3 min) ;
- comparer 30–45 s vs 60 s si Suno permet un contrôle réellement utile de la durée ;
- explorer des profils musicaux dérivés des goûts Deezer sans imitation d'artistes.

## Règle de choix d'une tâche au réveil

1. Lire ce fichier.
2. Vérifier les tâches / expériences déjà en cours.
3. Éviter de refaire ce qui attend une revue humaine.
4. Choisir la prochaine action qui réduit le plus une incertitude produit.
5. Préférer scripts/checks déterministes à une analyse GPT lorsqu'ils suffisent.
6. Pour une nouvelle structure de paroles, ne pas appeler Suno avant validation textuelle humaine par Vincent. Pour une structure déjà validée, exécuter **les deux précontrôles** : `check_generation_gate.py` et `check_suno_budget.py` avec le solde réel ; si l'un bloque, ne pas appeler Suno. Sinon faire au maximum un appel sur ce run.
7. Mettre à jour cette roadmap si l'état ou les priorités ont réellement changé.
