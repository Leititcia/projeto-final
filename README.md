# Sistema de Gestão de Farmácia

Sistema web desenvolvido para gerenciamento de farmácias, permitindo o controle de medicamentos, clientes e vendas.

## Tecnologias Utilizadas

- **Backend**:
  - FastAPI: Framework para construção de APIs em Python
  - SQLAlchemy: ORM para interação com o banco de dados
  - Pydantic: Validação de dados e criação de modelos
  - Python 3.10+: Linguagem de programação

- **Frontend**:
  - Jinja2: Template engine para renderização dinâmica
  - Bootstrap 5: Framework CSS para interface responsiva
  - JavaScript: Interatividade e validações no cliente

- **Banco de Dados**:
  - PostgreSQL: Sistema de gerenciamento de banco de dados relacional

## Como Instalar

1. **Clone o Repositório**:
   ```bash
   git clone https://github.com/seu-usuario/farmacia-api.git
   cd farmacia-api
   ```

2. **Configure as Variáveis de Ambiente**:
   - Crie um arquivo `.env` na raiz do projeto
   - Configure as variáveis de ambiente:
     ```
      DB_NAME=
      DB_USER=
      DB_PASSWORD=
      DB_HOST=
      DB_PORT=
      POSTGRES_DB=
      POSTGRES_USER=
      POSTGRES_PASSWORD=
      POSTGRES_HOST=
      SECRET_KEY=
      ALGORITHM=HS256
     ```

3. **Execute a Aplicação**:
   ```bash
   docker-compose up --build
   ```

: Letícia Vale