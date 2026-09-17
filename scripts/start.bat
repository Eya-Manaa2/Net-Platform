@echo off
REM Script de démarrage de l'infrastructure (Windows)

echo Starting Telecom Data Processing Platform...

REM Vérifier si Docker est en cours d'exécution
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Docker is not running. Please start Docker Desktop first.
    exit /b 1
)

REM Démarrer l'infrastructure Docker
cd docker
echo Starting Kafka, Elasticsearch, and Kibana...
docker-compose up -d

REM Attendre que les services soient prêts
echo Waiting for services to be ready...
timeout /t 30 /nobreak

REM Vérifier l'état des services
echo Checking service status...
docker-compose ps

REM Créer le topic Kafka si nécessaire
echo Creating Kafka topic...
docker exec kafka kafka-topics --create --if-not-exists --bootstrap-server localhost:29092 --partitions 3 --replication-factor 1 --topic telecom-events

echo Infrastructure started successfully!
echo.
echo Service URLs:
echo   - Kafka: localhost:9092
echo   - Elasticsearch: http://localhost:9200
echo   - Kibana: http://localhost:5601
echo.
echo Next steps:
echo   1. Start the data generator: cd data-generator ^&^& python generator.py
echo   2. Start the Java processor: cd java-processor ^&^& mvn clean package ^&^& java -jar target\telecom-processor-1.0.jar
echo   3. Access Kibana at http://localhost:5601 to visualize data

cd ..
