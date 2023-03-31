import tempfile
from typing import Annotated

from fastapi import APIRouter, Depends, status, Response
from starlette.responses import StreamingResponse

from app.db.models import ReportModel, ReportUpdateModel
from app.dependencies import DependencyContainer
from app.services.user_services import UserService

router = APIRouter()


@router.get("/users/pending_reports", tags=["users"])
async def get_pending_reports(
    emp_id: str,
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
) -> list[ReportModel]:
    with dependency_container.get_db() as db:
        reports = UserService.fetch_pending_reports_by_user(db, emp_id)

    return reports


@router.get("/users/submitted_reports", tags=["users"])
async def get_submitted_reports(
    emp_id: str,
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
) -> list[ReportModel]:
    with dependency_container.get_db() as db:
        reports = UserService.fetch_submitted_reports_by_user(db, emp_id)

    return reports


@router.get("/users/generate-report", tags=["users"])
async def generate_report(
    report_id: int,
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
):
    with dependency_container.get_db() as db:
        with tempfile.NamedTemporaryFile(suffix=".pdf") as temp:
            report_generator = dependency_container.REPORT_GENERATOR
            file_contents = UserService.generate_pdf(
                db, report_id, report_generator=report_generator, file_name=temp.name
            )
            headers = {
                "Content-Disposition": "attachment; filename=report.pdf",
                "Content-Type": "application/pdf",
            }
            print(file_contents)
            response = StreamingResponse(
                content=file_contents, status_code=status.HTTP_200_OK, headers=headers
            )
            return response


@router.patch("/users/update-report", tags=["users"])
async def update_report(
    report: ReportUpdateModel,
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
):
    with dependency_container.get_db() as db:
        UserService.update_report(db, report=report)
