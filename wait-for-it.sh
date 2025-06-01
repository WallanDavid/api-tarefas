#!/usr/bin/env bash
# Espera o Redis ficar disponível

HOST=$1
PORT=$2
shift 2
CMD="$@"

echo "⏳ Aguardando $HOST:$PORT ficar disponível..."
while ! nc -z $HOST $PORT; do
  sleep 1
done

echo "✅ $HOST:$PORT está pronto! Executando: $CMD"
exec $CMD
