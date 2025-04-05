from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from app.models.models import UserModel
from database.auth_user import ALGORITHM, SECRET_KEY
from sqlalchemy.orm import Session
from database.database import get_db
from jose import jwt, JWTError
from datetime import datetime, timedelta

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/login')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def verify_token(request: Request, db: Session):
    try:
        print("Iniciando verificação do token...") 
        
        token = request.cookies.get("access_token")
        print(f"Token encontrado no cookie: {'Sim' if token else 'Não'}")
        
        if not token:
            print("Token não encontrado") 
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token não fornecido")
        
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            print(f"Token decodificado com sucesso para o usuário: {username}")
        except JWTError as e:
            print(f"Erro ao decodificar o token: {str(e)}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado")
        
        if not username:
            print("Username não encontrado no token")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        
        user = db.query(UserModel).filter(UserModel.username == username).first()
        if not user:
            print("Usuário não encontrado no banco")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")
        
        return user
    except Exception as e:
        print(f"Erro na verificação do token: {str(e)}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado")
