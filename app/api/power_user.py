import tempfile
from typing import Annotated, Union

from fastapi import APIRouter, Depends, status
from starlette.responses import StreamingResponse, JSONResponse, Response

from app.db.crud import ReportCRUD
from app.db.models import (
    ReportModel,
    TokenData,
    ReportStatus,
    UserModel,
    COEModel,
    UserLevels,
)
from app.dependencies import DependencyContainer
from app.services.auth import parse_token
from app.services.user_services import UserService, PowerUserService

router = APIRouter()


@router.get("/power-user/all-users", tags=["power_user"])
async def get_all_user(
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
    token_data: TokenData = Depends(parse_token),
):
    if token_data.permissions != UserLevels.PowerUser:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    with dependency_container.get_db() as db:
        reports = PowerUserService.fetch_all_users(db)

    return reports


@router.get("/power-user/all-coe", tags=["power_user"])
async def get_all_coe(
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
    token_data: TokenData = Depends(parse_token),
):
    if token_data.permissions != UserLevels.PowerUser:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    with dependency_container.get_db() as db:
        reports = PowerUserService.fetch_all_coe(db)

    return reports


@router.get("/power-user/all-reports", tags=["power_user"])
async def get_all_reports(
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
    token_data: TokenData = Depends(parse_token),
):
    if token_data.permissions != UserLevels.PowerUser:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    with dependency_container.get_db() as db:
        reports = PowerUserService.fetch_all_reports(db)

    return reports


@router.get("/power-user/generate-report", tags=["power_user"])
async def generate_report(
    report_id: int,
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
    token_data: TokenData = Depends(parse_token),
):
    if token_data.permissions != UserLevels.PowerUser:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

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
