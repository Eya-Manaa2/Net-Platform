# Plateforme de Traitement de Données Télécom en Temps Réel

## Architecture

```text
        Générateur de données réseau
                   │
                   ▼
              Apache Kafka
                   │
                   ▼
          Application Java
        Validation / Traitement
                   │
          ┌────────┴────────┐
          ▼                 ▼
   Données temps réel   Données historiques
          │                 │
          ▼                 ▼
   Elasticsearch       Spark / PySpark
          │                 │
          ▼                 ▼
       Kibana          KPIs / Analyse
```

## Structure du Projet

```
projet/
├── docker/                    # Infrastructure Docker
│   ├── docker-compose.yml     # Kafka, Elasticsearch, Kibana
│   └── kafka/                 # Configuration Kafka
├── data-generator/            # Générateur Python
│   ├── generator.py          # Générateur d'événements
│   ├── requirements.txt       # Dépendances Python
│   └── config.py             # Configuration
├── java-processor/            # Application Java
│   ├── src/main/java/
│   │   └── com/telecom/
│   │       ├── processor/    # Traitement temps réel
│   │       ├── model/        # Modèles de données
│   │       └── kafka/        # Consumer/Producer Kafka
│   ├── pom.xml               # Maven configuration
│   └── config/               # Configuration
├── spark-batch/               # Traitement batch
│   ├── batch_processor.py    # Script PySpark
│   ├── requirements.txt      # Dépendances
│   └── config.py             # Configuration
├── kibana/                   # Dashboards Kibana
│   └── dashboards/           # Export JSON dashboards
├── performance/              # Tests de performance
│   ├── benchmarks.py        # Scripts de benchmark
│   └── results/             # Résultats
└── scripts/                  # Scripts de déploiement
    ├── start.sh             # Démarrage infrastructure
    └── stop.sh              # Arrêt infrastructure
```

## Technologies

- **Java 17+** - Traitement temps réel
- **Python 3.9+** - Générateur et batch
- **Apache Kafka** - Streaming de données
- **Apache Spark/PySpark** - Traitement batch
- **Elasticsearch** - Stockage et recherche
- **Kibana** - Visualisation
- **Docker & Docker Compose** - Infrastructure

## Données Télécom

Chaque événement réseau contient :

- `cell_id` - Identifiant de cellule (ex: "CELL_001")
- `timestamp` - Horodatage ISO 8601
- `technology` - Technologie (4G/5G)
- `throughput` - Débit en Mbps
- `latency` - Latence en ms
- `packet_loss` - Taux de perte de paquets (%)
- `signal_strength` - Puissance du signal (dBm)
- `connected_users` - Nombre d'utilisateurs connectés

## Installation

### Prérequis

- Docker et Docker Compose
- Java 17+
- Python 3.9+
- Maven 3.8+

### Démarrage Infrastructure

```bash
# Démarrer Kafka, Elasticsearch, Kibana
cd docker
docker-compose up -d

# Vérifier les services
docker-compose ps
```

### Générateur de Données

```bash
cd data-generator
pip install -r requirements.txt
python generator.py
```

### Application Java

```bash
cd java-processor
mvn clean package
java -jar target/telecom-processor-1.0.jar
```

### Traitement Batch Spark

```bash
cd spark-batch
pip install -r requirements.txt
spark-submit batch_processor.py
```

## Fonctionnalités

### 1. Génération et Ingestion
- Générateur Python produisant des événements réseau réalistes
- Publication dans Kafka topic `telecom-events`

### 2. Traitement Temps Réel (Java)
- Validation des données
- Filtrage des événements invalides
- Transformation et enrichissement
- Calcul de statistiques en temps réel
- Détection d'anomalies

### 3. Traitement Batch (Spark/PySpark)
- Analyse des données historiques
- Calcul des KPIs :
  - Débit moyen par cellule
  - Latence moyenne
  - Taux moyen de perte de paquets
  - Nombre d'incidents
  - Évolution de la qualité
  - Cellules dégradées

### 4. Visualisation (Kibana)
- Tableau de bord des indicateurs principaux
- Alertes sur anomalies détectées
- Historique des performances

### 5. Optimisation
- Mesures de performance (débit, latence, CPU, mémoire)
- Stratégies d'optimisation :
  - Traitement par lots
  - Parallélisation
  - Partitionnement Kafka
  - Filtrage en amont
- Comparaison avant/après optimisation

## Métriques de Performance

- **Débit de traitement** : événements/seconde
- **Latence de traitement** : temps de bout en bout
- **Utilisation CPU/Mémoire** : ressources consommées
- **Temps de traitement batch** : durée des jobs Spark

## Développement

### Branches Git

- `main` - Version stable
- `develop` - Développement en cours
- `feature/*` - Nouvelles fonctionnalités
- `optimization/*` - Optimisations de performance

### Tests

```bash
# Tests Java
cd java-processor
mvn test

# Tests Python
cd data-generator
pytest tests/

# Tests Spark
cd spark-batch
pytest tests/
```

## Auteurs

Projet PFE - Télécom Data Processing Platform

## Licence

MIT License
