import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import os

def get_versioned_filename(output_dir, style, format):
    date_str = datetime.now().strftime('%Y%m%d')
    base_filename = f"cv_{style}_{date_str}"
    extension = format.replace('markdown', 'md')
    
    version = 1
    output_file = os.path.join(output_dir, f"{base_filename}.{extension}")
    
    while os.path.exists(output_file):
        version += 1
        output_file = os.path.join(output_dir, f"{base_filename}_v{version}.{extension}")
        
    return output_file

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

    def _generate_profile(self, style: str, sections: Optional[List[str]]) -> List[str]:
        if not sections or 'profile' in sections:
            md = ["## Profile"]
            md.append(self.data['profile']['summary'])
            if style in ["research", "academic"]:
                md.append("\n**Key Expertise:**")
                for exp in self.data['profile']['expertise']:
                    md.append(f"- {exp}")
            md.append("")
            return md
        return []

    def _generate_core_competencies(self, style: str, sections: Optional[List[str]]) -> List[str]:
        if not sections or 'core_competencies' in sections:
            md = ["## Core Competencies"]
            if 'core_competencies' in self.data:
                for competency_type, competencies in self.data['core_competencies'].items():
                    title = competency_type.replace("_", " & ").title()
                    md.append(f"### {title}")
                    for competency in competencies:
                        md.append(f"- {competency}")
                    md.append("")
            return md
        return []

    def _generate_project_experience(self, style: str, sections: Optional[List[str]]) -> List[str]:
        if not sections or 'project_experience' in sections:
            if 'project_experience' in self.data and self.data['project_experience']:
                md = ["## Project Experience"]
                for project in self.data['project_experience']:
                    md.append(f"### {project['title']}")
                    for desc in project['description']:
                        md.append(f"- {desc}")
                    md.append("")
                return md
        return []

    def _generate_work_experience(self, style: str, sections: Optional[List[str]], experience_limit: Optional[int]) -> List[str]:
        if not sections or 'experience' in sections:
            md = ["## Work Experience"]
            experiences = self.data['work_experience'][:experience_limit] if experience_limit else self.data['work_experience']
            for exp in experiences:
                md.append(f"### {exp['position']}")
                md.append(f"**{exp['company']}** | {exp['period']}\n")
                for resp in exp['responsibilities']:
                    md.append(f"- {resp}")
                md.append("")
            return md
        return []

    def _generate_education(self, style: str, sections: Optional[List[str]]) -> List[str]:
        if not sections or 'education' in sections:
            md = ["## Education"]
            for edu in self.data['education']:
                distinction = f" ({edu['distinction']})" if edu.get('distinction') else ""
                md.append(f"### {edu['degree']}{distinction}")
                md.append(f"**{edu['institution']}** | {edu['period']}")
                md.append(f"{edu['description']}\n")
            return md
        return []

    def _generate_certifications(self, style: str, sections: Optional[List[str]]) -> List[str]:
        if not sections or 'certifications' in sections:
            md = ["## Certifications"]
            for cert in self.data['certifications']:
                location = f" | {cert['location']}" if 'location' in cert else ""
                md.append(f"- **{cert['name']}** - {cert['issuer']} ({cert['year']}){location}")
            md.append("")
            return md
        return []

    def _generate_publications(self, style: str, sections: Optional[List[str]], publications_limit: Optional[int]) -> List[str]:
        if (not sections or 'publications' in sections) and style in ["research", "academic"]:
            md = ["## Publications"]
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
            return md
        return []

    def _generate_memberships(self, style: str, sections: Optional[List[str]]) -> List[str]:
        if not sections or 'memberships' in sections:
            md = ["## Professional Memberships"]
            for mem in self.data['memberships']:
                member_id = f" (ID: {mem['member_id']})" if mem['member_id'] else ""
                md.append(f"### {mem['organization']}{member_id}")
                if mem['sigs']:
                    md.append(f"Special Interest Groups: {', '.join(mem['sigs'])}")
                if mem['chapters']:
                    md.append(f"Chapters: {', '.join(mem['chapters'])}")
                md.append("")
            return md
        return []

    def _generate_referees(self, style: str, sections: Optional[List[str]]) -> List[str]:
        if (not sections or 'referees' in sections) and style != "industry":
            md = ["## Referees"]
            for ref in self.data['referees']:
                md.append(f"### {ref['name']}")
                md.append(f"{ref['position']}")
                md.append(f"- Phone: {ref['phone']}")
                md.append(f"- Email: {ref['email']}\n")
            return md
        return []

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

        section_generators = {
            'profile': lambda: self._generate_profile(style, sections),
            'core_competencies': lambda: self._generate_core_competencies(style, sections),
            'project_experience': lambda: self._generate_project_experience(style, sections),
            'experience': lambda: self._generate_work_experience(style, sections, experience_limit),
            'education': lambda: self._generate_education(style, sections),
            'certifications': lambda: self._generate_certifications(style, sections),
            'publications': lambda: self._generate_publications(style, sections, publications_limit),
            'memberships': lambda: self._generate_memberships(style, sections),
            'referees': lambda: self._generate_referees(style, sections),
        }

        section_order = {
            "research": ["profile", "education", "experience", "core_competencies", "publications", "certifications", "memberships", "referees"],
            "academic": ["profile", "education", "experience", "core_competencies", "publications", "certifications", "memberships", "referees"],
            "industry": ["profile", "core_competencies", "experience", "project_experience", "education", "certifications"],
            "technical": ["profile", "core_competencies", "project_experience", "experience", "education", "certifications"],
        }

        order = section_order.get(style, section_order['research'])

        for section_name in order:
            if section_name in section_generators:
                md.extend(section_generators[section_name]())
        
        return "\n".join(md)
    
    def generate_html(self, **kwargs) -> str:
        """Generate CV in HTML format with improved structure."""
        md_content = self.generate_markdown(**kwargs)
        
        html_lines = [
            "<!DOCTYPE html>",
            "<html lang=\"en\">",
            "<head>",
            "    <meta charset=\"UTF-8\">",
            "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">",
            f"    <title>CV - {self.data['personal_info']['name']}</title>",
            "    <link rel=\"stylesheet\" href=\"../templates/style.css\">",
            "</head>",
            "<body>"
        ]

        lines = md_content.split('\n')
        in_section = False
        in_ul = False

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.startswith('## '):
                if in_ul:
                    html_lines.append("    </ul>")
                    in_ul = False
                if in_section:
                    html_lines.append("</section>")
                
                html_lines.append(f"<section>")
                html_lines.append(f"    <h2>{line[3:]}</h2>")
                in_section = True
            
            elif line.startswith('# '):
                if in_ul:
                    html_lines.append("    </ul>")
                    in_ul = False
                if in_section:
                    html_lines.append("</section>")
                
                html_lines.append(f"<header>")
                html_lines.append(f"    <h1>{line[2:]}</h1>")
                in_section = False # Header is not a section

            elif line.startswith('### '):
                if in_ul:
                    html_lines.append("    </ul>")
                    in_ul = False
                html_lines.append(f"    <h3>{line[4:]}</h3>")

            elif line.startswith('- '):
                if not in_ul:
                    html_lines.append("    <ul>")
                    in_ul = True
                
                processed_line = line[2:]
                processed_line = processed_line.replace('**', '<strong>').replace('**', '</strong>')
                html_lines.append(f"        <li>{processed_line}</li>")

            elif line.startswith('**'):
                if in_ul:
                    html_lines.append("    </ul>")
                    in_ul = False
                html_lines.append(f"    <p>{line.replace('**', '<strong>', 1).replace('**', '</strong>', 1)}</p>")
            
            else:
                if in_ul:
                    html_lines.append("    </ul>")
                    in_ul = False
                html_lines.append(f"    <p>{line}</p>")

        if in_ul:
            html_lines.append("    </ul>")
        if in_section:
            html_lines.append("</section>")

        html_lines.append("</body>")
        html_lines.append("</html>")
        
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
    
    # Create documents directory if it doesn't exist
    output_dir = "documents"
    os.makedirs(output_dir, exist_ok=True)

    # Generate different versions
    print("Generating CV versions...")
    
    # 1. Research-focused CV (full publications)
    cv.save_cv(get_versioned_filename(output_dir, "research", "md"), 
               format="markdown",
               style="research")
    
    # 2. Industry-focused CV (condensed, technical focus)
    cv.save_cv(get_versioned_filename(output_dir, "industry", "md"),
               format="markdown", 
               style="industry",
               experience_limit=3,
               publications_limit=5,
               sections=['profile', 'experience', 'core_competencies', 'certifications'])
    
    # 3. Academic CV (comprehensive)
    cv.save_cv(get_versioned_filename(output_dir, "academic", "html"),
               format="html",
               style="academic")
    
    # 4. Technical CV
    cv.save_cv(get_versioned_filename(output_dir, "technical", "md"),
               format="markdown",
               style="technical",
               sections=['profile', 'core_competencies', 'experience', 'certifications'])
    
    print("\nDone! Generated 4 CV versions.")