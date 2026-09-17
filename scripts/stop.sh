#!/bin/bash

# Script d'arrêt de l'infrastructure

echo "Stopping Telecom Data Processing Platform..."

cd docker
docker-compose down

echo "Infrastructure stopped successfully!"
