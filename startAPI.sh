#!/bin/sh
echo '\033]2;'MercadoRetoAPI'\007'

# This shell file initializes Docker Compose command to start MercadoRetoAPI api and db containers.

echo "Initializing MercadoRetoAPI Docker Containers..."
echo ""

sudo docker-compose up --build