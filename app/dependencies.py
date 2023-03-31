import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from app.services.pdf_gen_service import ReportGenerator


class DependencyContainer:
    BASE_PATH = ""
    TEMPLATE_FOLDER_PATH = "templates"
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
    ENGINE = None
    SESSION_LOCAL = None
    REPORT_GENERATOR = None

    @classmethod
    def initialize_container(cls):
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

    @classmethod
    @contextmanager
    def get_db(cls):
        db = cls.SESSION_LOCAL()
        try:
            yield db
        finally:
            db.close()
