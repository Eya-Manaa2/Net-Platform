# Lab 1 - First Contact

## Objectif

Vibe-code un petit prototype à partir du langage naturel en utilisant un agent de codage, puis localise-le sur le spectre (vibe → structured → agentic).

## Livrables

1. **Prototype fonctionnel** dans un dépôt Git
2. **REFLECTION.md** - Classification du workflow avec la grille à 5 questions

## La Grille d'Évaluation (5 Questions)

1. **Combien de la sortie avez-vous réellement lu ?**
   - Avez-vous revu tout le code généré ?
   - Avez-vous testé chaque fonctionnalité ?
   - Ou avez-vous fait confiance à l'agent aveuglément ?

2. **Y a-t-il des tests ou vérifications que le travail doit passer ?**
   - Tests unitaires ?
   - Tests d'intégration ?
   - Vérifications manuelles ?
   - Critères d'acceptation définis ?

3. **Qui a décidé de l'étape suivante — vous ou l'agent ?**
   - Qui a dirigé la conversation ?
   - Qui a déterminé la portée ?
   - Qui a choisi les technologies ?

4. **Que se passe-t-il si l'IA se trompe — un garde-fou, ou ça part en production ?**
   - Y a-t-il des revues de code ?
   - Y a-t-il des tests automatiques ?
   - Y a-t-il des vérifications de sécurité ?

5. **Quoi se casse si ça échoue, et comment récupérez-vous ?**
   - Impact sur les utilisateurs ?
   - Données perdues ?
   - Plan de rollback ?
   - Stratégie de récupération ?

## Le Spectre du Workflow

```
Vibe Coding → Structured → Agentic
```

- **Vibe Coding** : "Fais-moi un truc qui fait X" → Code généré, peu de revue
- **Structured** : Prompts structurés, tests définis, revue systématique
- **Agentic** : Agent autonome avec garde-fous, tests, et capacité de récupération

## Prototype à Construire

Pour ce lab, nous allons construire un **outil d'analyse de logs simples** en Python :

**Fonctionnalités :**
- Lire des fichiers de logs
- Parser les lignes de logs
- Extraire des métriques (erreurs, avertissements, temps)
- Générer un rapport
- Exporter en JSON/CSV

## Instructions

1. Utilisez un agent de codage (Codex, Claude Code, ou autre)
2. Construisez le prototype en mode "vibe coding"
3. Testez le prototype
4. Écrivez votre réflexion dans REFLECTION.md
5. Classez votre workflow sur le spectre

## Ressources

- Agent Skills standard: https://github.com/agentskills/agentskills
- AGENTS.md standard: https://agents.md/
- Codex CLI: https://developers.openai.com/codex/cli
