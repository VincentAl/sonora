# Expérience 01 — placement et densité des ancrages français

**Statut : paroles uniquement, aucun audio Suno généré.**

## Hypothèse

Des phrases françaises **autonomes** permettent de fixer le sens d'un mot espagnol sans casser la chanson. Mais leur **position** et leur **nombre** peuvent modifier la naturalité musicale et la mémorisation.

### Contrastes

- **A vs B (comparaison principale)** : mêmes 10 lignes espagnoles, mêmes 2 lignes françaises, même prompt folk ; seul l'emplacement des phrases françaises change. A regroupe les deux lignes dans un pont ; B les répartit dans deux pauses.
- **A vs C (exploratoire)** : mêmes lignes espagnoles ; C ne conserve qu'une seule phrase française. Ce contraste change le dosage d'ancrage, donc il ne faut pas interpréter ses résultats comme un simple effet de placement.

Les deux phrases françaises sont des images indépendantes, et non des traductions ligne à ligne des phrases espagnoles voisines.

## Cibles

| Espagnol | Sens français | Ancrage dans le morceau |
| --- | --- | --- |
| añorar / añoro | avoir la nostalgie de | « J'ai la nostalgie de nos dimanches sans fin. » |
| sosiego | quiétude, calme intérieur | contexte espagnol ; ancrage à prévoir dans un prochain morceau |
| hallar / hallo | trouver | contexte espagnol ; ancrage à prévoir dans un prochain morceau |
| dejar atrás / dejo atrás | laisser derrière soi | « J'ai laissé derrière moi les rendez-vous manqués. » (A/B) |

Attention : **deux des quatre cibles ne sont pas ancrées explicitement**. Elles doivent être réintroduites plus tard avec un ancrage exact. Les 4 cibles ne sont pas toutes censées être acquises en une minute.

## Protocole proposé

1. Générer **2 prises par variante** dans Suno avec le même style `prompts/folk.md`, si des crédits ont été autorisés. Ne pas inventer d'URL ni de résultats.
2. Écouter les six prises en ordre aléatoire et à volume comparable ; noter séparément chaque prise. Comparer A/B à style et paroles contrôlés ; ne pas surinterpréter les petites différences entre générations stochastiques.
3. Après une écoute, tester sans texte la reconnaissance du sens de `añorar`, `sosiego`, `hallar` et `dejar atrás` ; retester à 24 h si possible.
4. Évaluer de 0 à 5 : intelligibilité FR, intelligibilité ES, naturel musical, transitions trop rapides (5 = problème grave).
5. Conserver les URLs, notes et date dans un futur fichier de résultats ; ne conclure qu'après écoute. Les métadonnées de `manifest.json` sont le point d'entrée du lot.

## Critères de décision

- Préférer A ou B si l'une obtient un meilleur compromis entre intelligibilité FR et naturel musical sur **les deux prises**, sans baisse claire du rappel.
- Si les deux sont médiocres, tester des pauses instrumentales plus longues et une ligne FR par passage.
- Ne pas confondre qualité de la voix générée et effet pédagogique du placement ; ce protocole reste un **test exploratoire**, pas une preuve statistique.

## Prompt à transmettre à Suno

Utiliser `prompts/folk.md` comme style. Copier **uniquement** le texte sous le titre Markdown de la variante comme lyrics ; les marqueurs entre crochets indiquent les sections. Vérifier dans le rendu que les marqueurs ne sont pas chantés.

## Prochain lot

Introduire explicitement **sosiego → quiétude** et **hallar → trouver** dans des phrases françaises naturelles, puis recycler les 4 cibles en espagnol seul.
