import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


class CVGenerator:
    """Generate customized CVs from JSON data for different audiences."""
    
    def __init__(self, data_file: str = "cv_data.json"):
        """Initialize with CV data from JSON file."""
        self.data = self._load_data(data_file)
        
    def _load_data(self, file_path: str) -> dict:
        """Load CV data from JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_data(self, file_path: str = "cv_data.json"):
        """Save current CV data back to JSON file."""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def update_section(self, section: str, data: dict):
        """Update a specific section of the CV."""
        if section in self.data:
            self.data[section].update(data)
        else:
            self.data[section] = data
        return self
    
    def add_experience(self, experience: dict):
        """Add new work experience entry."""
        self.data['work_experience'].insert(0, experience)
        return self
    
    def add_publication(self, pub_type: str, publication: dict):
        """Add new publication (book_chapters or conference_proceedings)."""
        if pub_type in self.data['publications']:
            self.data['publications'][pub_type].insert(0, publication)
        return self
    
    def add_certification(self, certification: dict):
        """Add new certification."""
        self.data['certifications'].insert(0, certification)
        return self
    
    def generate_markdown(self, 
                         sections: Optional[List[str]] = None,
                         experience_limit: Optional[int] = None,
                         publications_limit: Optional[int] = None,
                         style: str = "research") -> str:
        """
        Generate CV in Markdown format.
        
        Args:
            sections: List of sections to include (None = all)
            experience_limit: Maximum number of experiences to show
            publications_limit: Maximum number of publications to show
            style: CV style - "research", "industry", "academic", "technical"
        """
        md = []
        
        # Header
        md.append(f"# {self.data['personal_info']['name']}")
        md.append(f"**{self.data['personal_info']['title']}**\n")
        
        # Contact info
        md.append("## Contact Information")
        md.append(f"- **Email:** {self.data['personal_info']['email']}")
        md.append(f"- **Phone:** {self.data['personal_info']['phone']}")
        for website in self.data['personal_info']['websites']:
            md.append(f"- {website}")
        md.append("")
        
        # Profile (customized by style)
        if not sections or 'profile' in sections:
            md.append("## Profile")
            md.append(self.data['profile']['summary'])
            
            if style in ["research", "academic"]:
                md.append("\n**Key Expertise:**")
                for exp in self.data['profile']['expertise']:
                    md.append(f"- {exp}")
            md.append("")
        
        # Education
        if not sections or 'education' in sections:
            md.append("## Education")
            for edu in self.data['education']:
                distinction = f" ({edu['distinction']})" if edu['distinction'] and edu['distinction'] != False else ""
                md.append(f"### {edu['degree']}{distinction}")
                md.append(f"**{edu['institution']}** | {edu['period']}")
                md.append(f"{edu['description']}\n")
        
        # Work Experience
        if not sections or 'experience' in sections:
            md.append("## Work Experience")
            experiences = self.data['work_experience'][:experience_limit] if experience_limit else self.data['work_experience']
            
            for exp in experiences:
                md.append(f"### {exp['position']}")
                md.append(f"**{exp['company']}** | {exp['period']}\n")
                for resp in exp['responsibilities']:
                    md.append(f"- {resp}")
                md.append("")
        
        # Skills (organized by style)
        if not sections or 'skills' in sections:
            md.append("## Skills & Competencies")
            
            skill_order = {
                "research": ["research", "pedagogical", "technical"],
                "academic": ["pedagogical", "research", "technical"],
                "industry": ["technical", "pedagogical", "research"],
                "technical": ["technical", "research", "pedagogical"]
            }
            
            order = skill_order.get(style, ["research", "technical", "pedagogical"])
            
            for skill_type in order:
                if skill_type in self.data['skills']:
                    title = skill_type.replace("_", " ").title()
                    md.append(f"### {title}")
                    for skill in self.data['skills'][skill_type]:
                        md.append(f"- {skill}")
                    md.append("")
        
        # Certifications
        if not sections or 'certifications' in sections:
            md.append("## Certifications")
            for cert in self.data['certifications']:
                location = f" | {cert['location']}" if 'location' in cert else ""
                md.append(f"- **{cert['name']}** - {cert['issuer']} ({cert['year']}){location}")
            md.append("")
        
        # Publications (prioritized for research/academic)
        if (not sections or 'publications' in sections) and style in ["research", "academic"]:
            md.append("## Publications")
            
            if self.data['publications']['book_chapters']:
                md.append("### Book Chapters")
                for pub in self.data['publications']['book_chapters'][:publications_limit]:
                    authors = " & ".join(pub['authors'])
                    md.append(f"- {authors} ({pub['year']}). *{pub['title']}*. In {', '.join(pub['editors'])} (Eds.), *{pub['book']}*. {pub['publisher']}.")
                md.append("")
            
            if self.data['publications']['conference_proceedings']:
                md.append("### Conference Proceedings")
                pubs = self.data['publications']['conference_proceedings'][:publications_limit] if publications_limit else self.data['publications']['conference_proceedings']
                for pub in pubs:
                    authors = " & ".join(pub['authors'])
                    doi = f" doi:{pub['doi']}" if 'doi' in pub else ""
                    md.append(f"- {authors} ({pub['year']}). *{pub['title']}*{doi}")
                md.append("")
        
        # Memberships
        if not sections or 'memberships' in sections:
            md.append("## Professional Memberships")
            for mem in self.data['memberships']:
                member_id = f" (ID: {mem['member_id']})" if mem['member_id'] else ""
                md.append(f"### {mem['organization']}{member_id}")
                if mem['sigs']:
                    md.append(f"Special Interest Groups: {', '.join(mem['sigs'])}")
                if mem['chapters']:
                    md.append(f"Chapters: {', '.join(mem['chapters'])}")
                md.append("")
        
        # Referees (optional for some styles)
        if (not sections or 'referees' in sections) and style != "industry":
            md.append("## Referees")
            for ref in self.data['referees']:
                md.append(f"### {ref['name']}")
                md.append(f"{ref['position']}")
                md.append(f"- Phone: {ref['phone']}")
                md.append(f"- Email: {ref['email']}\n")
        
        return "\n".join(md)
    
    def generate_html(self, **kwargs) -> str:
        """Generate CV in HTML format."""
        md_content = self.generate_markdown(**kwargs)
        
        # Simple Markdown to HTML conversion
        html_lines = []
        html_lines.append("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CV - {}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; border-bottom: 2px solid #ecf0f1; padding-bottom: 5px; }}
        h3 {{ color: #7f8c8d; margin-top: 20px; }}
        a {{ color: #3498db; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        ul {{ margin: 10px 0; }}
        li {{ margin: 5px 0; }}
        @media print {{
            body {{ margin: 0; padding: 20px; }}
        }}
    </style>
</head>
<body>
""".format(self.data['personal_info']['name']))
        
        # Convert markdown to HTML (basic conversion)
        for line in md_content.split('\n'):
            if line.startswith('# '):
                html_lines.append(f"<h1>{line[2:]}</h1>")
            elif line.startswith('## '):
                html_lines.append(f"<h2>{line[3:]}</h2>")
            elif line.startswith('### '):
                html_lines.append(f"<h3>{line[4:]}</h3>")
            elif line.startswith('- '):
                html_lines.append(f"<li>{line[2:]}</li>")
            elif line.startswith('**') and line.endswith('**'):
                html_lines.append(f"<p><strong>{line[2:-2]}</strong></p>")
            elif line.strip():
                # Convert **text** to <strong>text</strong>
                line = line.replace('**', '<strong>', 1).replace('**', '</strong>', 1)
                html_lines.append(f"<p>{line}</p>")
            else:
                html_lines.append("<br>")
        
        html_lines.append("""
</body>
</html>""")
        
        return "\n".join(html_lines)
    
    def save_cv(self, filename: str, format: str = "markdown", **kwargs):
        """Save generated CV to file."""
        if format == "markdown":
            content = self.generate_markdown(**kwargs)
        elif format == "html":
            content = self.generate_html(**kwargs)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"CV saved to {filename}")


# Example usage and templates
if __name__ == "__main__":
    cv = CVGenerator()
    
    # Generate different versions
    print("Generating CV versions...")
    
    # 1. Research-focused CV (full publications)
    cv.save_cv("cv_research_focused.md", 
               format="markdown",
               style="research")
    
    # 2. Industry-focused CV (condensed, technical focus)
    cv.save_cv("cv_industry.md",
               format="markdown", 
               style="industry",
               experience_limit=3,
               publications_limit=5,
               sections=['profile', 'experience', 'skills', 'certifications'])
    
    # 3. Academic CV (comprehensive)
    cv.save_cv("cv_academic.html",
               format="html",
               style="academic")
    
    # 4. Technical CV
    cv.save_cv("cv_technical.md",
               format="markdown",
               style="technical",
               sections=['profile', 'skills', 'experience', 'certifications'])
    
    print("\nDone! Generated 4 CV versions.")