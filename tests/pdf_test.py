import os

from app.services.pdf_gen_service import ReportGenerator
from app.services.pdf_models import PDFModelFinal
from pathlib import Path

test_json = {
    "establishment_date": 384280159,
    "center_name": "ABC Center",
    "purpose": "Research and Development",
    "center_incharge": "John Doe",
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
    file_path = os.path.join(Path(os.path.abspath(__file__)).parent.parent, "templates")
    rgen = ReportGenerator(file_path)
    rgen.generate_pdf(
        file_name="pdf_generated.pdf", render_data=PDFModelFinal.parse_obj(test_json)
    )
