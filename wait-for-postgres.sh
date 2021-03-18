#!/bin/sh
# wait-for-postgres.sh
set -e

host="$1"
shift

cmd="$@"
  
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U $POSTGRES_USER -c '\q'; do
  >&2 
  echo "PostgreSQL is unavailable or sleeping!"
  sleep 1
done
  
>&2 
echo ""
echo "PostgreSQL is running! - starting MercadoRetoAPI server..."
echo ""
exec $cmd