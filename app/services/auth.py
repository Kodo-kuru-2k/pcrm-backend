from datetime import datetime, timedelta

from fastapi import Cookie
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import ValidationError

from app.db.models import TokenData
from app.dependencies import DependencyContainer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=45)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")
    return encoded_jwt


def parse_token(access_token: str = Cookie(...)) -> TokenData:
    try:
        print(access_token)
        payload = jwt.decode(access_token, secret_key, algorithms=["HS256"])
        token_data = TokenData.parse_obj(payload)
        return token_data

    except (JWTError, ValidationError):
        raise Exception("Invalid token")


if __name__ == "__main__":
    DependencyContainer.initialize_container()
    access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbXBfaWQiOiJ1c2VyMTIzIiwibmFtZSI6InNvbWVvbmUiLCJlbWFpbCI6IjE5cHQyOEBwc2d0ZWNoLmFjLmluIiwiaXNfYWN0aXZlIjp0cnVlLCJwZXJtaXNzaW9ucyI6IlVzZXIiLCJleHAiOjE2ODA0MjI2NDh9.HfxKvnlghhKSYODc12eXH3nONHinbp38_AWWqukhH64"
    print(
        jwt.decode(access_token, DependencyContainer.SECRET_KEY, algorithms=["HS256"])
    )
