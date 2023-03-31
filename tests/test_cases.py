import json
from app.db.database import SessionLocal, engine, get_db
from app.db.models import Base
from app.db.schemas import User, UserLevels, Report, COE, ReportStatus
from app.services.user_services import AdminService

test_json = {
    "name": "John Doe",
    "age": 28,
    "email": "johndoe@example.com",
    "phone": "+1-555-123-4567",
    "address": {
        "street": "123 Main St",
        "city": "Anytown",
        "state": "CA",
        "zip": "12345"
    },
    "interests": [
        "reading",
        "hiking",
        "cooking"
    ],
    "education": {
        "degree": "Bachelor of Science",
        "major": "Computer Science",
        "school": "University of California"
    },
    "work_experience": [
        {
            "position": "Software Engineer",
            "company": "Acme Inc",
            "duration": "2 years"
        },
        {
            "position": "Systems Analyst",
            "company": "XYZ Corp",
            "duration": "3 years"
        }
    ],
    "skills": {
        "programming_languages": ["Java", "Python", "C++"],
        "web_technologies": ["HTML", "CSS", "JavaScript"],
        "databases": ["MySQL", "Oracle"]
    },
    "certifications": [
        {
            "name": "Oracle Certified Professional, Java SE 11 Developer",
            "organization": "Oracle Corporation",
            "year": 2022
        },
        {
            "name": "Certified Kubernetes Administrator (CKA)",
            "organization": "Cloud Native Computing Foundation",
            "year": 2021
        }
    ],
    "languages": [
        {
            "language": "English",
            "level": "Native"
        },
        {
            "language": "Spanish",
            "level": "Intermediate"
        },
        {
            "language": "Mandarin Chinese",
            "level": "Beginner"
        }
    ],
    "awards": [
        {
            "name": "Outstanding Employee Award",
            "organization": "Acme Inc",
            "year": 2021
        },
        {
            "name": "Best Paper Award",
            "conference": "IEEE Conference on Big Data",
            "year": 2020
        }
    ],
    "publications": [
        {
            "title": "Machine Learning for Image Classification",
            "authors": ["John Doe", "Jane Smith"],
            "conference": "ICML",
            "year": 2022
        },
        {
            "title": "Natural Language Processing for Sentiment Analysis",
            "authors": ["John Doe", "Mary Johnson"],
            "conference": "ACL",
            "year": 2021
        }]}

if __name__ == '__main__':
    # Base.metadata.create_all(engine)
    new_user = User(
        emp_id="user123",
        name="firstuser",
        email="abc@xyz.com",
        password="somepassword",
        permissions=UserLevels.User
    )
    new_coe = COE(
        center_id="center123",
        center_name="coe1",
        establishment_date=1680254931,
        purpose="test coe 1",
        sponsor="me",
        department_name="someone",
        department_head="user123",
    )
    new_coe_2 = COE(
        center_id="center456",
        center_name="coe2",
        establishment_date=1680254900,
        purpose="test coe 2",
        sponsor="me",
        department_name="noone",
        department_head="user123",
    )
    new_report = Report(
        report_status=ReportStatus.Draft,
        report=json.dumps(test_json),
        submission_date=1680255000,
        due_date=1680256000,
        center_id="center123"
    )
    new_report_2 = Report(
        report_status=ReportStatus.Submitted,
        report=json.dumps(test_json),
        submission_date=1680255000,
        due_date=1680256000,
        center_id="center456"
    )

    with get_db() as db:
        # AdminService.add_new_user(db, new_user)
        # AdminService.add_new_coe(db, new_coe)
        # AdminService.add_new_coe(db, new_coe_2)
        # AdminService.add_new_report(db, new_report)
        # AdminService.add_new_report(db, new_report_2)

        reports = AdminService.fetch_reports_by_user(db, user=new_user)
        print(reports)
        print(len(reports))
        print(AdminService.fetch_all_users(db))
        print(AdminService.fetch_user_by_email(db, email='abc@123.com'))

        modify_user = User(
            emp_id="user123",
            name="middleuser",
            email="abc@123.com",
            password="nopassword",
            permissions=UserLevels.PowerUser,
            is_active=False
        )
        modify_coe = COE(
            center_id="center456",
            center_name="coe3",
            establishment_date=1680254900,
            purpose="test coe 3",
            sponsor="me",
            department_name="noone",
            department_head="user123",
        )
        modify_report = Report(
            report_id=1,
            report_status=ReportStatus.Submitted,
            report=json.dumps(test_json),
            submission_date=1680255000,
            due_date=1680256000,
            center_id="center456"
        )
        AdminService.update_user(db, user=modify_user)
        AdminService.update_coe(db, coe=modify_coe)
        AdminService.update_report(db, report=modify_report)
