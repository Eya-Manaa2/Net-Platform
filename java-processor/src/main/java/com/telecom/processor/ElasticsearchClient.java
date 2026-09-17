package com.telecom.processor;

import co.elastic.clients.elasticsearch.ElasticsearchClient;
import co.elastic.clients.elasticsearch.core.IndexRequest;
import co.elastic.clients.elasticsearch.core.IndexResponse;
import co.elastic.clients.json.jackson.JacksonJsonpMapper;
import co.elastic.clients.transport.rest_client.RestClientTransport;
import com.telecom.model.TelecomEvent;
import org.apache.http.HttpHost;
import org.elasticsearch.client.RestClient;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;

/**
 * Client Elasticsearch pour stocker les événements traités
 */
public class TelecomElasticsearchClient {
    private static final Logger logger = LoggerFactory.getLogger(TelecomElasticsearchClient.class);
    
    private final ElasticsearchClient client;
    private final String indexName;
    
    public TelecomElasticsearchClient(String hostname, int port, String indexName) {
        this.indexName = indexName;
        
        RestClient restClient = RestClient.builder(
            new HttpHost(hostname, port, "http")
        ).build();
        
        JacksonJsonpMapper jsonMapper = new JacksonJsonpMapper();
        RestClientTransport transport = new RestClientTransport(restClient, jsonMapper);
        
        this.client = new ElasticsearchClient(transport);
        
        logger.info("Elasticsearch client initialized for index: {}", indexName);
    }
    
    /**
     * Indexe un événement dans Elasticsearch
     */
    public boolean indexEvent(TelecomEvent event) {
        try {
            IndexRequest<TelecomEvent> request = IndexRequest.of(i -> i
                .index(indexName)
                .id(event.getCellId() + "_" + System.currentTimeMillis())
                .document(event)
            );
            
            IndexResponse response = client.index(request);
            logger.debug("Event indexed with ID: {}", response.id());
            return true;
            
        } catch (IOException e) {
            logger.error("Error indexing event: {}", e.getMessage(), e);
            return false;
        }
    }
    
    /**
     * Ferme le client Elasticsearch
     */
    public void close() {
        try {
            if (client._transport() != null) {
                client._transport().close();
            }
            logger.info("Elasticsearch client closed");
        } catch (IOException e) {
            logger.error("Error closing Elasticsearch client: {}", e.getMessage(), e);
        }
    }
}
