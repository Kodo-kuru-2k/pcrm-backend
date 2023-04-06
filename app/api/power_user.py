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
