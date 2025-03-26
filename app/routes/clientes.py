from app.models import models
from database.token import verify_token
from fastapi import APIRouter, HTTPException, status, Depends, Request, Form
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from typing import List
from app.schemas import schemas
from database.database import get_db
from fastapi.responses import RedirectResponse

router = APIRouter(dependencies=[Depends(verify_token)])

templates = Jinja2Templates(directory="templates")

# clientes
@router.get("/clientes")
async def clientes(request: Request, db: Session = Depends(get_db)):
    clients = db.query(models.Client).all()
    return templates.TemplateResponse("clientes.html", {"request": request, "clients": clients})

@router.get("/clientes/adicionar")
def add_client_form(request: Request):
    return templates.TemplateResponse("adicionar_cliente.html", {"request": request})

@router.post("/clientes/adicionar")
def add_client(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(None),
    db: Session = Depends(get_db)
):
    new_client = models.Client(name=name, email=email, phone=phone)
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return RedirectResponse(url="/clientes", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/clientes/editar/{client_id}")
def edit_client_form(client_id: int, request: Request, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    return templates.TemplateResponse("editar_cliente.html", {"request": request, "client": client})

@router.post("/clientes/editar/{client_id}")
def edit_client(client_id: int, name: str = Form(...), email: str = Form(...), phone: str = Form(None), db: Session = Depends(get_db)):
    existing_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if existing_client is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    
    existing_client.name = name
    existing_client.email = email
    if phone:
        existing_client.phone = phone
    
    db.commit()
    db.refresh(existing_client)
    return RedirectResponse(url="/clientes", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/clientes/deletar/{client_id}")
def delete_client_form(client_id: int, request: Request, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    return templates.TemplateResponse("deletar_cliente.html", {"request": request, "client": client})

@router.post("/clientes/deletar/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    
    db.delete(client)
    db.commit()
    return RedirectResponse(url="/clientes", status_code=status.HTTP_303_SEE_OTHER)
