"""
Générateur de données télécom en temps réel
Produit des événements réseau réalistes et les publie dans Kafka
"""

import json
import random
import time
from datetime import datetime, timedelta
from kafka import KafkaProducer
import config


class TelecomEventGenerator:
    """Générateur d'événements télécom"""
    
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all',
            retries=3
        )
        self.cell_ids = config.CELL_IDS
        self.technologies = config.TECHNOLOGIES
        
    def generate_event(self):
        """Génère un événement télécom réaliste"""
        cell_id = random.choice(self.cell_ids)
        technology = random.choice(self.technologies)
        
        # Ajuster les valeurs selon la technologie
        if technology == '5G':
            throughput = random.uniform(*config.THROUGHPUT_RANGE) * 1.5
            latency = random.uniform(*config.LATENCY_RANGE) * 0.7
            signal_strength = random.uniform(-100, -50)
        else:  # 4G
            throughput = random.uniform(*config.THROUGHPUT_RANGE)
            latency = random.uniform(*config.LATENCY_RANGE)
            signal_strength = random.uniform(*config.SIGNAL_STRENGTH_RANGE)
        
        # Introduire des anomalies occasionnelles
        if random.random() < config.ANOMALY_PROBABILITY:
            throughput *= 0.3  # Dégradation du débit
            latency *= 2.5     # Augmentation de la latence
            signal_strength -= 15  # Signal faible
        
        event = {
            'cell_id': cell_id,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'technology': technology,
            'throughput_mbps': round(throughput, 2),
            'latency_ms': round(latency, 2),
            'packet_loss_percent': round(random.uniform(*config.PACKET_LOSS_RANGE), 2),
            'signal_strength_dbm': round(signal_strength, 2),
            'connected_users': random.randint(*config.CONNECTED_USERS_RANGE),
            'is_anomaly': random.random() < config.ANOMALY_PROBABILITY
        }
        
        return event
    
    def publish_event(self, event):
        """Publie un événement dans Kafka"""
        try:
            future = self.producer.send(config.KAFKA_TOPIC, value=event)
            record_metadata = future.get(timeout=10)
            print(f"Event published to {record_metadata.topic} "
                  f"partition {record_metadata.partition} offset {record_metadata.offset}")
            return True
        except Exception as e:
            print(f"Error publishing event: {e}")
            return False
    
    def run(self, duration_seconds=None):
        """Exécute le générateur en continu"""
        print(f"Starting telecom event generator...")
        print(f"Kafka bootstrap servers: {config.KAFKA_BOOTSTRAP_SERVERS}")
        print(f"Topic: {config.KAFKA_TOPIC}")
        print(f"Events per second: {config.EVENTS_PER_SECOND}")
        print(f"Cells: {len(self.cell_ids)}")
        
        start_time = time.time()
        event_count = 0
        
        try:
            while True:
                event = self.generate_event()
                self.publish_event(event)
                event_count += 1
                
                # Contrôle du débit
                time.sleep(1.0 / config.EVENTS_PER_SECOND)
                
                # Arrêt après durée spécifiée
                if duration_seconds and (time.time() - start_time) >= duration_seconds:
                    break
                    
                # Affichage de statistiques toutes les 100 événements
                if event_count % 100 == 0:
                    elapsed = time.time() - start_time
                    rate = event_count / elapsed
                    print(f"Generated {event_count} events ({rate:.2f} events/sec)")
                    
        except KeyboardInterrupt:
            print("\nGenerator stopped by user")
        finally:
            self.producer.close()
            print(f"Total events generated: {event_count}")


if __name__ == '__main__':
    generator = TelecomEventGenerator()
    
    # Mode test : génère pendant 60 secondes
    # Commenter cette ligne pour une exécution continue
    generator.run(duration_seconds=60)
    
    # Mode production : exécution continue
    # generator.run()
