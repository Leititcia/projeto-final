from app.models import models
from app.routes.utils import getPagination
from database.token import verify_token
from fastapi import APIRouter, HTTPException, status, Depends, Request, Form
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from database.database import get_db
from fastapi.responses import RedirectResponse, HTMLResponse
import json
from sqlalchemy import or_, cast
from sqlalchemy.types import String

router = APIRouter()

templates = Jinja2Templates(directory="templates")

# vendas
@router.get("/vendas", response_class=HTMLResponse)
async def vendas(request: Request, search: str = "", db: Session = Depends(get_db)):
    user = await verify_token(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    
    # criando query
    query = db.query(models.Order).join(models.Order.client).order_by(models.Order.order_date.desc())


    # aplicando filtro de pesquisa na query
    if(search):
        query = query.filter(
            or_(
                models.Client.name.ilike(f"%{search}%"),
                cast(models.Order.id, String).ilike(f"%{search}%"),
            )
        )

    # passando a query para a funcao que pega os dados e a paginacao
    orders, pagination = getPagination(query, request)

    return templates.TemplateResponse("vendas.html", {"request": request, "pagination": pagination, "orders": orders})

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
    cart_items: str = Form(...),
    db: Session = Depends(get_db),
    request: Request = None
):
    user = await verify_token(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Processar itens do carrinho
    try:
        cart_items_list = json.loads(cart_items)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Formato de carrinho inválido")
    
    if not cart_items_list:
        raise HTTPException(status_code=400, detail="Carrinho vazio")
    
    # Calcular o preço total do pedido
    total_order_price = 0
    
    # Criar um novo pedido
    new_order = models.Order(
        client_id=client_id,
        total_price=0  # Será atualizado após processar todos os itens
    )
    
    db.add(new_order)
    db.flush()  # Para obter o ID do pedido
    
    # Criar itens do pedido para cada item do carrinho
    for item in cart_items_list:
        medicine_id = item.get('id')
        quantity = item.get('quantity')
        price = item.get('price')
        
        if not medicine_id or not quantity or not price:
            raise HTTPException(status_code=400, detail="Dados do item inválidos")
        
        medicine = db.query(models.Medicine).filter(models.Medicine.id == medicine_id).first()
        if not medicine:
            raise HTTPException(status_code=404, detail=f"Medicamento com ID {medicine_id} não encontrado")
        
        if medicine.quantity < quantity:
            raise HTTPException(
                status_code=400, 
                detail=f"Quantidade insuficiente em estoque para o medicamento {medicine.name}"
            )
        
        item_total_price = price * quantity
        total_order_price += item_total_price
        
        # Criar item do pedido
        order_item = models.OrderItem(
            order_id=new_order.id,
            medicine_id=medicine_id,
            quantity=quantity,
            price=price
        )
        
        # Atualizar estoque
        medicine.quantity -= quantity
        
        db.add(order_item)
    
    # Atualizar o preço total do pedido
    new_order.total_price = total_order_price
    
    db.commit()
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
