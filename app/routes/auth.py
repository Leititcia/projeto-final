from fastapi import APIRouter, HTTPException, status, Depends, Request, Form
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from app.schemas import schemas
from database.database import get_db
from fastapi.responses import RedirectResponse, HTMLResponse
from database.token import verify_token, create_access_token
from database.auth_user import UserUseCases
from app.models import models
from passlib.context import CryptContext
from urllib.parse import quote

router = APIRouter()

templates = Jinja2Templates(directory="templates")
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login", response_class=RedirectResponse)
async def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.UserModel).filter(models.UserModel.username == username).first()
    if not user or not pwd_context.verify(password, user.password):
        error_message = "Usuário ou senha incorretos"
        return RedirectResponse(
            url=f"/login?error={quote(error_message)}", 
            status_code=status.HTTP_303_SEE_OTHER
        )
    
    access_token = create_access_token(data={"sub": user.username})
    response = RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

@router.get("/registro", response_class=HTMLResponse)
async def registro_page(request: Request):
    return templates.TemplateResponse("registro.html", {"request": request})

@router.post("/registro", response_class=RedirectResponse)
async def registro(
    nome_usuario: str = Form(...),
    senha: str = Form(...),
    confirmar_senha: str = Form(...),
    db: Session = Depends(get_db)
):
    if senha != confirmar_senha:
        error_message = "As senhas não coincidem"
        return RedirectResponse(
            url=f"/registro?error={quote(error_message)}", 
            status_code=status.HTTP_303_SEE_OTHER
        )
    
    if db.query(models.UserModel).filter(models.UserModel.username == nome_usuario).first():
        error_message = "Nome de usuário já existe"
        return RedirectResponse(
            url=f"/registro?error={quote(error_message)}", 
            status_code=status.HTTP_303_SEE_OTHER
        )
    
    hashed_password = pwd_context.hash(senha)
    new_user = models.UserModel(username=nome_usuario, password=hashed_password)
    db.add(new_user)
    db.commit()
    
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/logout", response_class=RedirectResponse)
async def logout():
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="access_token")
    return response