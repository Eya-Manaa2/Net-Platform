package com.telecom.processor;

import com.telecom.model.TelecomEvent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.atomic.AtomicLong;

/**
 * Processeur d'événements télécom
 * Valide, transforme et enrichit les événements
 */
public class EventProcessor {
    private static final Logger logger = LoggerFactory.getLogger(EventProcessor.class);
    
    // Statistiques de traitement
    private final AtomicLong totalEvents = new AtomicLong(0);
    private final AtomicLong validEvents = new AtomicLong(0);
    private final AtomicLong invalidEvents = new AtomicLong(0);
    private final AtomicLong anomaliesDetected = new AtomicLong(0);
    
    // Statistiques par cellule
    private final Map<String, CellStatistics> cellStatistics = new HashMap<>();
    
    // Seuils de validation
    private static final double MAX_PACKET_LOSS = 10.0; // %
    private static final double MAX_LATENCY_4G = 300.0; // ms
    private static final double MAX_LATENCY_5G = 150.0; // ms
    private static final double MIN_SIGNAL_STRENGTH = -130.0; // dBm
    private static final double MIN_THROUGHPUT = 1.0; // Mbps
    
    /**
     * Traite un événement télécom
     */
    public TelecomEvent process(TelecomEvent event) {
        totalEvents.incrementAndGet();
        
        // Validation
        validateEvent(event);
        
        if (event.isValid()) {
            validEvents.incrementAndGet();
            
            // Transformation et enrichissement
            enrichEvent(event);
            
            // Mise à jour des statistiques
            updateStatistics(event);
            
            // Détection d'anomalies
            detectAnomalies(event);
            
            if (event.isAnomaly()) {
                anomaliesDetected.incrementAndGet();
                logger.warn("Anomaly detected in cell {}: {}", event.getCellId(), event.getValidationMessage());
            }
        } else {
            invalidEvents.incrementAndGet();
            logger.debug("Invalid event from cell {}: {}", event.getCellId(), event.getValidationMessage());
        }
        
        return event;
    }
    
    /**
     * Valide un événement
     */
    private void validateEvent(TelecomEvent event) {
        StringBuilder validationMessage = new StringBuilder();
        boolean isValid = true;
        
        // Vérification des champs obligatoires
        if (event.getCellId() == null || event.getCellId().isEmpty()) {
            validationMessage.append("Missing cell_id; ");
            isValid = false;
        }
        
        if (event.getTimestamp() == null || event.getTimestamp().isEmpty()) {
            validationMessage.append("Missing timestamp; ");
            isValid = false;
        }
        
        if (event.getTechnology() == null || 
            (!event.getTechnology().equals("4G") && !event.getTechnology().equals("5G"))) {
            validationMessage.append("Invalid technology; ");
            isValid = false;
        }
        
        // Vérification des plages de valeurs
        if (event.getPacketLossPercent() < 0 || event.getPacketLossPercent() > MAX_PACKET_LOSS) {
            validationMessage.append(String.format("Packet loss %.2f%% out of range; ", event.getPacketLossPercent()));
            isValid = false;
        }
        
        if (event.getSignalStrengthDbm() < MIN_SIGNAL_STRENGTH || event.getSignalStrengthDbm() > -30) {
            validationMessage.append(String.format("Signal strength %.2f dBm out of range; ", event.getSignalStrengthDbm()));
            isValid = false;
        }
        
        if (event.getThroughputMbps() < MIN_THROUGHPUT) {
            validationMessage.append(String.format("Throughput %.2f Mbps too low; ", event.getThroughputMbps()));
            isValid = false;
        }
        
        double maxLatency = event.getTechnology().equals("5G") ? MAX_LATENCY_5G : MAX_LATENCY_4G;
        if (event.getLatencyMs() > maxLatency) {
            validationMessage.append(String.format("Latency %.2f ms exceeds threshold %.2f ms; ", 
                event.getLatencyMs(), maxLatency));
            isValid = false;
        }
        
        if (event.getConnectedUsers() < 0) {
            validationMessage.append("Negative connected users; ");
            isValid = false;
        }
        
        event.setValid(isValid);
        event.setValidationMessage(validationMessage.toString());
    }
    
    /**
     * Enrichit l'événement avec des informations calculées
     */
    private void enrichEvent(TelecomEvent event) {
        // Calcul du score de qualité (0-100)
        double throughputScore = Math.min(event.getThroughputMbps() / 500.0 * 40, 40);
        double latencyScore = Math.max(40 - (event.getLatencyMs() / 5.0), 0);
        double packetLossScore = Math.max(20 - (event.getPacketLossPercent() * 4), 0);
        double signalScore = Math.max((event.getSignalStrengthDbm() + 130) / 0.7, 0);
        
        double qualityScore = throughputScore + latencyScore + packetLossScore + signalScore;
        event.setQualityScore(Math.round(qualityScore * 100.0) / 100.0);
        
        // Détermination du niveau de qualité
        if (qualityScore >= 80) {
            event.setQualityLevel("EXCELLENT");
        } else if (qualityScore >= 60) {
            event.setQualityLevel("GOOD");
        } else if (qualityScore >= 40) {
            event.setQualityLevel("FAIR");
        } else {
            event.setQualityLevel("POOR");
        }
    }
    
