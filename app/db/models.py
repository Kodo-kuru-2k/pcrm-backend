import enum
from typing import Optional, Union

from pydantic import BaseModel

from app.services.pdf_models import PDFModelFinal, PDFModelDraft


class UserLevels(enum.Enum):
    Admin = "Admin"
    User = "User"
    PowerUser = "PowerUser"


class ReportStatus(enum.Enum):
    Draft = "Draft"
    Submitted = "Submitted"


class UserModel(BaseModel):
    emp_id: str
    name: str
    email: str
    password: str
    is_active: bool = True
    permissions: UserLevels

    class Config:
        orm_mode = True


class COEModel(BaseModel):
    center_id: str
    center_name: str
    establishment_date: int
    purpose: str
    sponsor: str
    department_name: str

    center_incharge: str

    class Config:
        orm_mode = True


class ReportModel(BaseModel):
    report_id: Optional[int]
    report_status: ReportStatus
    report: str
    submission_date: Optional[int]
    due_date: int

    center_id: str

    class Config:
        orm_mode = True


class ReportUpdateModel(BaseModel):
    report_id: int
    report: Union[PDFModelFinal, PDFModelDraft]
    report_status: ReportStatus
