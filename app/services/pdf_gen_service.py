from datetime import datetime

import jinja2
import pdfkit

from app.services.pdf_models import PDFModelFinal


class ReportGenerator:
    def __init__(
        self,
        template_file_path: str,
        wkhtmltopdf_location: str = "/usr/local/bin/wkhtmltopdf",
    ):
        template_loader = jinja2.FileSystemLoader(template_file_path)
        template_env = jinja2.Environment(loader=template_loader)
        self.template = template_env.get_template("report_template.html")
        self.config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_location)

    def generate_pdf(self, file_name: str, render_data: PDFModelFinal) -> None:
        render_data = render_data.dict()
        render_data["establishment_date"] = datetime.fromtimestamp(
            render_data["establishment_date"]
        ).strftime("%d-%m-%y")
        output_text = self.template.render(render_data)
        pdfkit.from_string(output_text, file_name, configuration=self.config)