    /**
     * Détecte les anomalies dans l'événement
     */
    private void detectAnomalies(TelecomEvent event) {
        boolean isAnomaly = false;
        StringBuilder message = new StringBuilder(event.getValidationMessage());
        
        // Détection basée sur les seuils
        if (event.getPacketLossPercent() > 3.0) {
            isAnomaly = true;
            message.append("High packet loss; ");
        }
        
        double maxLatency = event.getTechnology().equals("5G") ? MAX_LATENCY_5G * 0.7 : MAX_LATENCY_4G * 0.7;
        if (event.getLatencyMs() > maxLatency) {
            isAnomaly = true;
            message.append("High latency; ");
        }
        
        if (event.getSignalStrengthDbm() < -110) {
            isAnomaly = true;
            message.append("Weak signal; ");
        }
        
        if (event.getThroughputMbps() < 10.0) {
            isAnomaly = true;
            message.append("Low throughput; ");
        }
        
        event.setAnomaly(isAnomaly || event.isAnomaly());
        if (isAnomaly) {
            event.setValidationMessage(message.toString());
        }
    }
    
    /**
     * Met à jour les statistiques par cellule
     */
    private void updateStatistics(TelecomEvent event) {
        cellStatistics.computeIfAbsent(event.getCellId(), k -> new CellStatistics())
            .update(event);
    }
    
    /**
     * Retourne les statistiques de traitement
     */
    public ProcessingStatistics getStatistics() {
        return new ProcessingStatistics(
            totalEvents.get(),
            validEvents.get(),
            invalidEvents.get(),
            anomaliesDetected.get(),
            new HashMap<>(cellStatistics)
        );
    }
    
    /**
     * Réinitialise les statistiques
     */
    public void resetStatistics() {
        totalEvents.set(0);
        validEvents.set(0);
        invalidEvents.set(0);
        anomaliesDetected.set(0);
        cellStatistics.clear();
    }
    
    /**
     * Statistiques par cellule
     */
    public static class CellStatistics {
        private long eventCount = 0;
        private double totalThroughput = 0.0;
        private double totalLatency = 0.0;
        private double totalPacketLoss = 0.0;
        private long anomalyCount = 0;
        
        public synchronized void update(TelecomEvent event) {
            eventCount++;
            totalThroughput += event.getThroughputMbps();
            totalLatency += event.getLatencyMs();
            totalPacketLoss += event.getPacketLossPercent();
            if (event.isAnomaly()) {
                anomalyCount++;
            }
        }
        
        public double getAverageThroughput() {
            return eventCount > 0 ? totalThroughput / eventCount : 0;
        }
        
        public double getAverageLatency() {
            return eventCount > 0 ? totalLatency / eventCount : 0;
        }
        
        public double getAveragePacketLoss() {
            return eventCount > 0 ? totalPacketLoss / eventCount : 0;
        }
        
        public double getAnomalyRate() {
            return eventCount > 0 ? (double) anomalyCount / eventCount : 0;
        }
        
        public long getEventCount() {
            return eventCount;
        }
    }
    
    /**
     * Statistiques globales de traitement
     */
    public static class ProcessingStatistics {
        private final long totalEvents;
        private final long validEvents;
        private final long invalidEvents;
        private final long anomaliesDetected;
        private final Map<String, CellStatistics> cellStatistics;
        
        public ProcessingStatistics(long totalEvents, long validEvents, long invalidEvents, 
                                    long anomaliesDetected, Map<String, CellStatistics> cellStatistics) {
            this.totalEvents = totalEvents;
            this.validEvents = validEvents;
            this.invalidEvents = invalidEvents;
            this.anomaliesDetected = anomaliesDetected;
            this.cellStatistics = cellStatistics;
        }
        
        public long getTotalEvents() {
            return totalEvents;
        }
        
        public long getValidEvents() {
            return validEvents;
        }
        
        public long getInvalidEvents() {
            return invalidEvents;
        }
        
        public long getAnomaliesDetected() {
            return anomaliesDetected;
        }
        
        public Map<String, CellStatistics> getCellStatistics() {
            return cellStatistics;
        }
        
        public double getValidityRate() {
            return totalEvents > 0 ? (double) validEvents / totalEvents : 0;
        }
        
        @Override
        public String toString() {
            return String.format(
                "ProcessingStatistics{total=%d, valid=%d (%.2f%%), invalid=%d, anomalies=%d, cells=%d}",
                totalEvents, validEvents, getValidityRate() * 100, 
                invalidEvents, anomaliesDetected, cellStatistics.size()
            );
        }
    }
}
