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
- Environ 3–4 mots / idées cibles par morceau.
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
- Ces 4 clips sont **en attente de revue humaine**.

### Expérience active

`songs/experiments/2026-10-31-semantic-reset/`

Question à trancher :
- comment intégrer les ancrages français des quatre idées sans transformer la chanson en dictée bilingue ?

Le test actuel compare notamment ancrages regroupés vs répartis.

**Ne pas conclure sur l'audio avant le feedback de Vincent.**

## Objectifs immédiats

1. Attendre / intégrer le feedback humain sur les clips déjà générés.
2. Continuer à préparer des variantes courtes et discriminantes prêtes à générer.
3. Utiliser progressivement le budget Suno quotidien sur des hypothèses distinctes, pas sur des doublons.
4. Réduire les intros longues par les paroles / prompts / structures, sans lancer d'analyse audio automatique.
5. Tester plusieurs traitements musicaux cohérents avec le profil Deezer, tout en gardant les paroles constantes quand l'expérience porte sur le style.
6. Préparer un chemin de validation V6 complet dès qu'il devient accessible.

## Backlog

- améliorer la sélection de vocabulaire et le SRS léger ;
- journal d'écoute / feedback humain structuré ;
- distinguer clairement « candidat préparé », « généré », « écouté », « validé » ;
- historique des crédits Suno par jour et par expérience ;
- automatiser les checks déterministes de paroles / manifestes ;
- comparer 30–45 s vs 60 s si Suno permet un contrôle réellement utile de la durée ;
- explorer des profils musicaux dérivés des goûts Deezer sans imitation d'artistes.

## Règle de choix d'une tâche au réveil

1. Lire ce fichier.
2. Vérifier les tâches / expériences déjà en cours.
3. Éviter de refaire ce qui attend une revue humaine.
4. Choisir la prochaine action qui réduit le plus une incertitude produit.
5. Préférer scripts/checks déterministes à une analyse GPT lorsqu'ils suffisent.
6. Si un appel Suno est utile et que le budget journalier le permet, faire au maximum un appel sur ce run.
7. Mettre à jour cette roadmap si l'état ou les priorités ont réellement changé.
