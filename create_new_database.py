import os

from sqlalchemy import text

from app.db.models import UserLevels
from app.db.schemas import Base, UserSchema
from app.dependencies import DependencyContainer
from app.services.password_hash import PasswordHash


def create_database(dependency_container: DependencyContainer, base: Base):
    if not os.path.isfile(f"{dependency_container.BASE_PATH}/sql_app.db"):
        base.metadata.create_all(dependency_container.ENGINE)
        print("database created")


def enforce_foreign_key_integrity(dependency_container: DependencyContainer):
    with dependency_container.ENGINE.connect() as conn:
        conn.execute(text("PRAGMA foreign_keys = ON"))
        print("foreign key constraint added")


def add_new_admin(dependency_container: DependencyContainer):
    with dependency_container.get_db() as db:
        db_user = UserSchema(
            emp_id="1",
            name="admin",
            email="ecampus@psgtech.ac.in",
            password=PasswordHash.hash_password("password123"),
            permissions=UserLevels.Admin,
        )
        db.add(db_user)
        db.commit()
    print("added admin")


if __name__ == "__main__":
    DependencyContainer.initialize_container()
    create_database(dependency_container=DependencyContainer(), base=Base)
    enforce_foreign_key_integrity(dependency_container=DependencyContainer())
    add_new_admin(dependency_container=DependencyContainer())
    print("Done")
