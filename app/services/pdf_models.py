from typing import List, Optional

from pydantic import BaseModel


class Hardware(BaseModel):
    pass


class Software(BaseModel):
    pass


class LaboratoryUse(BaseModel):
    monday: list
    tuesday: list
    wednesday: list
    thursday: list
    friday: list
    saturday: list


class ResearchActivities(BaseModel):
    candidate_name: str
    supervisor: str


class ConsultancyActivities(BaseModel):
    sno: int
    client: str
    nature_of_work: str
    revenue_generated: str


class PDFModelDraft(BaseModel):
    ''' from db'''
    establishment_date: Optional[int]
    center_name: Optional[str]
    purpose: Optional[str]
    coe_head_name: Optional[str]
    sponsor: Optional[str]
    '''----'''

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
    ''' from db'''
    establishment_date: int
    center_name: str
    purpose: str
    coe_head_name: str
    sponsor: str
    '''----'''

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
