import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from dotenv import load_dotenv

from app.services.password_reset import PasswordResetHandler
from app.services.pdf_gen_service import ReportGenerator

load_dotenv()


class DependencyContainer:
    USER = None
    APP_PASSWORD = None
    SECRET_KEY = None
    BASE_PATH = None
    TEMPLATE_FOLDER_PATH = None
    SQLALCHEMY_DATABASE_URL = None
    ENGINE = None
    SESSION_LOCAL = None
    REPORT_GENERATOR = None
    PASSWORD_RESET_HANDLER = None

    @classmethod
    def initialize_container(cls):
        cls.APP_USER = os.environ.get("APP_USER")
        cls.APP_PASSWORD = os.environ.get("PASSWORD")
        cls.SECRET_KEY = f"{os.environ.get('SECRET_KEY')}=="

        cls.BASE_PATH = Path(os.path.abspath(__file__)).parent.parent
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
        cls.REPORT_GENERATOR = ReportGenerator(cls.TEMPLATE_FOLDER_PATH)
        cls.PASSWORD_RESET_HANDLER = PasswordResetHandler(
            cls.APP_USER, cls.APP_PASSWORD, cls.SECRET_KEY.encode("utf-8")
        )

    @classmethod
    @contextmanager
    def get_db(cls):
        db = cls.SESSION_LOCAL()
        try:
            yield db
        finally:
            db.close()
