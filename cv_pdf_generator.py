"""
PDF Generation Module for CV System
Requires: weasyprint, markdown2
Install: pip install weasyprint markdown2
"""

import markdown2
from weasyprint import HTML, CSS
from pathlib import Path
from cv_generator import CVGenerator


class PDFGenerator:
    """Generate professional PDF CVs with custom styling."""
    
    # Professional CSS styles for PDF
    PDF_STYLES = """
    @page {
        size: A4;
        margin: 2cm;
    }
    
    body {
        font-family: 'Helvetica', 'Arial', sans-serif;
        font-size: 11pt;
        line-height: 1.5;
        color: #333;
    }
    
    h1 {
        color: #2c3e50;
        font-size: 28pt;
        margin-bottom: 5pt;
        border-bottom: 3pt solid #3498db;
        padding-bottom: 8pt;
    }
    
    h2 {
        color: #34495e;
        font-size: 16pt;
        margin-top: 20pt;
        margin-bottom: 10pt;
        border-bottom: 1.5pt solid #bdc3c7;
        padding-bottom: 5pt;
    }
    
    h3 {
        color: #555;
        font-size: 13pt;
        margin-top: 12pt;
        margin-bottom: 5pt;
    }
    
    p {
        margin: 5pt 0;
    }
    
    ul {
        margin: 5pt 0;
        padding-left: 20pt;
    }
    
    li {
        margin: 3pt 0;
    }
    
    a {
        color: #3498db;
        text-decoration: none;
    }
    
    strong {
        color: #2c3e50;
    }
    
    .contact-info {
        font-size: 10pt;
        margin-bottom: 15pt;
    }
    
    .section-gap {
        margin-top: 15pt;
    }
    
    /* Page break control */
    h2 {
        page-break-after: avoid;
    }
    
    h3 {
        page-break-after: avoid;
    }
    
    .no-break {
        page-break-inside: avoid;
    }
    """
    
    ACADEMIC_STYLES = """
    @page {
        size: A4;
        margin: 2.5cm;
    }
    
    body {
        font-family: 'Georgia', 'Times New Roman', serif;
        font-size: 10pt;
        line-height: 1.4;
        color: #000;
    }
    
    h1 {
        font-size: 24pt;
        text-align: center;
        margin-bottom: 10pt;
        border: none;
    }
    
    h2 {
        font-size: 14pt;
        font-weight: bold;
        margin-top: 15pt;
        margin-bottom: 8pt;
        border-bottom: 1pt solid #000;
    }
    
    h3 {
        font-size: 11pt;
        font-weight: bold;
        font-style: italic;
        margin-top: 10pt;
    }
    
    .contact-info {
        text-align: center;
        font-size: 9pt;
        margin-bottom: 20pt;
    }
    """
    
    def __init__(self, cv_generator: CVGenerator):
        """Initialize with a CV generator instance."""
        self.cv = cv_generator
    
    def generate_pdf(self, 
                     output_file: str,
                     style: str = "research",
                     pdf_style: str = "professional",
                     **kwargs):
        """
        Generate PDF from CV data.
        
        Args:
            output_file: Path to save PDF
            style: CV style (research, industry, academic, technical)
            pdf_style: PDF styling (professional, academic)
            **kwargs: Additional arguments for CV generation
        """
        # Generate markdown content
        md_content = self.cv.generate_markdown(style=style, **kwargs)
        
        # Convert markdown to HTML
        html_content = markdown2.markdown(
            md_content,
            extras=['tables', 'break-on-newline']
        )
        
        # Wrap in full HTML document
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>CV - {self.cv.data['personal_info']['name']}</title>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Select CSS style
        css_style = self.ACADEMIC_STYLES if pdf_style == "academic" else self.PDF_STYLES
        
        # Generate PDF
        HTML(string=full_html).write_pdf(
            output_file,
            stylesheets=[CSS(string=css_style)]
        )
        
        print(f"✓ PDF generated: {output_file}")
        return output_file
    
    def generate_all_versions(self, output_dir: str = "output/pdf"):
        """Generate PDF versions for all CV styles."""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        versions = [
            ("research", "academic", {}),
            ("industry", "professional", {"experience_limit": 3, "publications_limit": 5}),
            ("academic", "academic", {}),
            ("technical", "professional", {"sections": "profile,skills,experience,certifications"}),
        ]
        
        generated = []
        for cv_style, pdf_style, kwargs in versions:
            output_file = f"{output_dir}/cv_{cv_style}.pdf"
            self.generate_pdf(output_file, style=cv_style, pdf_style=pdf_style, **kwargs)
            generated.append(output_file)
        
        return generated


# Standalone usage
if __name__ == "__main__":
    cv = CVGenerator()
    pdf_gen = PDFGenerator(cv)
    
    # Generate all versions
    files = pdf_gen.generate_all_versions()
    print(f"\nGenerated {len(files)} PDF versions:")
    for f in files:
        print(f"  - {f}")