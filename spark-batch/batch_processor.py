"""
Traitement batch des données télécom avec PySpark
Analyse les données historiques et calcule les KPIs
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, avg, count, sum, min, max, stddev, 
    when, lit, window, current_timestamp, to_timestamp
)
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, BooleanType
import config
import argparse
from datetime import datetime, timedelta
import json


class TelecomBatchProcessor:
    """Processeur batch pour les données télécom"""
    
    def __init__(self, elasticsearch_host, elasticsearch_port, index_name):
        self.elasticsearch_host = elasticsearch_host
        self.elasticsearch_port = elasticsearch_port
        self.index_name = index_name
        
        # Initialisation de Spark
        self.spark = SparkSession.builder \
            .appName(config.SPARK_APP_NAME) \
            .master(config.SPARK_MASTER) \
            .config("spark.es.nodes", elasticsearch_host) \
            .config("spark.es.port", str(elasticsearch_port)) \
            .config("spark.jars.packages", "org.elasticsearch:elasticsearch-spark-30_2.12:8.11.0") \
            .getOrCreate()
        
        self.spark.sparkContext.setLogLevel("WARN")
        
    def read_data_from_elasticsearch(self, start_time=None, end_time=None):
        """Lit les données depuis Elasticsearch"""
        es_url = f"es/{self.index_name}"
        
        # Lecture depuis Elasticsearch
        df = self.spark.read.format("org.elasticsearch.spark.sql") \
            .option("es.nodes", self.elasticsearch_host) \
            .option("es.port", str(self.elasticsearch_port)) \
            .option("es.resource", self.index_name) \
            .load()
        
        # Filtrage par plage temporelle si spécifiée
        if start_time and end_time:
            df = df.filter(
                (col("timestamp") >= start_time) & 
                (col("timestamp") <= end_time)
            )
        
        return df
    
    def calculate_kpis(self, df):
        """Calcule les KPIs principaux"""
        print("Calculating KPIs...")
        
        # KPIs globaux
        global_kpis = df.agg(
            avg("throughput_mbps").alias("avg_throughput"),
            avg("latency_ms").alias("avg_latency"),
            avg("packet_loss_percent").alias("avg_packet_loss"),
            avg("signal_strength_dbm").alias("avg_signal_strength"),
            avg("connected_users").alias("avg_connected_users"),
            count("*").alias("total_events"),
            sum(when(col("is_anomaly") == True, 1).otherwise(0)).alias("total_anomalies"),
            avg("quality_score").alias("avg_quality_score")
        ).collect()[0]
        
        # KPIs par cellule
        cell_kpis = df.groupBy("cell_id").agg(
            avg("throughput_mbps").alias("avg_throughput"),
            avg("latency_ms").alias("avg_latency"),
            avg("packet_loss_percent").alias("avg_packet_loss"),
            avg("signal_strength_dbm").alias("avg_signal_strength"),
            avg("connected_users").alias("avg_connected_users"),
            count("*").alias("event_count"),
            sum(when(col("is_anomaly") == True, 1).otherwise(0)).alias("anomaly_count"),
            avg("quality_score").alias("avg_quality_score"),
            min("quality_score").alias("min_quality_score"),
            max("quality_score").alias("max_quality_score")
        ).withColumn(
            "anomaly_rate",
            col("anomaly_count") / col("event_count")
        )
        
        # KPIs par technologie
        tech_kpis = df.groupBy("technology").agg(
            avg("throughput_mbps").alias("avg_throughput"),
            avg("latency_ms").alias("avg_latency"),
            avg("packet_loss_percent").alias("avg_packet_loss"),
            count("*").alias("event_count"),
            sum(when(col("is_anomaly") == True, 1).otherwise(0)).alias("anomaly_count")
        ).withColumn(
            "anomaly_rate",
            col("anomaly_count") / col("event_count")
        )
        
        # KPIs par niveau de qualité
        quality_kpis = df.groupBy("quality_level").agg(
            count("*").alias("event_count"),
            avg("throughput_mbps").alias("avg_throughput"),
            avg("latency_ms").alias("avg_latency")
        )
        
        return {
            'global': global_kpis,
            'by_cell': cell_kpis,
            'by_technology': tech_kpis,
            'by_quality': quality_kpis
        }
    
    def identify_degraded_cells(self, df, threshold=0.1):
        """Identifie les cellules avec des dégradations récurrentes"""
        print("Identifying degraded cells...")
        
        degraded_cells = df.groupBy("cell_id").agg(
            count("*").alias("event_count"),
            sum(when(col("is_anomaly") == True, 1).otherwise(0)).alias("anomaly_count"),
            avg("quality_score").alias("avg_quality_score")
        ).withColumn(
            "anomaly_rate",
            col("anomaly_count") / col("event_count")
        ).filter(
            (col("anomaly_rate") > threshold) | 
            (col("avg_quality_score") < 40)
        ).orderBy(
            col("anomaly_rate").desc(),
            col("avg_quality_score").asc()
        )
        
        return degraded_cells
    
    def analyze_quality_evolution(self, df):
        """Analyse l'évolution de la qualité dans le temps"""
        print("Analyzing quality evolution...")
        
        # Conversion du timestamp
        df_with_time = df.withColumn(
            "event_time",
            to_timestamp(col("timestamp"))
        )
        
        # Évolution horaire de la qualité moyenne
        hourly_evolution = df_with_time.groupBy(
            window(col("event_time"), "1 hour")
        ).agg(
            avg("quality_score").alias("avg_quality_score"),
            avg("throughput_mbps").alias("avg_throughput"),
            avg("latency_ms").alias("avg_latency"),
            count("*").alias("event_count")
        ).orderBy("window")
        
        return hourly_evolution
    
    def generate_report(self, kpis, degraded_cells, evolution):
        """Génère un rapport JSON des résultats"""
        print("Generating report...")
        
        report = {
            'timestamp': datetime.utcnow().isoformat(),
            'summary': {
                'total_events': kpis['global']['total_events'],
                'total_anomalies': kpis['global']['total_anomalies'],
                'avg_throughput_mbps': float(kpis['global']['avg_throughput'] or 0),
                'avg_latency_ms': float(kpis['global']['avg_latency'] or 0),
                'avg_packet_loss_percent': float(kpis['global']['avg_packet_loss'] or 0),
                'avg_quality_score': float(kpis['global']['avg_quality_score'] or 0)
            },
            'degraded_cells': [],
            'technology_comparison': {},
            'quality_distribution': {}
        }
        
        # Cellules dégradées
        for row in degraded_cells.collect():
            report['degraded_cells'].append({
                'cell_id': row['cell_id'],
                'anomaly_rate': float(row['anomaly_rate']),
                'avg_quality_score': float(row['avg_quality_score']),
                'event_count': row['event_count']
            })
        
        # Comparaison par technologie
        for row in kpis['by_technology'].collect():
            report['technology_comparison'][row['technology']] = {
                'avg_throughput_mbps': float(row['avg_throughput'] or 0),
                'avg_latency_ms': float(row['avg_latency'] or 0),
                'anomaly_rate': float(row['anomaly_rate'] or 0),
                'event_count': row['event_count']
            }
        
        # Distribution par niveau de qualité
        for row in kpis['by_quality'].collect():
            report['quality_distribution'][row['quality_level']] = {
                'event_count': row['event_count'],
                'avg_throughput_mbps': float(row['avg_throughput'] or 0),
                'avg_latency_ms': float(row['avg_latency'] or 0)
            }
        
        return report
    
    def save_results(self, report, output_path):
        """Sauvegarde les résultats"""
        import os
        os.makedirs(output_path, exist_ok=True)
        
        # Sauvegarde du rapport JSON
        report_file = f"{output_path}/telecom_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Report saved to {report_file}")
        
        return report_file
    
    def run(self, start_time=None, end_time=None, output_path=None):
        """Exécute le traitement batch"""
        print(f"Starting batch processing...")
        print(f"Time range: {start_time} to {end_time}")
        
        try:
            # Lecture des données
            df = self.read_data_from_elasticsearch(start_time, end_time)
            event_count = df.count()
            print(f"Loaded {event_count} events from Elasticsearch")
            
            if event_count == 0:
                print("No events to process")
                return None
            
            # Calcul des KPIs
            kpis = self.calculate_kpis(df)
            
            # Identification des cellules dégradées
            degraded_cells = self.identify_degraded_cells(df, config.ANOMALY_THRESHOLD)
            
            # Analyse de l'évolution
            evolution = self.analyze_quality_evolution(df)
            
            # Génération du rapport
            report = self.generate_report(kpis, degraded_cells, evolution)
            
            # Sauvegarde des résultats
            if output_path:
                report_file = self.save_results(report, output_path)
            
            # Affichage des résultats
            self.print_summary(report)
            
            return report
            
        except Exception as e:
            print(f"Error during batch processing: {e}")
            raise e
        finally:
            self.spark.stop()
    
    def print_summary(self, report):
        """Affiche un résumé des résultats"""
        print("\n" + "="*50)
        print("BATCH PROCESSING SUMMARY")
        print("="*50)
        print(f"Total events processed: {report['summary']['total_events']}")
        print(f"Total anomalies detected: {report['summary']['total_anomalies']}")
        print(f"Average throughput: {report['summary']['avg_throughput_mbps']:.2f} Mbps")
        print(f"Average latency: {report['summary']['avg_latency_ms']:.2f} ms")
        print(f"Average packet loss: {report['summary']['avg_packet_loss_percent']:.2f}%")
        print(f"Average quality score: {report['summary']['avg_quality_score']:.2f}")
        
        print(f"\nDegraded cells (anomaly rate > {config.ANOMALY_THRESHOLD*100}%):")
        for cell in report['degraded_cells'][:5]:  # Top 5
            print(f"  - {cell['cell_id']}: {cell['anomaly_rate']*100:.1f}% anomalies, "
                  f"quality score: {cell['avg_quality_score']:.1f}")
        
        print(f"\nTechnology comparison:")
        for tech, stats in report['technology_comparison'].items():
            print(f"  - {tech}: {stats['avg_throughput_mbps']:.1f} Mbps, "
                  f"{stats['avg_latency_ms']:.1f} ms, "
                  f"{stats['anomaly_rate']*100:.1f}% anomalies")
        
        print("="*50 + "\n")


def main():
    parser = argparse.ArgumentParser(description='Telecom Batch Processor')
    parser.add_argument('--start-time', type=str, help='Start time (ISO format)')
    parser.add_argument('--end-time', type=str, help='End time (ISO format)')
    parser.add_argument('--output', type=str, default=config.OUTPUT_PATH, help='Output path')
    
    args = parser.parse_args()
    
    # Calcul de la plage temporelle par défaut (dernières 24h)
    if not args.start_time:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=24)
        args.start_time = start_time.isoformat()
        args.end_time = end_time.isoformat()
    
    processor = TelecomBatchProcessor(
        config.ELASTICSEARCH_HOST,
        config.ELASTICSEARCH_PORT,
        config.ELASTICSEARCH_INDEX
    )
    
    processor.run(args.start_time, args.end_time, args.output)


if __name__ == '__main__':
    main()
