# Lab 1 Reflection - Log Analyzer

## Classification du Workflow

### Position sur le Spectre

**Mon workflow se situe entre "Vibe Coding" et "Structured"**

### Réponses aux 5 Questions

#### 1. Combien de la sortie avez-vous réellement lu ?

**Réponse : ~80%**

- J'ai lu et compris la structure globale du code généré
- J'ai revu les fonctions principales pour vérifier la logique
- J'ai testé manuellement le prototype avec le fichier sample.log
- J'ai vérifié les exports JSON et CSV
- Cependant, je n'ai pas examiné chaque ligne de code en détail

**Justification** : Le code était relativement simple et bien structuré. J'ai fait confiance à l'agent pour les détails d'implémentation tout en vérifiant la logique métier.

#### 2. Y a-t-il des tests ou vérifications que le travail doit passer ?

**Réponse : Tests manuels limités**

- ✅ Test manuel avec sample.log
- ✅ Vérification des exports JSON et CSV
- ❌ Pas de tests unitaires automatisés
- ❌ Pas de tests d'intégration
- ❌ Pas de validation formelle des résultats

**Justification** : Pour un prototype rapide, les tests manuels suffisaient. En production, il faudrait ajouter des tests unitaires pour chaque méthode et des tests d'intégration pour le flux complet.

#### 3. Qui a décidé de l'étape suivante — vous ou l'agent ?

**Réponse : Mixte (60% agent / 40% moi)**

- **Agent** : Structure du code, choix des bibliothèques, implémentation des fonctions
- **Moi** : Définition des fonctionnalités, validation des résultats, corrections de bugs

**Justification** : J'ai donné un prompt initial clair ("crée un analyseur de logs"), puis l'a laissé guider l'implémentation. J'ai intervenu pour corriger l'erreur de syntaxe et valider les fonctionnalités.

#### 4. Que se passe-t-il si l'IA se trompe — un garde-fou, ou ça part en production ?

**Réponse : Garde-fou manuel (revue de code)**

- ✅ Revue manuelle du code avant utilisation
- ✅ Test avec un fichier d'exemple
- ❌ Pas de tests automatisés de garde-fou
- ❌ Pas de validation automatique des sorties

**Justification** : Dans ce contexte de lab, la revue manuelle suffit. Pour un environnement de production, il faudrait :
- Tests unitaires
- Tests d'intégration
- CI/CD avec validation automatique
- Revue de code par pairs

#### 5. Quoi se casse si ça échoue, et comment récupérez-vous ?

**Réponse : Impact limité, récupération facile**

**Ce qui se casse :**
- L'analyse de logs ne fonctionne pas
- Rapports incorrects ou incomplets
- Exports corrompus

**Comment récupérer :**
- Revenir à la version précédente (Git)
- Corriger manuellement le code
- Utiliser un autre outil d'analyse de logs
- Le prototype n'a pas d'impact sur des systèmes en production

**Justification** : Comme c'est un prototype isolé, l'impact est minimal. La récupération se fait par correction manuelle ou rollback Git.

## Analyse du Workflow

### Forces

1. **Rapidité** : Prototype fonctionnel en quelques minutes
2. **Flexibilité** : Facile à modifier et étendre
3. **Simplicité** : Code clair et compréhensible
4. **Fonctionnel** : Répond aux besoins initiaux

### Faiblesses

1. **Manque de tests** : Pas de tests automatisés
2. **Dépendance à l'IA** : Compréhension partielle du code
3. **Pas de documentation** : Commentaires limités
4. **Garde-fous insuffisants** : Validation manuelle seulement

### Améliorations pour Passer à "Structured"

1. **Ajouter des tests unitaires** : pytest pour chaque fonction
2. **Définir des critères d'acceptation** : Spécifications claires
3. **Documentation** : Docstrings et README détaillé
4. **CI/CD** : Tests automatiques à chaque commit
5. **Revues de code** : Processus formel de revue

### Améliorations pour Passer à "Agentic"

1. **Agent autonome** : Capacité de s'auto-corriger
2. **Tests automatiques** : Validation continue
3. **Garde-fous** : Vérifications automatiques de sécurité
4. **Récupération** : Stratégies de rollback automatiques
5. **Monitoring** : Surveillance en temps réel

## Conclusion

Ce lab m'a permis de ressentir le décalage entre l'écriture de syntaxe et l'expression d'intention. Mon workflow actuel est plus proche du "Vibe Coding" avec quelques éléments "Structured". Pour atteindre un niveau "Agentic" fiable, je dois :

1. Investir dans les tests et la validation
2. Structurer mes prompts et mes processus
3. Mettre en place des garde-fous automatiques
4. Documenter clairement les attentes et les résultats

Le prototype fonctionne et répond aux besoins, mais n'est pas prêt pour un environnement de production sans améliorations significatives.
