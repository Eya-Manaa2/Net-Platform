package com.telecom.kafka;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.telecom.model.TelecomEvent;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.Duration;
import java.util.Collections;
import java.util.Properties;

/**
 * Consumer Kafka pour les événements télécom
 */
public class TelecomKafkaConsumer {
    private static final Logger logger = LoggerFactory.getLogger(TelecomKafkaConsumer.class);
    
    private final KafkaConsumer<String, String> consumer;
    private final String topic;
    private final ObjectMapper objectMapper;
    private volatile boolean running = true;
    
    public TelecomKafkaConsumer(String bootstrapServers, String topic, String groupId) {
        this.topic = topic;
        this.objectMapper = new ObjectMapper();
        
        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        props.put(ConsumerConfig.GROUP_ID_CONFIG, groupId);
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "latest");
        props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "true");
        props.put(ConsumerConfig.AUTO_COMMIT_INTERVAL_MS_CONFIG, "1000");
        
        this.consumer = new KafkaConsumer<>(props);
    }
    
    public void subscribe(EventHandler handler) {
        consumer.subscribe(Collections.singletonList(topic));
        logger.info("Subscribed to topic: {}", topic);
        
        try {
            while (running) {
                ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
                
                for (ConsumerRecord<String, String> record : records) {
                    try {
                        TelecomEvent event = objectMapper.readValue(record.value(), TelecomEvent.class);
                        handler.handle(event, record);
                    } catch (Exception e) {
                        logger.error("Error processing record: {}", e.getMessage(), e);
                    }
                }
            }
        } finally {
            consumer.close();
        }
    }
    
    public void shutdown() {
        running = false;
    }
    
    @FunctionalInterface
    public interface EventHandler {
        void handle(TelecomEvent event, ConsumerRecord<String, String> record);
    }
}
