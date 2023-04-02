import http
import json
import tempfile
from typing import Annotated

from fastapi import APIRouter, Depends, status, Response
from fastapi_jwt_auth import AuthJWT
from starlette.responses import StreamingResponse

from app.db.models import ReportModel, ReportUpdateModel, UserModel, UserLoginModel
from app.dependencies import DependencyContainer
from app.services.auth import create_access_token
from app.services.password_hash import PasswordHash
from app.services.user_services import UserService, AdminService

router = APIRouter()


@router.post("/login", tags=["common"])
async def set_cookie_for_login(
    user: UserLoginModel,
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
):
    with dependency_container.get_db() as db:
        existing_user = UserService.fetch_user_by_email(db, user.email)
        if existing_user.email == user.email and PasswordHash.compare_hash(
            user.password, hashed_password=existing_user.password
        ):
            existing_user = json.loads(existing_user.json())
            del existing_user["password"]
            access_token = create_access_token(data=existing_user)
            response = Response(status_code=status.HTTP_200_OK)
            response.set_cookie(key="access_token", value=f"{access_token}")
            return response

    return Response(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/forgot-password", tags=["common"])
async def get_pending_reports(
    email_id: str,
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
):
    with dependency_container.get_db() as db:
        print(email_id)
        user = UserService.fetch_user_by_email(db, email_id)
        dependency_container.PASSWORD_RESET_HANDLER.send_recovery_link(
            to=user.email, emp_id=user.emp_id
        )


@router.post("/recovery-link/{random_string}", tags=["common"])
async def get_pending_reports(
    random_string: str,
    password: str,
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
):
    with dependency_container.get_db() as db:
        emp_id = dependency_container.PASSWORD_RESET_HANDLER.decode_random_string(
            enc_recovery_string=random_string
        )
        if emp_id is None:
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)
        user = AdminService.fetch_user_by_emp_id(db, emp_id)
        user.password = PasswordHash.hash_password(password)
        AdminService.update_user(db, user)
