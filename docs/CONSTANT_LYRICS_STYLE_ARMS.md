# Protocole papier — trois arrangements à paroles strictement constantes

Statut : **préparation uniquement**, non approuvé, **aucune génération Suno autorisée**. Cette expérience isole l'effet de l'arrangement sur une future chanson complète **déjà approuvée mot pour mot** par Vincent. Ne pas utiliser D1b ni La luz del pasillo V0 avant leur validation explicite.

## Hypothèse discriminante

À paroles, langue, ordre des sections et modèle Suno identiques, un arrangement plus contrasté peut rendre les reprises conversationnelles moins scolaires sans sacrifier l'énergie. Les préférences musicales, l'intelligibilité, les accents et le naturel ne peuvent être évalués **que par Vincent à l'écoute**.

## Variables fixes (pour les trois bras)

- Exactement le même pack de paroles approuvées et son SHA-256, sans retouche, ajout d'introduction ou traduction.
- Même modèle, paramètres disponibles, durée cible, configuration vocale et date de campagne autant que possible.
- Deux voix qui se répondent si le pack les prévoit ; ne jamais demander une identité vocale Suno garantie.
- Aucun nom d'artiste, imitation de voix, référence à une œuvre protégée ni contenu pédagogique explicite.
- Ne pas modifier les mots-cibles, le nombre d'occurrences ni les ancrages FR/ES.
- Ordre des essais randomisé **avant** génération et IDs consignés ; aucune conclusion à partir d'une seule prise, car les sorties sont non déterministes.

## Bras expérimentaux — prompts de style uniquement

**A — organique / retenu (contrôle)**

> Intimate, raw, dark organic duet; close dry voices, sparse acoustic guitar and low cello, subtle room texture, restrained percussion, natural conversational handoffs, short instrumental opening, dynamic tension without sweetness. Preserve supplied lyrics exactly. No instructional spoken intro, no nursery-pop bounce.

**B — pulsation / tension (test énergie)**

> Driving nocturnal alternative electronic duet; tight syncopated low-end pulse, gritty percussion, tense analog textures, controlled build and a strong release, clear vocal foreground, crisp conversational call-and-response, brief intro. Preserve supplied lyrics exactly. No cute or bubbly pop, no instructional narration.

**C — silences / breaks parlés (test respiration)**

> Dark minimal rhythmic duet with sparse percussive guitar, dramatic stops and negative space, short natural spoken-sung exchanges where lyrics already indicate dialogue, a memorable rhythmic motif, raw intimate vocal presence, strong final lift, very short intro. Preserve supplied lyrics exactly. No added spoken words, no instructional intro.

Ces prompts ne garantissent pas que Suno respectera le texte, la durée ou les voix ; les écarts éventuels seront notés par Vincent, pas évalués automatiquement.

## Exécution après autorisation seulement

1. Sélectionner **un seul** texte complet approuvé et vérifier que son hash n'a pas changé ; exécuter le gate de génération de l'expérience.
2. Vérifier le solde réel Suno et exécuter `scripts/check_suno_budget.py --cost 10 --balance <solde>` avant **chaque** appel. Respecter le plafond d'un appel par run ; les trois bras nécessiteront plusieurs runs et éventuellement des jours distincts.
3. Consigner pour chaque bras le prompt exact, les paramètres, la version du modèle, l'ID/URL, les timestamps et le coût réellement débité. Ne pas modifier le pack de paroles entre les bras. Un changement de modèle ou de voix invalide la comparaison contrôlée.
4. Présenter les clips avec des codes neutres (X/Y/Z), dans un ordre masqué, sans annoncer l'hypothèse ; conserver la correspondance dans le journal.
5. Demander à Vincent : préférence globale, énergie, naturel des transitions, prononciation FR/ES, intelligibilité des cibles, adéquation des breaks. Séparer observations et décisions de publication.
6. Si le modèle/solde ou les paramètres changent entre runs, documenter la limitation : comparaison exploratoire, **pas** preuve causale. Ne pas inférer un gagnant sans feedback.

## Critère de fin

Livrable papier terminé lorsque les trois prompts et les variables fixes sont relus. La **validation musicale** n'aura lieu qu'après génération autorisée et feedback humain. Aucun clip n'est approuvé ou ajouté à la playlist par cette PR.
