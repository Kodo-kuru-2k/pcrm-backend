import enum

from pydantic import BaseModel


class UserLevels(enum.Enum):
    Admin = 'Admin'
    User = 'User'
    PowerUser = 'PowerUser'


class ReportStatus(enum.Enum):
    Draft = 'Draft'
    Submitted = 'Submitted'


class User(BaseModel):
    emp_id: str
    name: str
    email: str
    password: str
    is_active: bool = True
    permissions: UserLevels

    class Config:
        orm_mode = True


class COE(BaseModel):
    center_id: str
    center_name: str
    establishment_date: int
    name_and_purpose: str
    sponsor: str
    department_name: str

    department_head: str

    class Config:
        orm_mode = True


class Report(BaseModel):
    report_id: int
    report_status: ReportStatus
    report: str
    submission_date: int
    due_date: int

    center_id: int

    class Config:
        orm_mode = True
