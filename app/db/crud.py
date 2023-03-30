from typing import List

from sqlalchemy.orm import Session

from app.db import models, schemas


class UserCRUD:
    @staticmethod
    def get_user_by_employee_id(db: Session, emp_id: str) -> schemas.User:
        return schemas.User.from_orm(db.query(models.User).filter(models.User.emp_id == emp_id).first())

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> schemas.User:
        return schemas.User.from_orm(db.query(models.User).filter(models.User.email == email).first())

    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100):
        all_users = db.query(models.User).offset(skip).limit(limit).all()
        return [
            schemas.User.from_orm(user) for user in all_users
        ]

    @staticmethod
    def create_user(db: Session, user: schemas.User):
        db_user = models.User(
            emp_id=user.emp_id,
            name=user.name,
            email=user.email,
            password=user.password,
            permissions=user.permissions
        )
        db.add(db_user)
        db.commit()

    @staticmethod
    def delete_user_by_employee_id(db: Session, emp_id: str):
        db.query(models.User).filter(models.User.emp_id == emp_id).first().delete()
        db.commit()

    @staticmethod
    def delete_user_by_email(db: Session, email: str):
        db.query(models.User).filter(models.User.email == email).first().delete()
        db.commit()


class CenterOfExcellenceCRUD:
    @staticmethod
    def get_coe_by_center_id(db: Session, center_id: str) -> schemas.COE:
        return schemas.COE.from_orm(db.query(models.COE).filter(models.COE.center_id == center_id).first())

    @staticmethod
    def get_user_by_center_name(db: Session, center_name: str) -> schemas.COE:
        return schemas.COE.from_orm(db.query(models.COE).filter(models.COE.center_name == center_name).first())

    @staticmethod
    def get_all_coe(db: Session, skip: int = 0, limit: int = 10000):
        all_coe = db.query(models.COE).offset(skip).limit(limit).all()
        return [
            schemas.COE.from_orm(coe) for coe in all_coe
        ]

    @staticmethod
    def create_coe(db: Session, coe: schemas.COE):
        db_coe = models.COE(
            center_id=coe.center_id,
            center_name=coe.center_name,
            establishment_date=coe.establishment_date,
            name_and_purpose=coe.name_and_purpose,
            sponsor=coe.sponsor,
            department_name=coe.department_name,
            department_head=coe.department_head,
        )
        db.add(db_coe)
        db.commit()

    @staticmethod
    def delete_coe_by_center_id(db: Session, center_id: str):
        db.query(models.COE).filter(models.COE.center_id == center_id).first().delete()
        db.commit()

    @staticmethod
    def delete_user_by_center_name(db: Session, center_name: str):
        db.query(models.COE).filter(models.COE.center_name == center_name).first().delete()
        db.commit()


class ReportCRUD:
    @staticmethod
    def get_report_by_report_id(db: Session, report_id: str) -> schemas.Report:
        return schemas.Report.from_orm(db.query(models.Report).filter(models.Report.report_id == report_id).first())

    @staticmethod
    def get_reports_by_due_date(db: Session, due_date: int) -> List[schemas.Report]:
        all_reports = db.query(models.Report).filter(models.Report.due_date <= due_date)
        return [
            schemas.Report.from_orm(report) for report in all_reports
        ]

    @staticmethod
    def get_all_reports(db: Session, skip: int = 0, limit: int = 10000):
        all_reports = db.query(models.Report).offset(skip).limit(limit).all()
        return [
            schemas.Report.from_orm(report) for report in all_reports
        ]

    @staticmethod
    def create_report(db: Session, report: schemas.Report):
        db_report = models.Report(
            report_id=report.report_id,
            report_status=report.report_status,
            report=report.report,
            submission_date=report.submission_date,
            due_date=report.due_date,
            center_id=report.center_id
        )
        db.add(db_report)
        db.commit()

    @staticmethod
    def delete_report_by_report_id(db: Session, report_id: int):
        db.query(models.COE).filter(models.Report.report_id == report_id).first().delete()
        db.commit()
