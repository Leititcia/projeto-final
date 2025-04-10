-- Adiciona a coluna user_id à tabela sales
ALTER TABLE sales ADD COLUMN user_id INTEGER REFERENCES users(id);

-- Atualiza registros existentes com o ID do primeiro usuário (geralmente o admin)
UPDATE sales SET user_id = (SELECT id FROM users LIMIT 1) WHERE user_id IS NULL; 