from typing import List, Optional

from pydantic import BaseModel


class Hardware(BaseModel):
    sno: str
    description: str
    quantity: str


class Software(BaseModel):
    sno: str
    description: str
    quantity: str


class LaboratoryUse(BaseModel):
    MON: list
    TUE: list
    WED: list
    THU: list
    FRI: list
    SAT: list


class ResearchActivities(BaseModel):
    candidate_name: Optional[str] = None
    supervisor: Optional[str] = None


class ConsultancyActivities(BaseModel):
    sno: int
    client: str
    nature_of_work: str
    revenue_generated: str


class PDFModelDraft(BaseModel):
    hardware: Optional[List[Hardware]]
    software: Optional[List[Software]]

    other_features: Optional[str]
    name_and_designation_of_technical_staff: Optional[str]

    laboratory_use: Optional[LaboratoryUse]
    research_activities: Optional[Optional[ResearchActivities]]

    consultancy_activities: Optional[List[ConsultancyActivities]]

    total_number_of_courses_conducted: Optional[int]
    total_number_of_participants: Optional[int]
    revenue_generated: Optional[int]


class PDFModelFinal(BaseModel):
    hardware: List[Hardware]
    software: List[Software]

    other_features: str
    name_and_designation_of_technical_staff: str

    laboratory_use: LaboratoryUse
    research_activities: Optional[ResearchActivities]

    consultancy_activities: List[ConsultancyActivities]

    total_number_of_courses_conducted: int
    total_number_of_participants: int
    revenue_generated: int


class PDFModelWithCenterDetails(PDFModelFinal):
    establishment_date: int
    center_name: str
    purpose: str
    center_incharge: str
    sponsor: str
