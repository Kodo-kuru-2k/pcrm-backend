from sqlalchemy.orm import Session

from app.db import schemas
from app.db.crud import UserCRUD, CenterOfExcellenceCRUD, ReportCRUD


class UserService:
    @staticmethod
    def fetch_user_by_email(db: Session, email: str):
        return UserCRUD.get_user_by_email(db, email)

    @staticmethod
    def fetch_reports_by_user(db: Session, user: schemas.User) -> list[schemas.Report]:
        list_of_coe = CenterOfExcellenceCRUD.get_coe_by_user_head(db, user.emp_id)
        reports = []
        for coe in list_of_coe:
            reports.extend(ReportCRUD.get_coe_reports(db, center_id=coe.center_id))
        return reports

    @staticmethod
    def update_report(db: Session, report: schemas.Report):
        ReportCRUD.update_report(db, report)

    @staticmethod
    def generate_pdf(db: Session, report_id: int):
        pass

    @staticmethod
    def reset_password_send_link(db: Session, user: schemas.Report):
        pass

    @staticmethod
    def reset_password_reset_with_link(db: Session, user: schemas.Report):
        pass


class PowerUserService(UserService):
    @staticmethod
    def fetch_user_by_employee_id(db: Session, emp_id: str):
        return UserCRUD.get_user_by_employee_id(db, emp_id)

    @staticmethod
    def fetch_all_users(db: Session):
        return UserCRUD.get_all_users(db)

    @staticmethod
    def fetch_coe_by_center_id(db: Session, center_id: str):
        return CenterOfExcellenceCRUD.get_coe_by_center_id(db, center_id)

    @staticmethod
    def fetch_coe_by_center_name(db: Session, center_name: str):
        return CenterOfExcellenceCRUD.get_coe_by_center_name(db, center_name)

    @staticmethod
    def fetch_all_coe(db: Session):
        return CenterOfExcellenceCRUD.get_all_coe(db)

    @staticmethod
    def fetch_report_by_report_id(db: Session, report_id: str):
        return ReportCRUD.get_report_by_report_id(db, report_id)

    @staticmethod
    def fetch_reports_by_due_date(db: Session, due_date: int):
        return ReportCRUD.get_reports_by_due_date(db, due_date=due_date)

    @staticmethod
    def fetch_all_reports(db: Session):
        return ReportCRUD.get_all_reports(db)

    '''create'''

    @staticmethod
    def add_new_coe(db: Session, coe: schemas.COE):
        CenterOfExcellenceCRUD.create_coe(db, coe)

    @staticmethod
    def add_new_report(db: Session, report: schemas.Report):
        ReportCRUD.create_report(db, report)

    '''modify'''

    @staticmethod
    def update_coe(db: Session, coe: schemas.COE):
        CenterOfExcellenceCRUD.update_coe(db, coe=coe)

    @staticmethod
    def update_report(db: Session, report: schemas.Report):
        ReportCRUD.update_report(db, report=report)

    '''delete'''

    @staticmethod
    def delete_coe(db: Session, center_id: str):
        CenterOfExcellenceCRUD.delete_coe_by_center_id(db, center_id=center_id)

    @staticmethod
    def delete_report(db: Session, report_id: int):
        ReportCRUD.delete_report_by_report_id(db, report_id=report_id)


class AdminService(PowerUserService):
    ''' create '''

    @staticmethod
    def add_new_user(db: Session, new_user: schemas.User):
        UserCRUD.create_user(db, new_user)

    ''' modify '''

    @staticmethod
    def update_user(db: Session, user: schemas.User):
        UserCRUD.update_user(db, user=user)

    ''' delete '''

    @staticmethod
    def delete_user_by_user_id(db: Session, emp_id: str):
        UserCRUD.delete_user_by_employee_id(db, emp_id=emp_id)
