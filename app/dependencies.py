import os
from pathlib import Path

from Crypto.Hash import SHA256
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from dotenv import load_dotenv

from app.db.schemas import Base
from app.services.password_reset import PasswordResetHandler
from app.services.pdf_gen_service import ReportGenerator
from app.settings import Settings

load_dotenv()


class DependencyContainer:
    BASE_PATH = None
    SETTINGS = None
    TEMPLATE_FOLDER_PATH = None
    SQLALCHEMY_DATABASE_URL = None
    ENGINE = None
    SESSION_LOCAL = None
    REPORT_GENERATOR = None
    PASSWORD_RESET_HANDLER = None

    @classmethod
    def initialize_container(cls):
        cls.BASE_PATH = Path(os.path.abspath(__file__)).parent.parent
        cls.SETTINGS = Settings(_secrets_dir=DependencyContainer.BASE_PATH)

        cls.TEMPLATE_FOLDER_PATH = os.path.join(cls.BASE_PATH, "templates")
        cls.SQLALCHEMY_DATABASE_URL = (
            "sqlite:///" + cls.BASE_PATH.__str__() + "/sql_app.db"
        )
        cls.ENGINE = create_engine(
            cls.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
        )
        cls.SESSION_LOCAL = sessionmaker(
            autocommit=False, autoflush=False, bind=cls.ENGINE
        )
        cls.REPORT_GENERATOR = ReportGenerator(
            cls.TEMPLATE_FOLDER_PATH,
            wkhtmltopdf_location=f"{cls.BASE_PATH}/non-pythonic-dependencies/wkhtmltopdf",
        )
        cls.PASSWORD_RESET_HANDLER = PasswordResetHandler(
            cls.SETTINGS.app_user,
            cls.SETTINGS.app_password,
            cls.SETTINGS.secret_key.encode("utf-8"),
        )
        cls.SHA256 = SHA256.new()

        with cls.ENGINE.connect() as conn:
            conn.execute(text("PRAGMA foreign_keys = ON"))

    @classmethod
    @contextmanager
    def get_db(cls):
        db = cls.SESSION_LOCAL()
        try:
            yield db
        finally:
            db.close()
