@echo off
REM Script d'arrêt de l'infrastructure (Windows)

echo Stopping Telecom Data Processing Platform...

cd docker
docker-compose down

echo Infrastructure stopped successfully!

cd ..
