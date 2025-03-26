from fastapi import FastAPI, Request, Depends, HTTPException, status, Form # Certifique-se de importar Depends aqui
from app.models import models
from database.database import engine, get_db
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from app.schemas import schemas  # Importar schemas corretamente


from app.routes.clientes import router as routerClients
from app.routes.medicamentos import router as routerMedicines
from app.routes.auth import router as routerAuth

# Criar as tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.include_router(routerClients)
app.include_router(routerMedicines)
app.include_router(routerAuth)


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})




