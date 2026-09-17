"""
Configuration du traitement batch Spark
"""

import os

# Configuration Elasticsearch
ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST', 'localhost')
ELASTICSEARCH_PORT = os.getenv('ELASTICSEARCH_PORT', '9200')
ELASTICSEARCH_INDEX = 'telecom-events'

# Configuration Spark
SPARK_APP_NAME = 'TelecomBatchProcessor'
SPARK_MASTER = 'local[*]'  # Utiliser 'yarn' ou 'spark://host:port' en cluster

# Configuration du traitement
BATCH_INTERVAL_MINUTES = 60  # Intervalle de traitement en minutes
ANOMALY_THRESHOLD = 0.1  # 10% de taux d'anomalie considéré comme dégradé

# Seuils de qualité
QUALITY_THRESHOLDS = {
    'EXCELLENT': 80,
    'GOOD': 60,
    'FAIR': 40,
    'POOR': 0
}

# Sortie des résultats
OUTPUT_PATH = os.getenv('OUTPUT_PATH', './output')
