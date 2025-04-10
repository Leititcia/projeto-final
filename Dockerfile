FROM python:3.11-slim

WORKDIR /app

# Instala o netcat para verificar a disponibilidade do banco de dados
RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Torna o script de inicialização executável
RUN chmod +x start.sh

EXPOSE 8000

CMD ["sh", "./start.sh"]