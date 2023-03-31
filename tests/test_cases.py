import json
import pprint

from app.db.schemas import Base
from app.db.models import UserModel, UserLevels, ReportModel, COEModel, ReportStatus
from app.dependencies import DependencyContainer
from app.services.user_services import AdminService

test_json = {
    "establishment_date": 384280159,
    "center_name": "ABC Center",
    "purpose": "Research and Development",
    "coe_head_name": "John Doe",
    "sponsor": "XYZ Corporation",
    "hardware": [
        {"sno": "1", "description": "Computer, Dell XPS", "quantity": "5"},
        {"sno": "2", "description": "Printer, HP LaserJet", "quantity": "3"},
    ],
    "software": [
        {
            "sno": "1",
            "description": "Microsoft Office, 2022",
            "quantity": "6",
        },
        {
            "sno": "2",
            "description": "Autodesk AutoCAD, 2019",
            "quantity": "5",
        },
    ],
    "other_features": "High-speed internet, air conditioning",
    "name_and_designation_of_technical_staff": "Jane Smith, Senior Technician",
    "laboratory_use": {
        "MON": [3, 8, 7, 7, 1, 6, 6, 7, 3],
        "TUE": [9, 5, 2, 7, 5, 2, 5, 0, 9],
        "WED": [4, 10, 9, 7, 5, 10, 10, 10, 0],
        "THU": [3, 7, 8, 2, 3, 2, 5, 10, 7],
        "FRI": [1, 6, 4, 3, 10, 10, 6, 1, 6],
        "SAT": [10, 0, 2, 4, 9, 1, 7, 8, 9],
    },
    "research_activities": {
        "candidate_name": "Alice Johnson",
        "supervisor": "Dr. Bob Smith",
    },
    "consultancy_activities": [
        {
            "sno": 1,
            "client": "ABC Company",
            "nature_of_work": "Software development",
            "revenue_generated": "10,000",
        },
        {
            "sno": 2,
            "client": "XYZ Corporation",
            "nature_of_work": "IT consulting",
            "revenue_generated": "20,000",
        },
    ],
    "total_number_of_courses_conducted": 5,
    "total_number_of_participants": 100,
    "revenue_generated": 50000,
}

if __name__ == "__main__":
    new_user = UserModel(
        emp_id="user123",
        name="firstuser",
        email="abc@xyz.com",
        password="somepassword",
        permissions=UserLevels.User,
    )
    new_coe = COEModel(
        center_id="center123",
        center_name="coe1",
        establishment_date=1680254931,
        purpose="test coe 1",
        sponsor="me",
        department_name="someone",
        department_head="user123",
    )
    new_coe_2 = COEModel(
        center_id="center456",
        center_name="coe2",
        establishment_date=1680254900,
        purpose="test coe 2",
        sponsor="me",
        department_name="noone",
        department_head="user123",
    )
    new_report = ReportModel(
        report_status=ReportStatus.Draft,
        report=json.dumps(test_json),
        submission_date=1680255000,
        due_date=1680256000,
        center_id="center123",
    )
    new_report_2 = ReportModel(
        report_status=ReportStatus.Submitted,
        report=json.dumps(test_json),
        submission_date=1680255000,
        due_date=1680256000,
        center_id="center456",
    )
    DependencyContainer.initialize_container()
    Base.metadata.create_all(DependencyContainer.ENGINE)

    with DependencyContainer.get_db() as db:
        AdminService.add_new_user(db, new_user)
        AdminService.add_new_coe(db, new_coe)
        AdminService.add_new_coe(db, new_coe_2)
        AdminService.add_new_report(db, new_report)
        AdminService.add_new_report(db, new_report_2)

        reports = AdminService.fetch_submitted_reports_by_user(
            db, emp_id=new_user.emp_id
        )
        pprint.pprint(reports)
        print(len(reports))
        print(AdminService.fetch_all_users(db))
        print(AdminService.fetch_user_by_email(db, email="abc@xyz.com"))

        modify_user = UserModel(
            emp_id="user123",
            name="middleuser",
            email="abc@123.com",
            password="nopassword",
            permissions=UserLevels.PowerUser,
            is_active=False,
        )
        modify_coe = COEModel(
            center_id="center456",
            center_name="coe3",
            establishment_date=1680254900,
            purpose="test coe 3",
            sponsor="me",
            department_name="noone",
            department_head="user123",
        )
        modify_report = ReportModel(
            report_id=1,
            report_status=ReportStatus.Submitted,
            report=json.dumps(test_json),
            submission_date=1680255000,
            due_date=1680256000,
            center_id="center456",
        )
        # AdminService.update_user(db, user=modify_user)
        # AdminService.update_coe(db, coe=modify_coe)
        # AdminService.update_report(db, report=modify_report)
