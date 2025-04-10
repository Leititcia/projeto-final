import os
import sys
import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from passlib.context import CryptContext

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Carrega as variáveis de ambiente
load_dotenv()

# Configurações do banco de dados
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")

def run_migration():
    # Configurar o contexto de criptografia
    pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
    
    conn = None
    cur = None
    try:
        # Conecta ao banco de dados
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # Criar tabela de usuários
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)

        # Criar tabela de clientes
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(20),
                address TEXT
            )
        """)

        # Criar tabela de medicamentos
        cur.execute("""
            CREATE TABLE IF NOT EXISTS medicines (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                generic_name VARCHAR(100),
                manufacturer VARCHAR(100),
                type VARCHAR(50),
                pharmaceutical_form VARCHAR(50),
                lote VARCHAR(50),
                fabricacao DATE,
                validade DATE,
                fornecedor VARCHAR(100),
                price FLOAT NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 0
            )
        """)

        # Verificar se as colunas já existem e adicionar se necessário
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'medicines'
        """)
        existing_columns = [row[0] for row in cur.fetchall()]
        
        # Adiciona as novas colunas se não existirem
        if 'generic_name' not in existing_columns:
            cur.execute("ALTER TABLE medicines ADD COLUMN generic_name VARCHAR(100)")
            print("Coluna 'generic_name' adicionada com sucesso!")
        
        if 'manufacturer' not in existing_columns:
            cur.execute("ALTER TABLE medicines ADD COLUMN manufacturer VARCHAR(100)")
            print("Coluna 'manufacturer' adicionada com sucesso!")
        
        if 'type' not in existing_columns:
            cur.execute("ALTER TABLE medicines ADD COLUMN type VARCHAR(50)")
            print("Coluna 'type' adicionada com sucesso!")
        
        if 'pharmaceutical_form' not in existing_columns:
            cur.execute("ALTER TABLE medicines ADD COLUMN pharmaceutical_form VARCHAR(50)")
            print("Coluna 'pharmaceutical_form' adicionada com sucesso!")
            
        if 'lote' not in existing_columns:
            cur.execute("ALTER TABLE medicines ADD COLUMN lote VARCHAR(50)")
            print("Coluna 'lote' adicionada com sucesso!")
            
        if 'fabricacao' not in existing_columns:
            cur.execute("ALTER TABLE medicines ADD COLUMN fabricacao DATE")
            print("Coluna 'fabricacao' adicionada com sucesso!")
            
        if 'validade' not in existing_columns:
            cur.execute("ALTER TABLE medicines ADD COLUMN validade DATE")
            print("Coluna 'validade' adicionada com sucesso!")
            
        if 'fornecedor' not in existing_columns:
            cur.execute("ALTER TABLE medicines ADD COLUMN fornecedor VARCHAR(100)")
            print("Coluna 'fornecedor' adicionada com sucesso!")

        # Criar tabela de vendas
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id SERIAL PRIMARY KEY,
                client_id INTEGER REFERENCES clients(id),
                medicine_id INTEGER REFERENCES medicines(id),
                quantity INTEGER NOT NULL,
                total_price FLOAT NOT NULL,
                sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Inserir usuário admin se não existir
        hashed_password = pwd_context.hash("admin123")
        cur.execute("""
            INSERT INTO users (username, password)
            VALUES ('admin', %s)
            ON CONFLICT (username) DO NOTHING
        """, (hashed_password,))

        print("Migração concluída com sucesso!")

    except Exception as e:
        print(f"Erro durante a migração: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    run_migration() 