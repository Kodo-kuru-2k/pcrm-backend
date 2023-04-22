import tempfile
from typing import Annotated, List

from fastapi import APIRouter, Depends, status, Query
from starlette.responses import StreamingResponse, JSONResponse

from app.db.crud import ReportCRUD
from app.db.models import ReportModel, ReportUpdateModel, TokenData, ReportStatus
from app.dependencies import DependencyContainer
from app.services.auth import parse_token
from app.services.user_services import UserService

router = APIRouter(prefix="/api")


@router.get("/users/pending-reports", tags=["users"])
async def get_pending_reports(
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
    token_data: TokenData = Depends(parse_token),
) -> list[ReportModel]:
    with dependency_container.get_db() as db:
        reports = UserService.fetch_pending_reports_by_user(db, token_data.emp_id)

    return reports


@router.get("/users/submitted-reports", tags=["users"])
async def get_submitted_reports(
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
    token_data: TokenData = Depends(parse_token),
) -> list[ReportModel]:
    with dependency_container.get_db() as db:
        user = UserService.fetch_user_by_email(db, email=token_data.email)
        reports = UserService.fetch_submitted_reports_by_user(db, user.emp_id)

    return reports


@router.get("/users/generate-consolidated-report", tags=["users"])
async def generate_consolidated_report(
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
    report_ids: List[int] = Query(None),
):
    with dependency_container.get_db() as db:
        with tempfile.NamedTemporaryFile(suffix=".pdf") as temp:
            report_generator = dependency_container.REPORT_GENERATOR
            reports = ReportCRUD.get_multiple_report_by_ids(db, report_ids)
            for report in reports:
                if report.report_status == ReportStatus.Draft:
                    return JSONResponse(
                        content={"message": f"report {report.report_id} is a draft"},
                        status_code=status.HTTP_404_NOT_FOUND,
                    )

            file_contents = UserService.generate_multiple_pdf_and_merge(
                db, reports, report_generator=report_generator, file_name=temp.name
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


@router.get("/users/generate-report", tags=["users"])
async def generate_report(
    report_id: int,
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
):
    with dependency_container.get_db() as db:
        with tempfile.NamedTemporaryFile(suffix=".pdf") as temp:
            report_generator = dependency_container.REPORT_GENERATOR

            report = ReportCRUD.get_report_by_report_id(db, report_id)
            if report.report_status == ReportStatus.Draft:
                return JSONResponse(
                    content={"message": "report is a draft"},
                    status_code=status.HTTP_404_NOT_FOUND,
                )

            file_contents = UserService.generate_pdf(
                db, report, report_generator=report_generator, file_name=temp.name
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
    token_data: TokenData = Depends(parse_token),
):
    with dependency_container.get_db() as db:
        UserService.update_user_level_report(db, report=report)
