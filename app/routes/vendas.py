from app.models import models
from database.token import verify_token
from fastapi import APIRouter, HTTPException, status, Depends, Request, Form
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from database.database import get_db
from fastapi.responses import RedirectResponse, HTMLResponse
from datetime import datetime

router = APIRouter()

templates = Jinja2Templates(directory="templates")

# vendas
@router.get("/vendas", response_class=HTMLResponse)
async def vendas(request: Request, db: Session = Depends(get_db)):
    user = await verify_token(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    
    sales = db.query(models.Sale).all()
    return templates.TemplateResponse("vendas.html", {"request": request, "sales": sales})

@router.get("/vendas/adicionar", response_class=HTMLResponse)
async def add_sale_form(request: Request, db: Session = Depends(get_db)):
    user = await verify_token(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    
    clients = db.query(models.Client).all()
    medicines = db.query(models.Medicine).all()
    return templates.TemplateResponse(
        "adicionar_venda.html",
        {"request": request, "clients": clients, "medicines": medicines}
    )

@router.post("/vendas/adicionar", response_class=RedirectResponse)
async def add_sale(
    client_id: int = Form(...),
    medicine_id: int = Form(...),
    quantity: int = Form(...),
    db: Session = Depends(get_db),
    request: Request = None
):
    user = await verify_token(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    medicine = db.query(models.Medicine).filter(models.Medicine.id == medicine_id).first()
    
    if not client or not medicine:
        raise HTTPException(status_code=404, detail="Cliente ou medicamento não encontrado")

    if medicine.quantity < quantity:
        raise HTTPException(status_code=400, detail="Quantidade insuficiente em estoque")

    total_price = medicine.price * quantity

    new_sale = models.Sale(
        client_id=client_id,
        medicine_id=medicine_id,
        quantity=quantity,
        total_price=total_price
    )

    medicine.quantity -= quantity

    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)
    
    return RedirectResponse(url="/vendas", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/vendas/deletar/{sale_id}", response_class=HTMLResponse)
async def delete_sale_form(sale_id: int, request: Request, db: Session = Depends(get_db)):
    user = await verify_token(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    
    sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    
    return templates.TemplateResponse("deletar_venda.html", {"request": request, "sale": sale})

@router.post("/vendas/deletar/{sale_id}", response_class=RedirectResponse)
async def delete_sale(sale_id: int, db: Session = Depends(get_db), request: Request = None):
    user = await verify_token(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    
    sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    
    # Restaurar o estoque
    medicine = sale.medicine
    medicine.quantity += sale.quantity
    
    db.delete(sale)
    db.commit()
    
    return RedirectResponse(url="/vendas", status_code=status.HTTP_303_SEE_OTHER)
