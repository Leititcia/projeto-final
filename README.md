# Interface Gráfica Farmácia API

A interface da FármaciaAPI foi projetada utilizando Jinja2 para renderização de templates HTML dinâmicos.

- O sistema utiliza Bootstrap para responsividade.

- Layout minimalista e intuitivo.

- Botões destacados para operações CRUD.

---

## Telas do Sistema

### **Tela Principal**
<p align="center">
  <img src="https://github.com/user-attachments/assets/c8fe0af5-8721-4e0c-8c59-05442c80b07a" width="70%" alt="Tela Principal">
</p>

---

<div style="display: flex; justify-content: center; gap: 20px;">

### Gerenciamento de Clientes
  <div style="text-align: center; width: 50%;">
    <img src="https://github.com/user-attachments/assets/6db0a6f9-1446-4004-b799-4d5c4996ccdb" width="100%" alt="Lista de Medicamentos">
  </div>

### Gerenciamento de Medicamentos
  <div style="text-align: center; width: 50%;">
    <img src="https://github.com/user-attachments/assets/6a448e05-8796-40b7-af90-1813bd20d510" width="100%" alt="Cadastro de Medicamentos">
  </div>

</div>

---

## Tecnologias Utilizadas

- **FastAPI**: Framework para construção de APIs em Python.
- **Pydantic**: Biblioteca de validação de dados e criação de modelos.
- **Python10**: Linguagem utilizada para o desenvolvimento da aplicação.
- **SQLAlchemy**: ORM para interação com o banco de dados.
- **Jinja2**: Template engine para renderização dinâmica das páginas HTML.
- **Bootstrap**: Framework CSS para responsividade.

---

## Como Clonar

1. **Clone o Repositório**:
   - No terminal, execute o comando abaixo para clonar a branch específica do projeto:   
   ```
   git clone --branch jinja2 https://github.com/Leititcia/farmaAPI.git
   ```

2. **Crie e Ative um Ambiente Virtual**:
   - Com o diretório do projeto aberto crie o ambiente virtual com o comando abaixo:
    ```bash
      python -m venv venv
     ```
      - Para ativar
          - No windows:
            ```bash
              venv\Scripts\activate
             ```
          - No Linux/macOS:
            ```bash
              source venv/bin/activate
             ```

4. **Instale as Dependências**:
    ```bash
    pip install -r requirements.txt
    ```
     
5. **Execute a API**:
     ```bash
     uvicorn app.main:app --reload
     ```

---

## Autora
Letícia Vale.
