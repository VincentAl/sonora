# Suno — connexion officielle (vérifiée le 31 octobre 2026)

## Changement important

Suno a lancé **Suno MCP (Beta)**. Contrairement à l'hypothèse initiale « une API tierce et une clé API sont nécessaires », Suno documente maintenant une connexion **officielle** à ChatGPT, via un serveur MCP avec authentification de l'utilisateur. Elle ne nécessite **pas de clé API**.

- Guide officiel : https://help.suno.com/en/articles/14551425 (mis à jour le 28 octobre 2026)
- FAQ officielle : https://help.suno.com/en/articles/14486145 (mise à jour le 28 octobre 2026)
- Page officielle : https://suno.com/mcp
- URL MCP officielle : `https://api.suno.com/mcp`

## Activation dans ChatGPT

1. Dans **Plugins**, choisir **Add → Add custom MCP server**.
2. Nommer le plugin **Suno** et entrer `https://api.suno.com/mcp`.
3. Choisir **Create as a plugin**, puis **Connect Suno**.
4. Se connecter au compte Suno et autoriser l'accès.

Le compte Suno est requis ; **les générations consomment les crédits Suno du plan**, y compris sur le plan gratuit. Les chansons générées sont sauvegardées dans la bibliothèque Suno.

## État dans l'environnement de travail de ce run

Aucun outil Suno connecté n'est exposé dans cet environnement. Aucun audio n'a été généré, aucun crédit consommé. Ne pas inventer de lien Suno.

**Important :** même si Suno est connecté dans une conversation ChatGPT, sa disponibilité dans les exécutions autonomes doit être vérifiée explicitement. Ne pas supposer qu'une authentification interactive rend le connecteur disponible dans tous les contextes. Une fois le plugin disponible, vérifier la liste des outils et les droits avant de lancer des générations.

## Politique d'autonomie

- La préparation des paroles, prompts, manifestes et tests peut avancer sans compte Suno.
- **Ne pas dépenser de crédits Suno** sans budget/autorisation de génération établi.
- Ne pas utiliser d'API Suno non officielle ou de cookies de session détournés.
- Si la connexion officielle est indisponible dans l'automatisation, consigner ce blocage et continuer les tests hors audio.

## Critère de déblocage

Un outil Suno effectivement disponible, authentifié, avec autorisation explicite d'utiliser des crédits (quantité ou plafond), puis un premier lot limité à 2 prises par variante.
