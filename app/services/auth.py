from datetime import datetime, timedelta

from fastapi import Cookie
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import ValidationError

from app.db.models import TokenData
from app.dependencies import DependencyContainer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=45)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, DependencyContainer.SETTINGS.secret_key, algorithm="HS256"
    )
    return encoded_jwt


def parse_token(access_token: str = Cookie(...)) -> TokenData:
    try:
        print(access_token)
        payload = jwt.decode(
            access_token, DependencyContainer.SETTINGS.secret_key, algorithms=["HS256"]
        )
        token_data = TokenData.parse_obj(payload)
        return token_data

    except (JWTError, ValidationError):
        raise Exception("Invalid token")
