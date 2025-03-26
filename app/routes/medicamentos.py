from app.models import models
from database.token import verify_token
from fastapi import APIRouter, HTTPException, status, Depends, Request, Form
from sqlalchemy.orm import Session
from typing import List
from fastapi.templating import Jinja2Templates
from app.schemas import schemas
from database.database import get_db
from fastapi.responses import RedirectResponse

router = APIRouter(dependencies=[Depends(verify_token)])

templates = Jinja2Templates(directory="templates")

# medicamentos
@router.get("/medicamentos")
async def listar_medicamentos(request: Request, db: Session = Depends(get_db)):
    medicines = db.query(models.Medicine).all()
    return templates.TemplateResponse("medicamentos.html", {"request": request, "medicines": medicines})

@router.get("/medicamentos/adicionar")
def add_medicine_form(request: Request):
    return templates.TemplateResponse("adicionar_medicamento.html", {"request": request})

@router.post("/medicamentos/adicionar")
def add_medicine(
    name: str = Form(...), 
    quantity: int = Form(...), 
    price: float = Form(...), 
    db: Session = Depends(get_db)
):

    existing_medicine = db.query(models.Medicine).filter(models.Medicine.name == name).first()
    if existing_medicine:
        raise HTTPException(status_code=409, detail="Medicamento já cadastrado.")

    new_medicine = models.Medicine(name=name, quantity=quantity, price=price)
    db.add(new_medicine)
    db.commit()
    db.refresh(new_medicine)

    return RedirectResponse(url="/medicamentos", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/medicamentos/editar/{medicine_id}")
def edit_medicine_form(medicine_id: int, request: Request, db: Session = Depends(get_db)):
    medicine = db.query(models.Medicine).filter(models.Medicine.id == medicine_id).first()
    if medicine is None:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado.")
    return templates.TemplateResponse("editar_medicamento.html", {"request": request, "medicine": medicine})

@router.post("/medicamentos/editar/{medicine_id}")
def edit_medicine(
    medicine_id: int,
    name: str = Form(...),
    quantity: int = Form(...),
    price: float = Form(...),
    db: Session = Depends(get_db)
):

    existing_medicine = db.query(models.Medicine).filter(models.Medicine.id == medicine_id).first()
    if existing_medicine is None:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado.")
    
    existing_medicine.name = name
    existing_medicine.quantity = quantity
    existing_medicine.price = price
    db.commit()
    db.refresh(existing_medicine)
    
    return RedirectResponse(url="/medicamentos", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/medicamentos/deletar/{medicine_id}")
def delete_medicine_form(medicine_id: int, request: Request, db: Session = Depends(get_db)):
    medicine = db.query(models.Medicine).filter(models.Medicine.id == medicine_id).first()
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado.")
    return templates.TemplateResponse("deletar_medicamento.html", {"request": request, "medicine": medicine})

# Rota para realizar a deleção
@router.post("/medicamentos/deletar/{medicine_id}")
def delete_medicine(medicine_id: int, db: Session = Depends(get_db)):
    medicine = db.query(models.Medicine).filter(models.Medicine.id == medicine_id).first()
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado.")
    db.delete(medicine)
    db.commit()
    return RedirectResponse("/medicamentos", status_code=303)
