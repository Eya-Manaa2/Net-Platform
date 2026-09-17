package com.telecom.model;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.time.Instant;
import java.util.Objects;

/**
 * Modèle représentant un événement télécom
 */
public class TelecomEvent {
    
    @JsonProperty("cell_id")
    private String cellId;
    
    @JsonProperty("timestamp")
    @JsonFormat(shape = JsonFormat.Shape.STRING)
    private String timestamp;
    
    @JsonProperty("technology")
    private String technology;
    
    @JsonProperty("throughput_mbps")
    private double throughputMbps;
    
    @JsonProperty("latency_ms")
    private double latencyMs;
    
    @JsonProperty("packet_loss_percent")
    private double packetLossPercent;
    
    @JsonProperty("signal_strength_dbm")
    private double signalStrengthDbm;
    
    @JsonProperty("connected_users")
    private int connectedUsers;
    
    @JsonProperty("is_anomaly")
    private boolean isAnomaly;
    
    // Champs calculés après traitement
    private boolean isValid;
    private String validationMessage;
    private double qualityScore;
    private String qualityLevel;
    
    public TelecomEvent() {
    }
    
    // Getters and Setters
    public String getCellId() {
        return cellId;
    }
    
    public void setCellId(String cellId) {
        this.cellId = cellId;
    }
    
    public String getTimestamp() {
        return timestamp;
    }
    
    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }
    
    public String getTechnology() {
        return technology;
    }
    
    public void setTechnology(String technology) {
        this.technology = technology;
    }
    
    public double getThroughputMbps() {
        return throughputMbps;
    }
    
    public void setThroughputMbps(double throughputMbps) {
        this.throughputMbps = throughputMbps;
    }
    
    public double getLatencyMs() {
        return latencyMs;
    }
    
    public void setLatencyMs(double latencyMs) {
        this.latencyMs = latencyMs;
    }
    
    public double getPacketLossPercent() {
        return packetLossPercent;
    }
    
    public void setPacketLossPercent(double packetLossPercent) {
        this.packetLossPercent = packetLossPercent;
    }
    
    public double getSignalStrengthDbm() {
        return signalStrengthDbm;
    }
    
    public void setSignalStrengthDbm(double signalStrengthDbm) {
        this.signalStrengthDbm = signalStrengthDbm;
    }
    
    public int getConnectedUsers() {
        return connectedUsers;
    }
    
    public void setConnectedUsers(int connectedUsers) {
        this.connectedUsers = connectedUsers;
    }
    
    public boolean isAnomaly() {
        return isAnomaly;
    }
    
    public void setAnomaly(boolean anomaly) {
        isAnomaly = anomaly;
    }
    
    public boolean isValid() {
        return isValid;
    }
    
    public void setValid(boolean valid) {
        isValid = valid;
    }
    
    public String getValidationMessage() {
        return validationMessage;
    }
    
    public void setValidationMessage(String validationMessage) {
        this.validationMessage = validationMessage;
    }
    
    public double getQualityScore() {
        return qualityScore;
    }
    
    public void setQualityScore(double qualityScore) {
        this.qualityScore = qualityScore;
    }
    
    public String getQualityLevel() {
        return qualityLevel;
    }
    
    public void setQualityLevel(String qualityLevel) {
        this.qualityLevel = qualityLevel;
    }
    
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        TelecomEvent that = (TelecomEvent) o;
        return Objects.equals(cellId, that.cellId) &&
               Objects.equals(timestamp, that.timestamp);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(cellId, timestamp);
    }
    
    @Override
    public String toString() {
        return "TelecomEvent{" +
               "cellId='" + cellId + '\'' +
               ", timestamp='" + timestamp + '\'' +
               ", technology='" + technology + '\'' +
               ", throughputMbps=" + throughputMbps +
               ", latencyMs=" + latencyMs +
               ", packetLossPercent=" + packetLossPercent +
               ", signalStrengthDbm=" + signalStrengthDbm +
               ", connectedUsers=" + connectedUsers +
               ", isAnomaly=" + isAnomaly +
               ", isValid=" + isValid +
               ", qualityScore=" + qualityScore +
               ", qualityLevel='" + qualityLevel + '\'' +
               '}';
    }
}
