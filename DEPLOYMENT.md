# Guide de Déploiement

## Prérequis

### Logiciels Requis
- **Docker Desktop** 20.10+ (Windows/Mac) ou Docker Engine 20.10+ (Linux)
- **Java** 17+ (OpenJDK ou Oracle JDK)
- **Maven** 3.8+
- **Python** 3.9+
- **Git** (pour le versionnement)

### Vérification des Prérequis
```bash
# Vérifier Docker
docker --version
docker-compose --version

# Vérifier Java
java -version

# Vérifier Maven
mvn -version

# Vérifier Python
python --version
```

## Installation

### 1. Cloner le Repository
```bash
git clone <repository-url>
cd projet
```

### 2. Démarrer l'Infrastructure
```bash
# Windows
scripts\start.bat

# Linux/Mac
chmod +x scripts/start.sh
./scripts/start.sh
```

Cela démarre :
- **Zookeeper** (port 2181)
- **Kafka** (ports 9092, 29092)
- **Elasticsearch** (ports 9200, 9300)
- **Kibana** (port 5601)

### 3. Vérifier les Services
```bash
cd docker
docker-compose ps
```

Tous les services doivent afficher "Up" ou "healthy".

## Configuration

### Variables d'Environnement

Créez un fichier `.env` à la racine du projet :

```bash
# Kafka
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAKA_TOPIC=telecom-events

# Elasticsearch
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200
ELASTICSEARCH_INDEX=telecom-events

# Application
EVENTS_PER_SECOND=10
BATCH_INTERVAL_MINUTES=60
```

### Configuration Kafka

Pour modifier le nombre de partitions :
```bash
docker exec kafka kafka-topics --alter --bootstrap-server localhost:29092 \
  --topic telecom-events --partitions 6
```

### Configuration Elasticsearch

Pour optimiser les performances :
```bash
# Via l'API Elasticsearch
curl -X PUT "localhost:9200/telecom-events/_settings" -H 'Content-Type: application/json' -d'
{
  "index": {
    "refresh_interval": "30s",
    "number_of_replicas": 0
  }
}'
```

## Démarrage des Applications

### Générateur de Données

```bash
cd data-generator
pip install -r requirements.txt
python generator.py
```

Pour un mode test (60 secondes) :
```bash
python generator.py
```

Pour une exécution continue, modifiez `generator.py` et commentez la ligne `generator.run(duration_seconds=60)`.

### Processeur Java

```bash
cd java-processor
mvn clean package
java -jar target/telecom-processor-1.0.jar
```

Avec configuration personnalisée :
```bash
java -Dkafka.bootstrap.servers=localhost:9092 \
     -Delasticsearch.host=localhost \
     -jar target/telecom-processor-1.0.jar
```

### Traitement Batch Spark

```bash
cd spark-batch
pip install -r requirements.txt
spark-submit batch_processor.py
```

Avec plage temporelle spécifique :
```bash
spark-submit batch_processor.py \
  --start-time "2024-01-01T00:00:00Z" \
  --end-time "2024-01-02T00:00:00Z" \
  --output ./output
```

## Configuration Kibana

### 1. Accéder à Kibana
Ouvrez http://localhost:5601 dans votre navigateur.

### 2. Créer l'Index Pattern
1. Allez dans **Stack Management** > **Index Patterns**
2. Cliquez sur **Create index pattern**
3. Entrez `telecom-events*`
4. Sélectionnez `@timestamp` comme time field
5. Cliquez sur **Create index pattern**

### 3. Importer le Dashboard
1. Allez dans **Stack Management** > **Saved Objects**
2. Cliquez sur **Import**
3. Sélectionnez `kibana/dashboards/telecom-dashboard.json`
4. Cliquez sur **Import**

### 4. Visualiser les Données
Allez dans **Dashboard** et sélectionnez **Telecom Network Monitoring Dashboard**.

## Monitoring

### Vérifier les Logs

**Kafka**
```bash
docker logs kafka
```

