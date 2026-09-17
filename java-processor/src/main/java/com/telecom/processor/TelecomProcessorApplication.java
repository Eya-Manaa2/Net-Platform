package com.telecom.processor;

import com.telecom.kafka.TelecomKafkaConsumer;
import com.telecom.model.TelecomEvent;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Timer;
import java.util.TimerTask;

/**
 * Application principale de traitement temps réel
 * Consomme les événements Kafka, les traite et les stocke dans Elasticsearch
 */
public class TelecomProcessorApplication {
    private static final Logger logger = LoggerFactory.getLogger(TelecomProcessorApplication.class);
    
    private static final String KAFKA_BOOTSTRAP_SERVERS = System.getenv().getOrDefault("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092");
    private static final String KAFKA_TOPIC = System.getenv().getOrDefault("KAFKA_TOPIC", "telecom-events");
    private static final String KAFKA_GROUP_ID = "telecom-processor-group";
    private static final String ELASTICSEARCH_HOST = System.getenv().getOrDefault("ELASTICSEARCH_HOST", "localhost");
    private static final int ELASTICSEARCH_PORT = Integer.parseInt(System.getenv().getOrDefault("ELASTICSEARCH_PORT", "9200"));
    private static final String ELASTICSEARCH_INDEX = "telecom-events";
    
    private final EventProcessor processor;
    private final TelecomElasticsearchClient esClient;
    private final TelecomKafkaConsumer kafkaConsumer;
    private volatile boolean running = true;
    
    public TelecomProcessorApplication() {
        this.processor = new EventProcessor();
        this.esClient = new TelecomElasticsearchClient(ELASTICSEARCH_HOST, ELASTICSEARCH_PORT, ELASTICSEARCH_INDEX);
        this.kafkaConsumer = new TelecomKafkaConsumer(KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, KAFKA_GROUP_ID);
    }
    
    public void start() {
        logger.info("Starting Telecom Processor Application");
        logger.info("Kafka bootstrap servers: {}", KAFKA_BOOTSTRAP_SERVERS);
        logger.info("Kafka topic: {}", KAFKA_TOPIC);
        logger.info("Elasticsearch: {}:{}", ELASTICSEARCH_HOST, ELASTICSEARCH_PORT);
        
        // Timer pour afficher les statistiques périodiquement
        Timer statsTimer = new Timer("StatisticsTimer", true);
        statsTimer.schedule(new TimerTask() {
            @Override
            public void run() {
                printStatistics();
            }
        }, 10000, 10000); // Toutes les 10 secondes
        
        // Hook d'arrêt propre
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            logger.info("Shutdown signal received");
            running = false;
            kafkaConsumer.shutdown();
            statsTimer.cancel();
            esClient.close();
            printStatistics();
        }));
        
        // Démarrage du consumer Kafka
        kafkaConsumer.subscribe((event, record) -> {
            if (!running) return;
            
            try {
                // Traitement de l'événement
                TelecomEvent processedEvent = processor.process(event);
                
                // Stockage dans Elasticsearch si valide
                if (processedEvent.isValid()) {
                    esClient.indexEvent(processedEvent);
                }
                
                // Log périodique
                if (processor.getStatistics().getTotalEvents() % 100 == 0) {
                    logger.info("Processed {} events", processor.getStatistics().getTotalEvents());
                }
                
            } catch (Exception e) {
                logger.error("Error processing event: {}", e.getMessage(), e);
            }
        });
    }
    
    private void printStatistics() {
        EventProcessor.ProcessingStatistics stats = processor.getStatistics();
        logger.info("=== Processing Statistics ===");
        logger.info("{}", stats);
        
        // Afficher les statistiques des top 5 cellules
        stats.getCellStatistics().entrySet().stream()
            .sorted((e1, e2) -> Long.compare(e2.getValue().getEventCount(), e1.getValue().getEventCount()))
            .limit(5)
            .forEach(entry -> {
                EventProcessor.CellStatistics cellStats = entry.getValue();
                logger.info("Cell {}: events={}, avg_throughput={:.2f} Mbps, avg_latency={:.2f} ms, anomaly_rate={:.2f}%",
                    entry.getKey(),
                    cellStats.getEventCount(),
                    cellStats.getAverageThroughput(),
                    cellStats.getAverageLatency(),
                    cellStats.getAnomalyRate() * 100
                );
            });
    }
    
    public static void main(String[] args) {
        TelecomProcessorApplication app = new TelecomProcessorApplication();
        app.start();
    }
}
