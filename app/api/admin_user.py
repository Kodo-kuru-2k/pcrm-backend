import tempfile
from typing import Annotated

from fastapi import APIRouter, Depends, status, Response
from starlette.responses import StreamingResponse

from app.db.models import ReportModel, COEModel, UserModel
from app.dependencies import DependencyContainer
from app.services.password_hash import PasswordHash
from app.services.user_services import AdminService
from app.services.user_services_models import DateModel

router = APIRouter()

"""
admin fetch data
"""


@router.get("/admin/all-users", tags=["admin"])
async def get_all_user(
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
) -> list[UserModel]:
    with dependency_container.get_db() as db:
        reports = AdminService.fetch_all_users(db)

    return reports


@router.get("/admin/all-coe", tags=["admin"])
async def get_all_coe(
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
) -> list[COEModel]:
    with dependency_container.get_db() as db:
        reports = AdminService.fetch_all_coe(db)

    return reports


@router.get("/admin/all-reports", tags=["admin"])
async def get_all_reports(
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
) -> list[ReportModel]:
    with dependency_container.get_db() as db:
        reports = AdminService.fetch_all_reports(db)

    return reports


@router.get("/admin/generate-report", tags=["admin"])
async def generate_report(
    report_id: int,
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
):
    with dependency_container.get_db() as db:
        with tempfile.NamedTemporaryFile(suffix=".pdf") as temp:
            report_generator = dependency_container.REPORT_GENERATOR
            file_contents = AdminService.generate_pdf(
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


"""
admin create data
"""


@router.post("/admin/create-report-for-each-quarter", tags=["admin"])
async def create_new_report_for_each_quarter(
    date_model: DateModel,
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
):
    with dependency_container.get_db() as db:
        AdminService.add_reports_for_all_coe_based_on_quarter(db, date_model)
    return Response(status_code=status.HTTP_200_OK)


@router.post("/admin/create-report", tags=["admin"])
async def create_new_report(
    report_model: ReportModel,
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
):
    with dependency_container.get_db() as db:
        AdminService.add_new_report(db, report_model)

    return Response(status_code=status.HTTP_200_OK)


@router.post("/admin/create-ceo", tags=["admin"])
async def create_new_coe(
    ceo_model: COEModel,
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
):
    with dependency_container.get_db() as db:
        AdminService.add_new_coe(db, ceo_model)

    return Response(status_code=status.HTTP_200_OK)


@router.post("/admin/create-user", tags=["admin"])
async def create_new_user(
    user_model: UserModel,
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
):
    with dependency_container.get_db() as db:
        user_model.password = PasswordHash.hash_password(user_model.password)
        AdminService.add_new_user(db, user_model)

    return Response(status_code=status.HTTP_200_OK)


"""
modify data
"""


@router.patch("/admin/modify-user", tags=["admin"])
async def modify_user(
    user_model: UserModel,
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
):
    with dependency_container.get_db() as db:
        existing_model = AdminService.fetch_user_by_emp_id(db, user_model.emp_id)
        if existing_model.password != user_model.password:
            user_model.password = PasswordHash.hash_password(
                password=user_model.password
            )
        AdminService.update_user(db, user=user_model)
    return Response(status_code=status.HTTP_200_OK)


@router.patch("/admin/modify-coe", tags=["admin"])
async def modify_coe(
    coe_model: COEModel,
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
):
    with dependency_container.get_db() as db:
        AdminService.update_coe(db, coe=coe_model)
    return Response(status_code=status.HTTP_200_OK)


@router.patch("/admin/modify-report", tags=["admin"])
async def modify_report(
    report_model: ReportModel,
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
):
    with dependency_container.get_db() as db:
        AdminService.update_report(db, report=report_model)
    return Response(status_code=status.HTTP_200_OK)


"""
delete report
"""


@router.delete("/admin/delete-report", tags=["admin"])
async def delete_report(
    report_id: int,
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
):
    with dependency_container.get_db() as db:
        AdminService.delete_report(db, report_id=report_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/admin/delete-coe", tags=["admin"])
async def delete_coe(
    center_id: str,
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
):
    with dependency_container.get_db() as db:
        AdminService.delete_coe(db, center_id=center_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/admin/delete-user", tags=["admin"])
async def delete_user(
    user_id: str,
    dependency_container: Annotated[DependencyContainer, Depends(DependencyContainer)],
):
    with dependency_container.get_db() as db:
        AdminService.delete_user_by_user_id(db, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
