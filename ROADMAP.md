# Sonora — Roadmap autonome

> Source de vérité pour les priorités courantes de Sonora.
>
> Chaque run autonome doit lire ce fichier **avant de choisir son travail**.
> Le prompt de l'automatisation définit le harnais stable ; ce fichier contient les objectifs, priorités et tâches mouvantes.
> Les discussions avec Vincent peuvent modifier cette roadmap à tout moment.

## Vision

Créer des chansons qu'on peut écouter normalement en travaillant, qui enseignent passivement du vocabulaire espagnol à un francophone.

La musique est le vecteur. L'objectif produit reste l'apprentissage.

## Trajectoire produit — validée dans la discussion du 1 novembre 2026

Sonora doit produire **de vraies chansons complètes**, pas rester au stade de POC de quatre lignes. Le but à terme est **une chanson nouvelle par semaine**, ajoutée à une playlist/bibliothèque où Vincent peut écouter, aimer, rejeter et conserver les titres, pour apprendre progressivement du vocabulaire.

### Vocabulaire de conception

- **Mécanisme pédagogique** : façon naturelle d'introduire et de réactiver une notion dans une chanson (écho conversationnel, confirmation, correction, souvenir partagé, question-réponse, etc.). C'est le nom de travail pour ce que nous appelions « scénarios ».
- **Scénario narratif** : situation et personnages qui rendent le mécanisme crédible (ex. deux anciens amoureux se répondent).
- **Identité musicale** : style, arrangement, interprète/voix. Ces dimensions doivent pouvoir être testées séparément.
- **Bestiaire** : catalogue de mécanismes, scénarios et combinaisons testées, avec statut et feedback humain.

### Étapes et critères de passage

1. **Cataloguer les mécanismes** : documenter D1 comme premier candidat prometteur et explorer d'autres formes de reprise naturelle. Distinguer mécanisme et histoire. Le feedback sur D1 ne valide pas automatiquement chaque ancrage lexical.
2. **Écrire des chansons complètes** : produire un premier texte de ~2–3 minutes avec ~4–5 notions, structure musicale cohérente, ancrages sémantiques vérifiables et répétitions non forcées. Revue humaine du texte avant Suno. D1b reste un brouillon court servant de référence, **pas** un feu vert pour le générer.
3. **Valider musicalement** : générer des versions de chansons complètes, recueillir le feedback d'écoute de Vincent, comparer des mécanismes et scénarios, documenter les réussites/échecs.
4. **Explorer styles et voix** : tests contrôlés de styles à paroles constantes ; étudier la faisabilité de chanteuses/chanteurs récurrents sur Suno, créer une première identité vocale si possible, puis plusieurs. Ne pas présumer que Suno garantit une voix identique.
5. **Bibliothèque et playlist** : choisir une intégration réellement disponible, gérer ajout, écoute, like/dislike, conservation et lien avec les notions enseignées. Ne pas présumer qu'une playlist externe est automatisable avant vérification.
6. **Cadence hebdomadaire** : automatiser la préparation et la livraison d'environ une chanson par semaine, avec validation humaine adaptée, budget maîtrisé et suivi des mots/reprises entre chansons.

### Prochaine priorité

**Catalogue initial rédigé** : [bestiaire de 7 mécanismes](docs/MECHANISM_BESTIARY.md), dont M01 (écho conversationnel) avec premier feedback positif, les autres encore hypothétiques. **Première chanson complète rédigée** : [La luz del pasillo V0](songs/drafts/2026-11-01-la-luz-del-pasillo-full.md), 4 cibles, ~2–3 min visées, **en attente de revue textuelle humaine**. Ne pas générer ce texte ni D1b sans approbation explicite. Prévalidation structurelle disponible via `scripts/audit_full_draft.py` ; [protocole de comparaison à paroles constantes](docs/FULL_SONG_COMPARISON_PROTOCOL.md) préparé. Chemin de promotion déterministe prêt via `scripts/prepare_full_song_pack.py` et le modèle `songs/drafts/2026-11-01-la-luz-del-pasillo-pack-template.json`. Le script extrait uniquement les paroles, valide la structure, fige le SHA-256 et produit un pack **toujours bloqué** jusqu'à approbation explicite des paroles exactes par Vincent. Playlist privée créée et faisabilité des voix documentée ci-dessous. Prochain travail autonome : préparer le journal de feedback hebdomadaire minimal, sans génération.

