import json
import markdown2
from cv_generator import CVGenerator # Inherit from the original generator

def get_value(data_field, default=''):
    """Safely gets the 'value' from a data field, returning a string or list."""
    if isinstance(data_field, dict) and 'value' in data_field:
        return data_field['value'] if data_field['value'] is not None else default
    if isinstance(data_field, (str, int, bool, list)):
        return data_field
    # Fallback for unexpected structures (like an empty dict) or None
    return default

def format_conflicts(data_field):
    """Formats the conflicts for a given field into a readable HTML string."""
    if not (isinstance(data_field, dict) and data_field.get('conflicts')):
        return ""
    
    conflict_lines = ["<br><small style='color: #e74c3c;'><em>"]
    for conflict in data_field['conflicts']:
        # Ensure conflict value is a string
        c_val = get_value(conflict, default='N/A')
        c_source = get_value(conflict.get('source'), default='unknown')
        conflict_lines.append(f"&nbsp;&nbsp;- Conflict from {c_source}: {c_val}")
    conflict_lines.append("</em></small>")
    return "<br>".join(conflict_lines)

class ComprehensiveCVGenerator(CVGenerator):
    """A CV generator that understands and displays the merged data format."""
    
    def __init__(self, data_file: str = "cv_data_merged.json"):
        """Initialize with the merged CV data."""
        super().__init__(data_file)

    def generate_markdown(self, **kwargs) -> str:
        """Overrides the original method to generate a comprehensive CV from merged data."""
        md = []
        
        # Helper to process a field for markdown
        def process_field_md(field_data):
            val = get_value(field_data)
            # In markdown, we can just show the primary value. HTML will show conflicts.
            return str(val)

        # Header
        md.append(f"# {process_field_md(self.data['personal_info']['name'])}")
        md.append(f"**{process_field_md(self.data['personal_info']['title'])}**\n")

        # Contact info
        md.append("## Contact Information")
        md.append(f"- **Email:** {process_field_md(self.data['personal_info']['email'])}")
        md.append(f"- **Phone:** {process_field_md(self.data['personal_info']['phone'])}")
        for website in get_value(self.data['personal_info']['websites'], []):
            md.append(f"- {process_field_md(website)}")
        md.append("")

        # Profile
        md.append("## Profile")
        md.append(process_field_md(self.data['profile']['summary']))
        if self.data['profile'].get('expertise'):
            md.append("\n**Key Expertise:**")
            for exp in get_value(self.data['profile']['expertise'], []):
                md.append(f"- {process_field_md(exp)}")
        md.append("")

        # Education
        md.append("## Education")
        for edu in get_value(self.data['education'], []):
            degree = process_field_md(edu['degree'])
            distinction = get_value(edu.get('distinction'))
            distinction_str = f" ({distinction})" if distinction and distinction != False else ""
            md.append(f"### {degree}{distinction_str}")
            md.append(f"**{process_field_md(edu['institution'])}** | {process_field_md(edu['period'])}")
            desc = process_field_md(edu.get('description', ''))
            if desc:
                md.append(f"{desc}\n")

        # Work Experience
        md.append("## Work Experience")
        for exp in get_value(self.data['work_experience'], []):
            md.append(f"### {process_field_md(exp['position'])}")
            md.append(f"**{process_field_md(exp['company'])}** | {process_field_md(exp['period'])}\n")
            for resp in get_value(exp.get('responsibilities', []), []):
                md.append(f"- {process_field_md(resp)}")
            md.append("")

        return "\n".join(md)

    def generate_html(self, **kwargs) -> str:
        """Overrides the base HTML generator to use a proper Markdown converter and handle conflicts."""
        
        # Use a custom function to add conflict details to the HTML
        def add_conflicts_to_html(html):
            # This is a complex task. A simpler way is to embed them in the markdown generation.
            # For now, we will re-do the generation with HTML in mind.
            return html # Placeholder

        # We will build the HTML directly for more control
        lines = []
        
        # Helper to process a field for HTML output
        def process_field_html(field_data):
            val = get_value(field_data)
            conflicts = format_conflicts(field_data)
            return f"{val}{conflicts}"

        # Header
        lines.append(f"<h1>{process_field_html(self.data['personal_info']['name'])}</h1>")
        lines.append(f"<p><strong>{process_field_html(self.data['personal_info']['title'])}</strong></p>")

        # Contact
        lines.append("<h2>Contact Information</h2>")
        lines.append("<ul>")
        lines.append(f"<li><strong>Email:</strong> {process_field_html(self.data['personal_info']['email'])}</li>")
        lines.append(f"<li><strong>Phone:</strong> {process_field_html(self.data['personal_info']['phone'])}</li>")
        for site in get_value(self.data['personal_info']['websites'], []):
            lines.append(f"<li><a href='{get_value(site)}'>{get_value(site)}</a>{format_conflicts(site)}</li>")
        lines.append("</ul>")

        # Profile
        lines.append("<h2>Profile</h2>")
        lines.append(f"<p>{process_field_html(self.data['profile']['summary'])}</p>")
        if self.data['profile'].get('expertise'):
            lines.append("<h3>Key Expertise</h3>")
            lines.append("<ul>")
            for exp in get_value(self.data['profile']['expertise'], []):
                lines.append(f"<li>{process_field_html(exp)}</li>")
            lines.append("</ul>")

        # Education
        lines.append("<h2>Education</h2>")
        for edu in get_value(self.data['education'], []):
            degree = process_field_html(edu['degree'])
            distinction = get_value(edu.get('distinction'))
            distinction_str = f" <em>({distinction})</em>" if distinction and distinction != False else ""
            lines.append(f"<h3>{degree}{distinction_str}</h3>")
            lines.append(f"<p><strong>{process_field_html(edu['institution'])}</strong> | {process_field_html(edu['period'])}</p>")
            desc = get_value(edu.get('description', ''))
            if desc:
                lines.append(f"<p>{desc}</p>")

        # Work Experience
        lines.append("<h2>Work Experience</h2>")
        for exp in get_value(self.data['work_experience'], []):
            lines.append(f"<h3>{process_field_html(exp['position'])}</h3>")
            lines.append(f"<p><strong>{process_field_html(exp['company'])}</strong> | {process_field_html(exp['period'])}</p>")
            responsibilities = get_value(exp.get('responsibilities', []), [])
            if responsibilities:
                lines.append("<ul>")
                for resp in responsibilities:
                    lines.append(f"<li>{process_field_html(resp)}</li>")
                lines.append("</ul>")

        # --- HTML Boilerplate ---
        title_name = get_value(self.data['personal_info']['name'])
        head = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>CV - {title_name}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 900px; margin: 40px auto; padding: 20px; line-height: 1.6; color: #333; }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; border-bottom: 2px solid #ecf0f1; padding-bottom: 5px; }}
        h3 {{ color: #7f8c8d; margin-top: 20px; margin-bottom: 5px; }}
        p {{ margin-top: 0; margin-bottom: 10px; }}
        a {{ color: #3498db; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        ul {{ margin-top: 0; padding-left: 20px; }}
    </style>
</head>
<body>"""
        
        body_content = "\n".join(lines)
        foot = "</body>\n</html>"

        return head + body_content + foot

# Example usage
if __name__ == "__main__":
    print("Generating refined comprehensive CV...")
    comp_cv = ComprehensiveCVGenerator()
    comp_cv.save_cv("comprehensive_cv.html", format="html")
    print("\nDone! comprehensive_cv.html has been updated.")