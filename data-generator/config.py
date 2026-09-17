"""
Configuration du générateur de données télécom
"""

import os

# Configuration Kafka
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_TOPIC = 'telecom-events'

# Configuration génération
EVENTS_PER_SECOND = 10
CELL_IDS = [f'CELL_{i:03d}' for i in range(1, 51)]  # 50 cellules
TECHNOLOGIES = ['4G', '5G']

# Plages de valeurs pour les métriques
THROUGHPUT_RANGE = (10, 1000)  # Mbps
LATENCY_RANGE = (5, 200)  # ms
PACKET_LOSS_RANGE = (0, 5)  # %
SIGNAL_STRENGTH_RANGE = (-120, -60)  # dBm
CONNECTED_USERS_RANGE = (10, 500)

# Probabilités d'anomalies
ANOMALY_PROBABILITY = 0.05  # 5% de chance d'anomalie

# Configuration Elasticsearch (optionnel pour stockage direct)
ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST', 'localhost:9200')
ELASTICSEARCH_INDEX = 'telecom-events'
