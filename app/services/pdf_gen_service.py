import pdfkit
from mako.template import Template


class ReportGenerator:
    def __init__(self):
        self.template = Template(
            filename='report_template.html'
        )
        self.config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')

    def generate_pdf(self):
        # todo
        # use named temporary file
        output_text = self.template.render()
        output_pdf = 'pdf_generated.pdf'
        config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
        pdfkit.from_string(output_text, output_pdf, configuration=config)


if __name__ == '__main__':
    # pass
    template = Template(
        filename='report_template.html'
    )
    output_text = template.render()
    output_pdf = 'pdf_generated.pdf'
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    pdfkit.from_string(output_text, output_pdf, configuration=config)
