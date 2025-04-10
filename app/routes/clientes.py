from app.models import models
from database.token import verify_token
from fastapi import APIRouter, HTTPException, status, Depends, Request, Form
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from typing import List
from app.schemas import schemas
from database.database import get_db
from fastapi.responses import RedirectResponse, HTMLResponse
from app.utils.validators import validate_phone, format_phone

router = APIRouter()

templates = Jinja2Templates(directory="templates")

# clientes
@router.get("/clientes", response_class=HTMLResponse)
async def clientes(request: Request, db: Session = Depends(get_db)):
    user = await verify_token(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    clients = db.query(models.Client).all()
    return templates.TemplateResponse("clientes.html", {"request": request, "clients": clients})

@router.get("/clientes/adicionar", response_class=HTMLResponse)
async def add_client_form(request: Request, db: Session = Depends(get_db)):
    user = await verify_token(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    return templates.TemplateResponse("adicionar_cliente.html", {"request": request})

@router.post("/clientes/adicionar", response_class=RedirectResponse)
async def add_client(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(None),
    db: Session = Depends(get_db),
    request: Request = None
):
    user = await verify_token(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
    # Valida telefone
    if phone and not validate_phone(phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Número de telefone inválido. Use o formato (XX) XXXXX-XXXX"
        )

    formatted_phone = format_phone(phone) if phone else None
    
    new_client = models.Client(name=name, email=email, phone=formatted_phone)
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return RedirectResponse(url="/clientes", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/clientes/editar/{client_id}", response_class=HTMLResponse)
async def edit_client_form(client_id: int, request: Request, db: Session = Depends(get_db)):
    user = await verify_token(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    return templates.TemplateResponse("editar_cliente.html", {"request": request, "client": client})

@router.post("/clientes/editar/{client_id}", response_class=RedirectResponse)
async def edit_client(
    client_id: int,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(None),
    db: Session = Depends(get_db),
    request: Request = None
):
    user = await verify_token(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
    # Valida telefone
    if phone and not validate_phone(phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Número de telefone inválido. Use o formato (XX) XXXXX-XXXX"
        )

    formatted_phone = format_phone(phone) if phone else None
    
    existing_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if existing_client is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    
    existing_client.name = name
    existing_client.email = email
    existing_client.phone = formatted_phone
    
    db.commit()
    db.refresh(existing_client)
    return RedirectResponse(url="/clientes", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/clientes/deletar/{client_id}", response_class=HTMLResponse)
async def delete_client_form(client_id: int, request: Request, db: Session = Depends(get_db)):
    user = await verify_token(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    return templates.TemplateResponse("deletar_cliente.html", {"request": request, "client": client})

@router.post("/clientes/deletar/{client_id}", response_class=RedirectResponse)
async def delete_client(client_id: int, db: Session = Depends(get_db), request: Request = None):
    user = await verify_token(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    
    db.delete(client)
    db.commit()
    return RedirectResponse(url="/clientes", status_code=status.HTTP_303_SEE_OTHER)
