from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Cookie, Depends
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import ValidationError

from app.db.models import TokenData
from app.dependencies import DependencyContainer
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=45)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, DependencyContainer.SETTINGS.secret_key, algorithm="HS256"
    )
    return encoded_jwt


def parse_token(access_token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
    try:
        print(access_token)
        payload = jwt.decode(
            access_token, DependencyContainer.SETTINGS.secret_key, algorithms=["HS256"]
        )
        token_data = TokenData.parse_obj(payload)
        return token_data

    except (JWTError, ValidationError):
        raise Exception("Invalid token")
