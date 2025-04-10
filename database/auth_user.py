from datetime import datetime, timedelta
from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from jose import jwt, JWTError
import os
from dotenv import load_dotenv
from app.models.models import UserModel
from app.schemas.schemas import UserSchema

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
crypt_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

class UserUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def user_register(self, user: UserSchema):
        user_model = UserModel(
            username=user.username,
            password=crypt_context.hash(user.password)
        )
        try:
            self.db_session.add(user_model)
            self.db_session.flush()
            self.db_session.commit()
        except IntegrityError:

            self.db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User already exists'
            )

    def user_login(self, user: UserSchema, expires_in: int = 30):
        user_on_db = self.db_session.query(UserModel).filter_by(username=user.username).first()

        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid username or password'
            )
        
        if not crypt_context.verify(user.password, user_on_db.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid username or password'
            )
        

        exp = datetime.utcnow() + timedelta(minutes=expires_in)
        
        payload = {
            'sub': user.username, 
            'exp': exp 
        }

        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {
            'access_token': access_token,
            'exp': exp.isoformat()
        }

    def verify_token(self, access_token: str): 
        try:
            data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid access token'
            )

        user_on_db = self.db_session.query(UserModel).filter_by(username=data['sub']).first()

        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid access token'
            )
