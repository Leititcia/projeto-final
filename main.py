from fastapi import FastAPI, Request, Depends, HTTPException, status, Form
from fastapi.staticfiles import StaticFiles
from app.models import models
from database.database import engine, get_db
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from app.schemas import schemas

from app.routes.clientes import router as routerClients
from app.routes.medicamentos import router as routerMedicines
from app.routes.auth import router as routerAuth
from app.routes.home import router as routerHome
from app.routes.vendas import router as routerSales

# Criar as tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app = FastAPI()

# Montar arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(routerClients)
app.include_router(routerMedicines)
app.include_router(routerAuth)
app.include_router(routerHome)
app.include_router(routerSales)

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})