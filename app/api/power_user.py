import tempfile
from typing import Annotated

from fastapi import APIRouter, Depends, status, Response
from starlette.responses import StreamingResponse

from app.db.models import ReportModel, ReportUpdateModel
from app.dependencies import DependencyContainer
from app.services.user_services import UserService, PowerUserService

router = APIRouter()


@router.get("/power-user/all-users", tags=["power_user"])
async def get_all_user(
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
) -> list[ReportModel]:
    with dependency_container.get_db() as db:
        reports = PowerUserService.fetch_all_users(db)

    return reports


@router.get("/power-user/all-coe", tags=["power_user"])
async def get_all_coe(
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
) -> list[ReportModel]:
    with dependency_container.get_db() as db:
        reports = PowerUserService.fetch_all_coe(db)

    return reports


@router.get("/power-user/all-reports", tags=["power_user"])
async def get_all_reports(
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
) -> list[ReportModel]:
    with dependency_container.get_db() as db:
        reports = PowerUserService.fetch_all_reports(db)

    return reports


@router.get("/power-user/generate-report", tags=["power_user"])
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
            response = StreamingResponse(
                content=file_contents, status_code=status.HTTP_200_OK, headers=headers
            )
            return response
