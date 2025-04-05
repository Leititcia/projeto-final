#!/bin/bash

# Aguarda o banco de dados estar pronto
echo "Aguardando o banco de dados..."
while ! nc -z db 5432; do
  sleep 1
done
echo "Banco de dados está pronto!"
sleep 5
echo "Executando migrações..."
python database/migrations/run_migration.py

# Inicia a aplicação
echo "Iniciando a aplicação..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload 