@ECHO OFF
TITLE MercadoRetoAPI

:: This batch file initializes Docker Compose command to start MercadoRetoAPI api and db containers.

ECHO Initializing MercadoRetoAPI Docker Containers...
ECHO.

docker-compose up --build