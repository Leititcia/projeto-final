from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.database import get_db
from app.models import models
from sqlalchemy import func
from database.token import verify_token
from fastapi.responses import HTMLResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/home", response_class=HTMLResponse)
async def home_page(request: Request, db: Session = Depends(get_db)):
    user = await verify_token(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    
    try:
        # resumo total
        total_clientes = db.query(func.count()).select_from(models.Client).scalar()
        total_medicamentos = db.query(func.count()).select_from(models.Medicine).scalar()
        total_vendas = db.query(func.count()).select_from(models.Sale).scalar()
        
        return templates.TemplateResponse(
            "home.html",
            {
                "request": request,
                "user": user,
                "total_clientes": total_clientes,
                "total_medicamentos": total_medicamentos,
                "total_vendas": total_vendas
            }
        )
    except Exception as e:
        print(f"Erro ao buscar dados da home: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao carregar dados da página inicial")