**Elasticsearch**
```bash
docker logs elasticsearch
```

**Kibana**
```bash
docker logs kibana
```

### Vérifier les Métriques

**Kafka Topics**
```bash
docker exec kafka kafka-topics --list --bootstrap-server localhost:29092
docker exec kafka kafka-topics --describe --bootstrap-server localhost:29092 --topic telecom-events
```

**Elasticsearch Health**
```bash
curl http://localhost:9200/_cluster/health
```

**Nombre de Documents**
```bash
curl http://localhost:9200/telecom-events/_count
```

## Arrêt de l'Infrastructure

```bash
# Windows
scripts\stop.bat

# Linux/Mac
./scripts/stop.sh
```

Pour supprimer les volumes Docker (attention : supprime les données) :
```bash
cd docker
docker-compose down -v
```

## Dépannage

### Kafka ne démarre pas
```bash
# Vérifier si Zookeeper est démarré
docker logs zookeeper

# Redémarrer Kafka
docker-compose restart kafka
```

### Elasticsearch out of memory
```bash
# Modifier docker-compose.yml
# Augmenter ES_JAVA_OPTS
environment:
  - "ES_JAVA_OPTS=-Xms1g -Xmx1g"
```

### Le processeur Java ne se connecte pas à Kafka
```bash
# Vérifier la connectivité
telnet localhost 9092

# Vérifier les logs du processeur
# Les logs devraient indiquer l'erreur de connexion
```

### Kibana n'affiche pas les données
```bash
# Vérifier que l'index pattern est créé
curl http://localhost:9200/_cat/indices?v

# Vérifier que des données sont indexées
curl http://localhost:9200/telecom-events/_search?size=1
```

### Spark ne se connecte pas à Elasticsearch
```bash
# Vérifier la connectivité
curl http://localhost:9200

# Vérifier que le connecteur Spark-Elasticsearch est disponible
spark-submit --packages org.elasticsearch:elasticsearch-spark-30_2.12:8.11.0 batch_processor.py
```

## Déploiement en Production

### Sécurité

**Kafka**
```properties
# Activer SASL
security.inter.broker.protocol=SASL_PLAINTEXT
sasl.mechanism.inter.broker.protocol=PLAIN
sasl.enabled.mechanisms=PLAIN
```

**Elasticsearch**
```yaml
# Activer l'authentification
xpack.security.enabled: true
xpack.security.http.ssl.enabled: true
```

### Scalabilité

**Kafka**
- Augmenter le nombre de brokers
- Augmenter le nombre de partitions
- Configurer la réplication

**Elasticsearch**
- Ajouter des nœuds au cluster
- Configurer les shards et replicas
- Utiliser des hot/warm architectures

**Application Java**
- Déployer plusieurs instances
- Utiliser un load balancer
- Configurer le scaling horizontal

### Monitoring de Production

Utilisez des outils comme :
- **Prometheus + Grafana** : Métriques et alertes
- **ELK Stack** : Logs centralisés
- **Jaeger** : Distributed tracing
- **Datadog/New Relic** : APM

## Sauvegarde et Restauration

### Elasticsearch
```bash
# Snapshot
curl -X PUT "localhost:9200/_snapshot/backup_repo/snapshot_1"

# Restauration
curl -X POST "localhost:9200/_snapshot/backup_repo/snapshot_1/_restore"
```

### Kafka
```bash
# Utiliser MirrorMaker pour la réplication
# ou des outils tiers comme Confluent Replicator
```

## Mise à Jour

### Mise à jour de l'Application
```bash
# Arrêter l'application
# Compiler la nouvelle version
cd java-processor
mvn clean package

# Redémarrer avec le nouveau JAR
java -jar target/telecom-processor-1.0.jar
```

### Mise à jour de l'Infrastructure
```bash
cd docker
docker-compose pull
docker-compose up -d
```

## Support

Pour les problèmes ou questions :
- Consultez les logs des services
- Vérifiez la documentation officielle de chaque technologie
- Créez une issue sur le repository GitHub