## Intégration Suno — vérifiée le 2 novembre 2026

### Playlist hebdomadaire

- Playlist privée créée et relue via Suno MCP : **[Sonora — Hebdo](https://suno.com/playlist/152d06fb-bd76-4d7c-9eb3-b11bd3c90bde)**, ID `152d06fb-bd76-4d7c-9eb3-b11bd3c90bde`.
- **0 titre** actuellement. Ne pas y ajouter D1 ni d'autres tests tant que les paroles et la qualité n'ont pas été validées humainement pour la diffusion hebdomadaire.
- Suno MCP permet de lister, créer, ajouter et retirer des clips de playlists. Pour un titre validé, l'ajouter par `clip_id` à cette playlist, vérifier le résultat (dont les éventuels `failed`), puis enregistrer l'ID du clip et l'état de publication dans le repo.
- Suno MCP propose `audio_like` / `audio_unlike` et `library_liked`. **Pas d'action explicite de dislike** : ne pas confondre « unlike » avec un rejet. Le statut `rejected` devra être consigné dans un journal Sonora séparé, sur feedback explicite de Vincent.
- La playlist est un canal d'écoute, pas à elle seule une base de suivi pédagogique ou un système de SRS. La sélection des notions et les retours restent à tracer côté Sonora.

### Voix récurrentes

- `voices_list(collection="own")` retourne **0 voix** au 2 novembre. Aucune voix récurrente disponible actuellement.
- Suno MCP propose `voices_start`, qui ouvre un parcours Suno de création **et vérification par l'utilisateur**. Après disponibilité d'une voix, `voices_list` donne un `voice_id` réutilisable dans `audio_create` ou `audio_covers_create`.
- Une identité vocale récurrente est donc techniquement **testable**, mais pas encore créée ni validée. Ne pas lancer ce parcours sans intérêt confirmé au moment du test ; ne jamais présenter un `voice_id` comme garantissant une interprétation identique à chaque génération.
- Protocole futur : même texte, même style, comparer voix par défaut vs voix enregistrée, puis évaluer exclusivement à l'écoute de Vincent.

### Quota observé

- Lecture `account_usage` le 2 novembre : plan **Free**, `allowed_models=["v6-mini"]`, `credits_remaining=50`, `monthly_limit=50`, `monthly_usage=0`, `renews_on=null`.
- C'est une **observation ponctuelle**, pas la preuve d'un renouvellement quotidien. Le contrôle de budget existant reste obligatoire avant toute génération ; aucune dépense sur ce run.

### Prochaine action autonome

**Journal hebdomadaire minimal prêt** : [format et procédure](docs/WEEKLY_FEEDBACK_JOURNAL.md), [données](data/weekly_feedback.json), validateur déterministe `scripts/validate_weekly_feedback.py` et tests. Il démarre vide : D1 reste un test, pas un titre diffusé. Ne pas confondre like, approbation audio, approbation pédagogique et publication.

**Contrôle playlist/journal prêt** : `scripts/check_weekly_playlist.py` compare une capture Suno MCP fraîche, complète et paginée avec `data/weekly_feedback.json`, sans rien modifier ; six tests couvrent les écarts et les refus. Voir [procédure](docs/WEEKLY_FEEDBACK_JOURNAL.md). La playlist réelle a été relue le 2 novembre : **0 titre**, cohérent avec le journal vide. Aucun titre ajouté, aucun feedback inventé.

**Sélection de vocabulaire V0 prête** : [registre](data/vocabulary.json), [planificateur déterministe](scripts/plan_vocabulary.py), [documentation](docs/VOCABULARY_PLANNING.md) et 8 tests. Les 4 notions de `La luz del pasillo` sont réservées comme brouillon, jamais considérées apprises ; 4 nouvelles notions sont candidates, non validées. Reprise éventuelle après 14 jours depuis une **publication vérifiée**, pas depuis une génération. Paramètres exploratoires, sans mesure de mémorisation. **Prochain travail autonome** : préparer une autre scène/mécanisme sur papier à partir de candidats distincts, sans générer ni dupliquer la chanson en revue. `La luz del pasillo` attend toujours la validation textuelle.


## Règles produit stables

- Une chanson doit sonner comme une vraie chanson, jamais comme un exercice.
- Pour les tests d'une minute : viser **2 mots / idées cibles**. Sur une chanson finale d'environ 3 minutes, viser environ **4–5 notions** avec répétitions naturelles.
- Chaque cible doit être compréhensible en espagnol dans le contexte **et la même idée sémantique doit réapparaître clairement en français**, dans une formulation ou un contexte différent. Même sens, pas forcément même phrase.
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

## État actuel — 1 novembre 2026

### Suno

- MCP connecté au compte `vincent_alfaro`.
- Modèle exposé via MCP : `v6-mini`.
- Premier smoke test réel effectué.
- 4 clips générés pour 20 crédits.
- 80 crédits restaient après le test.
- Les 4 clips du premier smoke test ont reçu un premier feedback humain sur la structure bilingue.
- Le 1 novembre, D1 a généré 2 prises v6-mini (~55 s). Vincent a donné un **premier retour positif** (« ça marche ») et préfère la **prise 1** ; ce n'est pas une validation de la prononciation, de la mémorisation ni de la précision de chaque ancrage.
- Le solde affichait encore 50 crédits juste après génération, mais une vérification différée a confirmé **40 crédits restants et 10 consommés**. Le journal D1 a été corrigé : ne jamais traiter une absence de décrément immédiat comme une génération gratuite.

### Compatibilité du pipeline

- Le validateur `scripts/validate_experiment.py` accepte désormais **2–5 cibles** : auparavant il imposait 3–4 et aurait bloqué les POC à 2 cibles pourtant retenus dans cette roadmap.
- Les règles de densité restent éditoriales : viser 2 cibles/minute en POC et 4–5 sur ~3 min ; le validateur contrôle seulement le nombre déclaré, pas le naturel des paroles.
- Pour les **nouveaux POC d'une minute**, définir `common.max_target_occurrences_per_variant: 2` dans le manifeste : le validateur bloque alors les répétitions exactes d'une cible au-delà de deux occurrences par variante. Ce contrôle est **opt-in** pour ne pas réécrire l'historique ; il ne détecte ni conjugaisons différentes ni répétitions sémantiques, qui restent à juger à la lecture.
- Les packs longs peuvent maintenant déclarer **1 à 40 lignes françaises** avec `french_anchor_count` et utiliser `anchor_line_map` si plusieurs cibles partagent des lignes. Cela n'impose aucune répétition.
- Ce changement **n'approuve aucun texte** et ne déverrouille pas Suno sans le garde-fou d'approbation humaine.

### Prévalidation en cours

- [3 variantes de paroles sans audio](songs/drafts/2026-10-31-lyrics-preflight.md) : A = deux voix, B = deux époques, C = contrôle à deux cibles.
- **Statut : à relire par Vincent**. Aucune des trois variantes n'est validée.
- Les ancrages français risquent encore de ressembler à des traductions ; c'est l'objet du test textuel.
- Vincent a **validé le principe de 2 cibles/minute** et la piste de la reprise naturelle d'une notion dans un autre contexte ; il **n'a pas validé les paroles C**.
- [D1/D2/D3 — révision sémantique](songs/drafts/2026-10-31-dialogue-mechanisms.md) : Vincent a jugé les trois pistes prometteuses puis a choisi **D1** pour le premier test audio.
- D1 a été promue dans [l'expérience exécutable](songs/experiments/2026-11-01-d1-dialogue/) et explicitement approuvée par Vincent.
- Un appel Suno v6-mini a généré **2 prises D1** le 1 novembre 2026. **Retour initial reçu : prise 1 préférée, mécanisme jugé prometteur**. Ne pas régénérer D1 sans nouvelle hypothèse explicite.
- Garde-fou ajouté : `scripts/check_generation_gate.py` vérifie l'approbation humaine **liée au hash des paroles** ; les exports hors ligne restent marqués en attente si l'approbation manque.

### Expérience active

`songs/experiments/2026-11-01-d1-dialogue/` (2 prises générées, [premier feedback humain](songs/experiments/2026-11-01-d1-dialogue/human-feedback.md) reçu ; revue pédagogique/phonétique complète non faite).

### Expérience historique rejetée

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

1. D1 a reçu un premier feedback humain positif : le mécanisme « marche » et Vincent préfère **la prise 1**. Ne pas régénérer D1 sans nouvelle hypothèse. Les 2 liens Suno sont dans le manifeste de l'expérience ; ne pas lancer une autre génération sur ce texte pendant l'attente.
2. **Incertitude pédagogique à résoudre** : le couplage `dejar atrás` de D1 était imprécis. [D1b](songs/drafts/2026-11-01-d1b-semantic-preflight.md) et la [chanson complète V0](songs/drafts/2026-11-01-la-luz-del-pasillo-full.md) proposent une correction **encore à valider humainement** ; ne pas générer avant approbation explicite.
3. Si D1 fonctionne comme mécanisme, garder D2/D3 pour de futurs morceaux plutôt que chercher un vainqueur unique.
4. Si les paroles sont validées mais le style ne l'est pas, tester ensuite plusieurs traitements musicaux avec **exactement les mêmes paroles D1**.
5. Continuer à utiliser le budget Suno uniquement sur des hypothèses déjà valides sur papier.
6. Préparer un chemin de validation V6 complet dès qu'il devient accessible.

## Règle de couplage sémantique

Pour chaque cible, avant toute génération, il faut pouvoir écrire :
- sens cible X ;
- contexte espagnol A ;
- contexte français B ;
- et vérifier que **X est réellement le même dans A et B**.

Le français peut changer l'objet, le souvenir, le personnage ou la formulation, mais pas le **sens lexical précis** appris. Par exemple `dejar atrás` (« laisser derrière soi / dépasser un passé ») ne se réduit pas automatiquement à `dejar` (« laisser des clés quelque part »). Si la paire ne conserve que le sens plus large de `dejar`, revoir la cible ou l'ancrage.

Une simple continuité d'ambiance, de narration **ou de famille lexicale** ne suffit pas. Voir [règles pédagogiques](docs/PEDAGOGY_RULES.md).

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

## File de travail autonome — priorité et anti-attente (proposition du 4 novembre 2026)

**Règle de sélection :** à chaque run, prendre la première tâche **actionnable** de cette file, pas simplement la première tâche numérotée. Si une tâche attend la revue de Vincent, un accès, un quota ou une PR concurrente, la marquer `blocked` avec la raison et **passer immédiatement à la suivante dans le même run**. Une tâche bloquée n'immobilise jamais toute la routine. Ne pas fabriquer des micro-correctifs pour remplir un run. Ne recontrôler une PR en attente que si son état a changé ou si cela débloque réellement une action. Une vérification CI seule ne constitue pas un livrable produit.

**Livrable attendu :** pour une tâche choisie, viser un résultat concret et vérifiable (texte à relire, script + tests, protocole exploitable, jeu de données ou décision documentée), en une PR par livrable et un commit logique. Si aucune tâche n'est faisable, signaler précisément pourquoi, sans inventer de travail.

| Ordre | Chantier | Résultat concret / critère de fin | Dépendance |
| --- | --- | --- | --- |
| 1 | M08 — finalisation | Paroles cohérentes avec cibles du diagnostic, ancrages français exacts, sections chantées suffisamment musicales ; soumettre **un seul texte figé** à validation | PR #5 ; **bloqué si déjà soumis et sans nouveau retour** |
| 2 | Diagnostic vocabulaire | Registre de 30 connus / 30 à confirmer et tests, puis sélection effective par le planificateur sans supposer qu'un non-coché est inconnu | PR #6 ; intégration au planificateur dépend de PR #4 ; ne pas dupliquer |
| 3 | Nouvelle chanson M02 / autre mécanisme | Une chanson complète autonome, scène crédible, 4–5 cibles pertinentes, grille des sens FR/ES, sans génération | Réutiliser PR #3 si même livrable ; **passer si en revue** |
| 4 | Nouvelle expérience de mécanisme | Préparer une chanson/variante distincte qui teste un mécanisme non couvert (confirmation, correction, parallèle), avec hypothèse discriminante et paroles à valider | Indépendant de M08 ; PR dédiée ; éviter de multiplier des brouillons identiques |
| 5 | Audit déterministe des chansons | Script de prévalidation qui signale cible déjà connue/non évaluée, cible sans ancrage et incohérences **structurelles vérifiables** ; tests sur exemples positifs/négatifs | Réutiliser les contrôles existants ; ne pas prétendre automatiser la qualité narrative |
| 6 | Parcours approbation → pack figé | Vérifier bout en bout sur un fixture que hash des paroles, approbation humaine et gate empêchent toute génération après modification | Aucun appel Suno ; tests déterministes |
| 7 | Expériences à paroles constantes | Préparer 2–3 prompts musicaux réellement contrastés pour un **même texte futur approuvé**, avec critères de comparaison soumis à Vincent | Pas de génération avant validation du texte |
| 8 | Journal des retours d'écoute | Formaliser un formulaire/JSON minimal pour qualité musicale, prononciation, naturel, vocabulaire retenu et statut accepté/rejeté ; test de validation | Ne pas inventer d'avis humains |
| 9 | Bibliothèque hebdomadaire | Définir le flux de promotion d'un clip validé vers playlist + journal, et tester la cohérence avec fixtures | Ne pas publier de morceau non validé |
| 10 | Suivi des crédits et cadence | Consolider les journaux de génération et une synthèse quotidienne déterministe, sans IA audio ; différencier budget souhaité et solde Suno réel | Pas d'achat ni génération fictive |
| 11 | Sélection espacée des notions | Proposition de reprise entre chansons à partir d'expositions **publiées**, jamais de simple génération, avec tests | Après stabilisation du planificateur |
| 12 | Pipeline hebdomadaire | Définir une machine d'états explicite : brouillon → revue texte → texte figé → génération → revue audio → playlist, avec reprises sur échec | Réutiliser les gates et journaux existants |

**Entretien de la file :** quand un livrable est terminé, noter sa PR/commit et remplacer son entrée par la prochaine incertitude concrète. Garder en permanence **au moins 5 tâches indépendantes actionnables** (écriture, pédagogie, outillage, bibliothèque), sans compter les tâches déjà en revue. Ne pas ouvrir de nouvelles PR pour des tâches déjà couvertes par #2–#6. Mettre à jour cette file lorsque la priorité produit change, sur branche/PR uniquement.

**Mesure des runs :** dans le bilan de 21 h, indiquer les runs avec livrable réel, les runs bloqués et la cause, et le nombre de PR en attente. Un run de simple vérification n'est pas compté productif.

## Backlog

- améliorer la sélection de vocabulaire et le SRS léger ;
- journal d'écoute / feedback humain structuré ;
- distinguer clairement « candidat préparé », « généré », « écouté », « validé » ;
- historique des crédits Suno par jour et par expérience (précontrôle déterministe `scripts/check_suno_budget.py` implémenté ; maintenir les journaux à jour) ;
- étendre les checks déterministes de paroles / manifestes (garde-fou d'approbation déjà implémenté ; validation des packs étendue à **2–5 cibles**, avec tests 2/1/6 cibles, pour couvrir les POC 1 min et les chansons finales 3 min) ;
- comparer 30–45 s vs 60 s si Suno permet un contrôle réellement utile de la durée ;
- explorer des profils musicaux dérivés des goûts Deezer sans imitation d'artistes.

## Hygiène Git

- Un changement logique = **un commit** autant que possible.
- Ne pas créer un commit par fichier pour un même pack/expérience.
- Préparer les blobs/arbre puis créer un commit groupé quand plusieurs fichiers sont liés.
- Éviter les chaînes de commits « fix précédent commit » sur `main` ; valider localement/déterministement avant de pousser.
- Pendant un run, viser **1 commit final**, exceptionnellement 2 si les changements sont réellement indépendants.
- Ne pas réécrire l'historique déjà poussé uniquement pour nettoyer l'esthétique.

## Règle de choix d'une tâche au réveil

1. Lire ce fichier.
2. Vérifier les tâches / expériences déjà en cours.
3. Éviter de refaire ce qui attend une revue humaine.
4. Choisir la prochaine action qui réduit le plus une incertitude produit.
5. Préférer scripts/checks déterministes à une analyse GPT lorsqu'ils suffisent.
6. Pour une nouvelle structure de paroles, ne pas appeler Suno avant validation textuelle humaine par Vincent. Pour une structure déjà validée, exécuter **les deux précontrôles** : `check_generation_gate.py` et `check_suno_budget.py` avec le solde réel ; si l'un bloque, ne pas appeler Suno. Sinon faire au maximum un appel sur ce run.
7. Mettre à jour cette roadmap si l'état ou les priorités ont réellement changé.
