"""
Outils de benchmarking pour la plateforme de traitement
Mesure les performances avant et après optimisation
"""

import time
import psutil
import json
import os
from datetime import datetime
from kafka import KafkaProducer, KafkaConsumer
import statistics


class PerformanceBenchmark:
    """Classe pour mesurer les performances de la pipeline"""
    
    def __init__(self):
        self.results = {
            'timestamp': datetime.utcnow().isoformat(),
            'system_info': self.get_system_info(),
            'benchmarks': []
        }
    
    def get_system_info(self):
        """Récupère les informations système"""
        return {
            'cpu_count': psutil.cpu_count(),
            'memory_total_gb': psutil.virtual_memory().total / (1024**3),
            'python_version': os.sys.version,
            'platform': os.sys.platform
        }
    
    def measure_kafka_producer_performance(self, bootstrap_servers, topic, num_events=1000):
        """Mesure les performances du producteur Kafka"""
        print(f"Measuring Kafka producer performance ({num_events} events)...")
        
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        # Mesure du temps CPU et mémoire avant
        cpu_before = psutil.cpu_percent(interval=0.1)
        mem_before = psutil.virtual_memory().percent
        
        start_time = time.time()
        latencies = []
        
        for i in range(num_events):
            event = {
                'test_id': i,
                'timestamp': datetime.utcnow().isoformat(),
                'data': 'x' * 100  # 100 bytes de données
            }
            
            event_start = time.time()
            future = producer.send(topic, value=event)
            future.get(timeout=10)
            event_end = time.time()
            
            latencies.append((event_end - event_start) * 1000)  # en ms
        
        end_time = time.time()
        
        # Mesure après
        cpu_after = psutil.cpu_percent(interval=0.1)
        mem_after = psutil.virtual_memory().percent
        
        producer.close()
        
        throughput = num_events / (end_time - start_time)
        
        benchmark = {
            'name': 'kafka_producer',
            'num_events': num_events,
            'duration_seconds': end_time - start_time,
            'throughput_events_per_sec': throughput,
            'avg_latency_ms': statistics.mean(latencies),
            'median_latency_ms': statistics.median(latencies),
            'p95_latency_ms': sorted(latencies)[int(len(latencies) * 0.95)],
            'p99_latency_ms': sorted(latencies)[int(len(latencies) * 0.99)],
            'cpu_usage_percent': cpu_after - cpu_before,
            'memory_usage_percent': mem_after - mem_before
        }
        
        self.results['benchmarks'].append(benchmark)
        print(f"  Throughput: {throughput:.2f} events/sec")
        print(f"  Avg latency: {benchmark['avg_latency_ms']:.2f} ms")
        
        return benchmark
    
    def measure_kafka_consumer_performance(self, bootstrap_servers, topic, group_id, duration_seconds=30):
        """Mesure les performances du consommateur Kafka"""
        print(f"Measuring Kafka consumer performance ({duration_seconds}s)...")
        
        consumer = KafkaConsumer(
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            auto_offset_reset='latest',
            enable_auto_commit=True,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        
        consumer.subscribe([topic])
        
        # Mesures avant
        cpu_before = psutil.cpu_percent(interval=0.1)
        mem_before = psutil.virtual_memory().percent
        
        start_time = time.time()
        event_count = 0
        processing_times = []
        
        while time.time() - start_time < duration_seconds:
            batch_start = time.time()
            messages = consumer.poll(timeout_ms=1000)
            batch_end = time.time()
            
            for topic_partition, records in messages.items():
                event_count += len(records)
                processing_times.append((batch_end - batch_start) * 1000)
        
        end_time = time.time()
        
        # Mesures après
        cpu_after = psutil.cpu_percent(interval=0.1)
        mem_after = psutil.virtual_memory().percent
        
        consumer.close()
        
        throughput = event_count / (end_time - start_time)
        
        benchmark = {
            'name': 'kafka_consumer',
            'duration_seconds': duration_seconds,
            'events_processed': event_count,
            'throughput_events_per_sec': throughput,
            'avg_processing_time_ms': statistics.mean(processing_times) if processing_times else 0,
            'cpu_usage_percent': cpu_after - cpu_before,
            'memory_usage_percent': mem_after - mem_before
        }
        
        self.results['benchmarks'].append(benchmark)
        print(f"  Throughput: {throughput:.2f} events/sec")
        print(f"  Events processed: {event_count}")
        
        return benchmark
    
    def measure_processing_latency(self, processing_function, num_iterations=100):
        """Mesure la latence d'une fonction de traitement"""
        print(f"Measuring processing latency ({num_iterations} iterations)...")
        
        latencies = []
        
        for _ in range(num_iterations):
            start = time.perf_counter()
            processing_function()
            end = time.perf_counter()
            latencies.append((end - start) * 1000)  # en ms
        
        benchmark = {
            'name': 'processing_latency',
            'num_iterations': num_iterations,
            'avg_latency_ms': statistics.mean(latencies),
            'median_latency_ms': statistics.median(latencies),
            'min_latency_ms': min(latencies),
            'max_latency_ms': max(latencies),
            'p95_latency_ms': sorted(latencies)[int(len(latencies) * 0.95)],
            'p99_latency_ms': sorted(latencies)[int(len(latencies) * 0.99)]
        }
        
        self.results['benchmarks'].append(benchmark)
        print(f"  Avg latency: {benchmark['avg_latency_ms']:.4f} ms")
        
        return benchmark
    
    def compare_optimizations(self, baseline, optimized):
        """Compare deux benchmarks"""
        improvement = {}
        
        for metric in ['throughput_events_per_sec', 'avg_latency_ms', 'cpu_usage_percent']:
            if metric in baseline and metric in optimized:
                if 'throughput' in metric:
                    improvement[metric] = ((optimized[metric] - baseline[metric]) / baseline[metric]) * 100
                else:
                    improvement[metric] = ((baseline[metric] - optimized[metric]) / baseline[metric]) * 100
        
        return improvement
    
    def save_results(self, output_path):
        """Sauvegarde les résultats"""
        os.makedirs(output_path, exist_ok=True)
        
        filename = f"{output_path}/benchmark_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"Results saved to {filename}")
        return filename
    
    def print_summary(self):
        """Affiche un résumé des benchmarks"""
        print("\n" + "="*60)
        print("PERFORMANCE BENCHMARK SUMMARY")
        print("="*60)
        
        for benchmark in self.results['benchmarks']:
            print(f"\n{benchmark['name'].upper()}:")
            for key, value in benchmark.items():
                if key != 'name':
                    print(f"  {key}: {value}")
        
        print("="*60 + "\n")


def benchmark_java_processor():
    """Benchmark spécifique pour le processeur Java"""
    print("Note: Java processor benchmarking requires JMX or custom metrics")
    print("Consider using: JConsole, VisualVM, or adding Micrometer metrics")
    print("Key metrics to monitor:")
    print("  - JVM Heap Memory Usage")
    print("  - GC Pause Times")
    print("  - Thread Pool Usage")
    print("  - Kafka Consumer Lag")


def benchmark_spark_job(spark_submit_command, output_path):
    """Benchmark spécifique pour les jobs Spark"""
    print(f"Running Spark benchmark: {spark_submit_command}")
    print("Key Spark metrics to monitor:")
    print("  - Job Duration")
    print("  - Task Execution Time")
    print("  - Shuffle Read/Write")
    print("  - Executor Memory Usage")
    print("Use Spark UI (typically http://localhost:4040) for detailed metrics")


def main():
    """Fonction principale pour exécuter les benchmarks"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Performance Benchmarking Tool')
    parser.add_argument('--kafka-bootstrap', type=str, default='localhost:9092', 
                        help='Kafka bootstrap servers')
    parser.add_argument('--topic', type=str, default='telecom-events',
                        help='Kafka topic')
    parser.add_argument('--num-events', type=int, default=1000,
                        help='Number of events for producer benchmark')
    parser.add_argument('--duration', type=int, default=30,
                        help='Duration for consumer benchmark (seconds)')
    parser.add_argument('--output', type=str, default='./performance/results',
                        help='Output path for results')
    
    args = parser.parse_args()
    
    benchmark = PerformanceBenchmark()
    
    # Exécuter les benchmarks
    try:
        benchmark.measure_kafka_producer_performance(
            args.kafka_bootstrap, 
            args.topic, 
            args.num_events
        )
        
        benchmark.measure_kafka_consumer_performance(
            args.kafka_bootstrap,
            args.topic,
            'benchmark-consumer-group',
            args.duration
        )
        
        # Sauvegarder les résultats
        benchmark.save_results(args.output)
        benchmark.print_summary()
        
    except Exception as e:
        print(f"Error during benchmarking: {e}")


if __name__ == '__main__':
    main()
