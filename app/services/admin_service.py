from sqlalchemy.orm import Session

from app.db import schemas
from app.db.crud import UserCRUD


class AdminService:
    @staticmethod
    def add_new_user(db: Session, new_user: schemas.User):
        UserCRUD.create_user(db, new_user)

