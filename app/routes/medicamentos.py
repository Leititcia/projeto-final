from app.models import models
from database.token import verify_token
from fastapi import APIRouter, HTTPException, status, Depends, Request, Form
from sqlalchemy.orm import Session
from typing import List
from fastapi.templating import Jinja2Templates
from app.schemas import schemas
from database.database import get_db
from fastapi.responses import RedirectResponse, HTMLResponse

router = APIRouter()

templates = Jinja2Templates(directory="templates")

# medicamentos
@router.get("/medicamentos", response_class=HTMLResponse)
async def medicamentos(request: Request, db: Session = Depends(get_db)):
    user = await verify_token(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    medicines = db.query(models.Medicine).all()
    return templates.TemplateResponse("medicamentos.html", {"request": request, "medicines": medicines})

@router.get("/medicamentos/adicionar", response_class=HTMLResponse)
async def add_medicine_form(request: Request, db: Session = Depends(get_db)):
    user = await verify_token(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    return templates.TemplateResponse("adicionar_medicamento.html", {"request": request})

@router.post("/medicamentos/adicionar", response_class=RedirectResponse)
async def add_medicine(
    name: str = Form(...),
    price: float = Form(...),
    quantity: int = Form(...),
    db: Session = Depends(get_db),
    request: Request = None
):
    user = await verify_token(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    existing_medicine = db.query(models.Medicine).filter(models.Medicine.name == name).first()
    if existing_medicine:
        raise HTTPException(status_code=409, detail="Medicamento já cadastrado.")

    new_medicine = models.Medicine(name=name, price=price, quantity=quantity)
    db.add(new_medicine)
    db.commit()
    db.refresh(new_medicine)

    return RedirectResponse(url="/medicamentos", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/medicamentos/editar/{medicine_id}", response_class=HTMLResponse)
async def edit_medicine_form(medicine_id: int, request: Request, db: Session = Depends(get_db)):
    user = await verify_token(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    medicine = db.query(models.Medicine).filter(models.Medicine.id == medicine_id).first()
    if medicine is None:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado.")
    return templates.TemplateResponse("editar_medicamento.html", {"request": request, "medicine": medicine})

@router.post("/medicamentos/editar/{medicine_id}", response_class=RedirectResponse)
async def edit_medicine(
    medicine_id: int,
    name: str = Form(...),
    quantity: int = Form(...),
    price: float = Form(...),
    db: Session = Depends(get_db),
    request: Request = None
):
    user = await verify_token(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    existing_medicine = db.query(models.Medicine).filter(models.Medicine.id == medicine_id).first()
    if existing_medicine is None:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado.")
    
    existing_medicine.name = name
    existing_medicine.quantity = quantity
    existing_medicine.price = price
    db.commit()
    db.refresh(existing_medicine)
    
    return RedirectResponse(url="/medicamentos", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/medicamentos/deletar/{medicine_id}", response_class=HTMLResponse)
async def delete_medicine_form(medicine_id: int, request: Request, db: Session = Depends(get_db)):
    user = await verify_token(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    medicine = db.query(models.Medicine).filter(models.Medicine.id == medicine_id).first()
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado.")
    return templates.TemplateResponse("deletar_medicamento.html", {"request": request, "medicine": medicine})

@router.post("/medicamentos/deletar/{medicine_id}", response_class=RedirectResponse)
async def delete_medicine(medicine_id: int, db: Session = Depends(get_db), request: Request = None):
    user = await verify_token(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    medicine = db.query(models.Medicine).filter(models.Medicine.id == medicine_id).first()
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado.")
    db.delete(medicine)
    db.commit()
    return RedirectResponse("/medicamentos", status_code=303)
