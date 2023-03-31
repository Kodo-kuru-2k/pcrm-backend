import datetime
import json
from typing import List

from sqlalchemy.orm import Session

from app.db.models import (
    ReportStatus,
    UserModel,
    ReportModel,
    COEModel,
    ReportUpdateModel,
)
from app.db.schemas import UserSchema, ReportSchema, COESchema


class UserCRUD:
    @staticmethod
    def get_user_by_employee_id(db: Session, emp_id: str) -> UserModel:
        return UserModel.from_orm(
            db.query(UserSchema).filter(UserSchema.emp_id == emp_id).first()
        )

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> UserModel:
        return UserModel.from_orm(
            db.query(UserSchema).filter(UserSchema.email == email).first()
        )

    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[UserModel]:
        all_users = db.query(UserSchema).offset(skip).limit(limit).all()
        return [UserModel.from_orm(user) for user in all_users]

    @staticmethod
    def create_user(db: Session, user: UserModel) -> None:
        db_user = UserSchema(
            emp_id=user.emp_id,
            name=user.name,
            email=user.email,
            password=user.password,
            permissions=user.permissions,
        )
        db.add(db_user)
        db.commit()

    @staticmethod
    def update_user(db: Session, user: UserModel) -> None:
        existing_user = (
            db.query(UserSchema).filter(UserSchema.emp_id == user.emp_id).first()
        )
        existing_user.emp_id = user.emp_id
        existing_user.name = user.name
        existing_user.email = user.email
        existing_user.password = user.password
        existing_user.is_active = user.is_active
        existing_user.permissions = user.permissions
        db.commit()

    @staticmethod
    def delete_user_by_employee_id(db: Session, emp_id: str) -> None:
        db.query(UserSchema).filter(UserSchema.emp_id == emp_id).first().delete()
        db.commit()

    @staticmethod
    def delete_user_by_email(db: Session, email: str) -> None:
        db.query(UserSchema).filter(UserSchema.email == email).first().delete()
        db.commit()


class CenterOfExcellenceCRUD:
    @staticmethod
    def get_coe_by_center_id(db: Session, center_id: str) -> COEModel:
        return COEModel.from_orm(
            db.query(COESchema).filter(COESchema.center_id == center_id).first()
        )

    @staticmethod
    def get_coe_by_user_head(db: Session, emp_id: str) -> List[COEModel]:
        all_coe = db.query(COESchema).filter(COESchema.department_head == emp_id)
        return [COEModel.from_orm(coe) for coe in all_coe]

    @staticmethod
    def get_coe_by_center_name(db: Session, center_name: str) -> COEModel:
        return COEModel.from_orm(
            db.query(COESchema).filter(COESchema.center_name == center_name).first()
        )

    @staticmethod
    def get_all_coe(db: Session, skip: int = 0, limit: int = 10000) -> List[COEModel]:
        all_coe = db.query(COESchema).offset(skip).limit(limit).all()
        return [COEModel.from_orm(coe) for coe in all_coe]

    @staticmethod
    def create_coe(db: Session, coe: COEModel) -> None:
        db_coe = COESchema(
            center_id=coe.center_id,
            center_name=coe.center_name,
            establishment_date=coe.establishment_date,
            purpose=coe.purpose,
            sponsor=coe.sponsor,
            department_name=coe.department_name,
            department_head=coe.department_head,
        )
        db.add(db_coe)
        db.commit()

    @staticmethod
    def update_coe(db: Session, coe: COEModel) -> None:
        existing_coe = (
            db.query(COESchema).filter(COESchema.center_id == coe.center_id).first()
        )
        existing_coe.center_id = coe.center_id
        existing_coe.center_name = coe.center_name
        existing_coe.establishment_date = coe.establishment_date
        existing_coe.purpose = coe.purpose
        existing_coe.sponsor = coe.sponsor
        existing_coe.department_name = coe.department_name
        existing_coe.department_head = coe.department_head
        db.commit()

    @staticmethod
    def delete_coe_by_center_id(db: Session, center_id: str) -> None:
        db.query(COESchema).filter(COESchema.center_id == center_id).first().delete()
        db.commit()

    @staticmethod
    def delete_user_by_center_name(db: Session, center_name: str) -> None:
        db.query(COESchema).filter(
            COESchema.center_name == center_name
        ).first().delete()
        db.commit()


class ReportCRUD:
    @staticmethod
    def get_report_by_report_id(db: Session, report_id: int) -> ReportModel:
        return ReportModel.from_orm(
            db.query(ReportSchema).filter(ReportSchema.report_id == report_id).first()
        )

    @staticmethod
    def get_coe_pending_reports(db: Session, center_id: str) -> List[ReportModel]:
        user_reports = db.query(ReportSchema).filter(
            ReportSchema.center_id == center_id
            and ReportSchema.report_status == ReportStatus.Draft
        )
        return [
            ReportModel.from_orm(report)
            for report in user_reports
            if report.report_status == ReportStatus.Draft
        ]

    @staticmethod
    def get_coe_submitted_reports(db: Session, center_id: str) -> List[ReportModel]:
        user_reports = db.query(ReportSchema).filter(
            ReportSchema.center_id == center_id
            and ReportSchema.report_status == ReportStatus.Submitted
        )
        return [
            ReportModel.from_orm(report)
            for report in user_reports
            if report.report_status == ReportStatus.Submitted
        ]

    @staticmethod
    def get_all_coe_reports(db: Session, center_id: str) -> List[ReportModel]:
        user_reports = db.query(ReportSchema).filter(
            ReportSchema.center_id == center_id
        )
        return [ReportModel.from_orm(report) for report in user_reports]

    @staticmethod
    def get_reports_by_due_date(db: Session, due_date: int) -> List[ReportModel]:
        all_reports = db.query(ReportSchema).filter(ReportSchema.due_date <= due_date)
        return [ReportModel.from_orm(report) for report in all_reports]

    @staticmethod
    def get_all_reports(
        db: Session, skip: int = 0, limit: int = 10000
    ) -> List[ReportModel]:
        all_reports = db.query(ReportSchema).offset(skip).limit(limit).all()
        return [ReportModel.from_orm(report) for report in all_reports]

    @staticmethod
    def create_report(db: Session, report: ReportModel) -> None:
        db_report = ReportSchema(
            report_status=report.report_status,
            report=report.report,
            submission_date=report.submission_date,
            due_date=report.due_date,
            center_id=report.center_id,
        )
        db.add(db_report)
        db.commit()

    @staticmethod
    def update_report(db: Session, report: ReportUpdateModel) -> None:
        existing_report = (
            db.query(ReportSchema)
            .filter(ReportSchema.report_id == report.report_id)
            .first()
        )
        existing_report.report_status = report.report_status
        existing_report.report = report.report.json()
        existing_report.submission_date = datetime.datetime.now().timestamp()
        db.commit()

    @staticmethod
    def update_all_report_metadata(db: Session, report: ReportModel) -> None:
        existing_report = (
            db.query(ReportSchema)
            .filter(ReportSchema.report_id == report.report_id)
            .first()
        )
        existing_report.report_status = report.report_status
        existing_report.report = report.report
        existing_report.submission_date = report.submission_date
        existing_report.due_date = report.due_date
        existing_report.center_id = report.center_id
        db.commit()

    @staticmethod
    def delete_report_by_report_id(db: Session, report_id: int) -> None:
        db.query(ReportSchema).filter(
            ReportSchema.report_id == report_id
        ).first().delete()
        db.commit()
