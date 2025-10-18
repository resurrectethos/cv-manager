"""
Cover Letter Generator Module
Creates customized cover letters using CV data and templates
"""

import json
from datetime import datetime
from pathlib import Path
from cv_generator import CVGenerator


class CoverLetterGenerator:
    """Generate customized cover letters based on CV data and templates."""
    
    TEMPLATES = {
        "academic": """
{date}

{recipient_name}
{recipient_title}
{institution}
{address}

Dear {salutation},

RE: Application for {position}

I am writing to express my strong interest in the {position} position at {institution}. With a {highest_degree} in {degree_field} and over {years_experience} years of experience in {primary_expertise}, I am confident that my background aligns exceptionally well with your requirements.

{custom_paragraph_1}

My research focuses on {research_focus}, and I have published extensively in this area, including {notable_publications}. At my current position at {current_institution}, I have {key_achievement_1}. Additionally, {key_achievement_2}.

{custom_paragraph_2}

I am particularly drawn to {institution} because {why_institution}. I believe my expertise in {expertise_1}, {expertise_2}, and {expertise_3} would contribute significantly to your department's mission.

{custom_paragraph_3}

I have enclosed my CV, which provides additional details about my qualifications and achievements. I would welcome the opportunity to discuss how my experience and vision align with the needs of your institution.

Thank you for considering my application. I look forward to hearing from you.

Yours sincerely,

{signature}
{name}
{current_title}
{email}
{phone}
        """,
        
        "industry": """
{date}

{recipient_name}
{recipient_title}
{company}
{address}

Dear {salutation},

RE: Application for {position}

I am excited to apply for the {position} role at {company}. With {years_experience} years of experience in {primary_expertise} and a proven track record of {key_strength}, I am confident I can make an immediate impact on your team.

{custom_paragraph_1}

In my current role as {current_position} at {current_institution}, I have successfully {key_achievement_1}. This experience has given me deep expertise in {technical_skill_1}, {technical_skill_2}, and {technical_skill_3}, which I understand are critical for success in this position.

{custom_paragraph_2}

What particularly excites me about {company} is {why_company}. I am impressed by {company_achievement}, and I believe my background in {relevant_experience} would enable me to contribute meaningfully to your continued success.

{custom_paragraph_3}

I would welcome the opportunity to discuss how my skills and experience align with your needs. Please find my CV attached for your review.

Thank you for your consideration. I look forward to speaking with you soon.

Best regards,

{signature}
{name}
{email}
{phone}
        """,
        
        "research_grant": """
{date}

{recipient_name}
{funding_body}
{address}

Dear {salutation},

RE: Application for {grant_name}

I am writing to apply for the {grant_name} to support my research on {research_topic}. As a researcher with expertise in {research_area}, I believe this funding would enable significant advances in {field_impact}.

{custom_paragraph_1}

My research background includes {research_experience}, and I have published {publication_count} peer-reviewed papers in this domain, including {notable_publications}. My work has been recognized through {recognition}.

{custom_paragraph_2}

The proposed research aims to {research_objective}. This project builds on my previous work in {previous_work} and addresses a critical gap in {research_gap}. The expected outcomes include {outcomes}.

{custom_paragraph_3}

With access to {resources} at {institution} and my established track record in {expertise}, I am well-positioned to successfully complete this research. I have secured support from {collaborators}, and the project timeline is realistic and achievable.

Thank you for considering this application. I am happy to provide any additional information you may require.

Yours sincerely,

{signature}
{name}
{current_title}
{institution}
{email}
        """,
        
        "consulting": """
{date}

{recipient_name}
{recipient_title}
{company}
{address}

Dear {salutation},

RE: {service_type} Services for {project}

I am pleased to submit this proposal for {service_type} services to support {project}. With over {years_experience} years of specialized experience in {expertise_area}, I can provide the expertise needed to achieve your objectives.

{custom_paragraph_1}

My relevant experience includes:
• {key_qualification_1}
• {key_qualification_2}
• {key_qualification_3}

{custom_paragraph_2}

I have successfully delivered similar projects for {previous_clients}, achieving {results}. My approach combines {methodology_1} with {methodology_2} to ensure {outcome}.

{custom_paragraph_3}

I propose a {duration} engagement with deliverables including {deliverables}. My daily rate is {rate}, and I can begin work on {start_date}.

I would be delighted to discuss this opportunity further and answer any questions you may have.

Best regards,

{signature}
{name}
{credentials}
{email}
{phone}
        """
    }
    
    def __init__(self, cv_generator: CVGenerator):
        """Initialize with CV generator."""
        self.cv = cv_generator
        self.data = cv_generator.data
    
    def _extract_cv_defaults(self) -> dict:
        """Extract default values from CV data."""
        defaults = {
            "name": self.data['personal_info']['name'],
            "email": self.data['personal_info']['email'],
            "phone": self.data['personal_info']['phone'],
            "current_title": self.data['personal_info']['title'],
            "date": datetime.now().strftime("%d %B %Y"),
            "signature": "",  # Leave blank for digital signature
        }
        
        # Get current position
        if self.data['work_experience']:
            current = self.data['work_experience'][0]
            defaults["current_position"] = current['position']
            defaults["current_institution"] = current['company']
        
        # Get education
        if self.data['education']:
            phd = self.data['education'][0]
            defaults["highest_degree"] = phd['degree']
            defaults["degree_field"] = phd['degree'].split(':')[-1].strip()
        
        # Calculate years of experience
        if self.data['work_experience']:
            start_year = int(self.data['work_experience'][-1]['period'].split('-')[0])
            current_year = datetime.now().year
            defaults["years_experience"] = current_year - start_year
        
        # Get expertise areas
        if 'pedagogical' in self.data['skills']:
            defaults["primary_expertise"] = "Technology-Enhanced Learning and Digital Education"
            defaults["research_focus"] = ", ".join(self.data['profile']['expertise'][:2])
        
        # Get skills
        all_skills = []
        for category in self.data['skills'].values():
            all_skills.extend(category[:3])
        
        defaults["expertise_1"] = all_skills[0] if len(all_skills) > 0 else "digital education"
        defaults["expertise_2"] = all_skills[1] if len(all_skills) > 1 else "learning analytics"
        defaults["expertise_3"] = all_skills[2] if len(all_skills) > 2 else "educational technology"
        
        # Get publications count
        defaults["publication_count"] = len(self.data['publications']['conference_proceedings']) + \
                                       len(self.data['publications']['book_chapters'])
        
        # Get notable publications (most recent)
        recent_pubs = self.data['publications']['conference_proceedings'][:2]
        if recent_pubs:
            defaults["notable_publications"] = " and ".join([
                f'"{pub["title"]}" ({pub["year"]})'
                for pub in recent_pubs
            ])
        
        return defaults
    
    def generate_cover_letter(self,
                            template_type: str = "academic",
                            custom_fields: dict = None,
                            output_file: str = None) -> str:
        """
        Generate a cover letter from template.
        
        Args:
            template_type: Type of letter (academic, industry, research_grant, consulting)
            custom_fields: Dictionary of custom field values
            output_file: Optional file to save the letter
        
        Returns:
            Generated cover letter text
        """
        if template_type not in self.TEMPLATES:
            raise ValueError(f"Unknown template type: {template_type}")
        
        # Get defaults from CV
        fields = self._extract_cv_defaults()
        
        # Override with custom fields
        if custom_fields:
            fields.update(custom_fields)
        
        # Generate letter
        template = self.TEMPLATES[template_type]
        
        try:
            letter = template.format(**fields)
        except KeyError as e:
            missing_field = str(e).strip("'")
            print(f"⚠️  Missing required field: {missing_field}")
            print(f"Please provide this field in custom_fields or add a default.")
            fields[missing_field] = f"[{missing_field.upper()}]"
            letter = template.format(**fields)
        
        # Save if requested
        if output_file:
            with open(output_file, 'w') as f:
                f.write(letter)
            print(f"✓ Cover letter saved to {output_file}")
        
        return letter
    
    def interactive_cover_letter(self):
        """Interactive cover letter generation."""
        print("\n=== Cover Letter Generator ===\n")
        print("Select template type:")
        print("1. Academic Position")
        print("2. Industry Job")
        print("3. Research Grant")
        print("4. Consulting Proposal")
        
        choice = input("\nTemplate (1-4): ").strip()
        template_map = {
            "1": "academic",
            "2": "industry",
            "3": "research_grant",
            "4": "consulting"
        }
        template_type = template_map.get(choice, "academic")
        
        print(f"\n=== {template_type.title()} Letter ===\n")
        
        # Get required fields
        custom_fields = {}
        
        # Common fields
        custom_fields["recipient_name"] = input("Recipient name: ")
        custom_fields["recipient_title"] = input("Recipient title: ")
        
        if template_type == "academic":
            custom_fields["institution"] = input("Institution: ")
            custom_fields["address"] = input("Address (optional): ") or ""
            custom_fields["position"] = input("Position title: ")
            custom_fields["salutation"] = input("Salutation (e.g., 'Professor Smith'): ")
            
            print("\nCustom paragraphs (press Enter for default):")
            custom_fields["custom_paragraph_1"] = input("Paragraph 1: ") or \
                "I bring a unique combination of technical expertise and pedagogical innovation to this role."
            custom_fields["custom_paragraph_2"] = input("Paragraph 2: ") or \
                "I am committed to excellence in both teaching and research."
            custom_fields["custom_paragraph_3"] = input("Paragraph 3: ") or \
                "I am enthusiastic about the opportunity to contribute to your institution."
            
            custom_fields["why_institution"] = input("Why this institution?: ")
            custom_fields["key_achievement_1"] = input("Key achievement 1: ")
            custom_fields["key_achievement_2"] = input("Key achievement 2: ")
            
        elif template_type == "industry":
            custom_fields["company"] = input("Company: ")
            custom_fields["address"] = input("Address (optional): ") or ""
            custom_fields["position"] = input("Position title: ")
            custom_fields["salutation"] = input("Salutation (e.g., 'Hiring Manager'): ")
            
            custom_fields["custom_paragraph_1"] = input("Paragraph 1 (Enter for default): ") or \
                "My experience directly aligns with your requirements."
            custom_fields["custom_paragraph_2"] = input("Paragraph 2 (Enter for default): ") or \
                "I am excited about the opportunity to bring my skills to your team."
            custom_fields["custom_paragraph_3"] = input("Paragraph 3 (Enter for default): ") or \
                "I am confident I can make an immediate impact."
            
            custom_fields["why_company"] = input("Why this company?: ")
            custom_fields["company_achievement"] = input("Company achievement you admire: ")
            custom_fields["key_achievement_1"] = input("Your key achievement: ")
            custom_fields["key_strength"] = input("Your key strength: ")
            custom_fields["technical_skill_1"] = input("Technical skill 1: ")
            custom_fields["technical_skill_2"] = input("Technical skill 2: ")
            custom_fields["technical_skill_3"] = input("Technical skill 3: ")
            custom_fields["relevant_experience"] = input("Relevant experience: ")
        
        elif template_type == "research_grant":
            custom_fields["funding_body"] = input("Funding body: ")
            custom_fields["address"] = input("Address (optional): ") or ""
            custom_fields["grant_name"] = input("Grant name: ")
            custom_fields["research_topic"] = input("Research topic: ")
            custom_fields["salutation"] = input("Salutation: ") or "Selection Committee"
            
            custom_fields["research_area"] = input("Research area: ")
            custom_fields["field_impact"] = input("Field impact: ")
            custom_fields["research_experience"] = input("Research experience summary: ")
            custom_fields["recognition"] = input("Recognition received: ")
            custom_fields["research_objective"] = input("Research objective: ")
            custom_fields["previous_work"] = input("Previous work: ")
            custom_fields["research_gap"] = input("Research gap addressed: ")
            custom_fields["outcomes"] = input("Expected outcomes: ")
            custom_fields["resources"] = input("Resources available: ")
            custom_fields["collaborators"] = input("Collaborators: ")
            custom_fields["institution"] = self.data['work_experience'][0]['company']
            
            custom_fields["custom_paragraph_1"] = ""
            custom_fields["custom_paragraph_2"] = ""
            custom_fields["custom_paragraph_3"] = ""
        
        elif template_type == "consulting":
            custom_fields["company"] = input("Company/Client: ")
            custom_fields["address"] = input("Address (optional): ") or ""
            custom_fields["service_type"] = input("Service type (e.g., 'Consulting'): ")
            custom_fields["project"] = input("Project name: ")
            custom_fields["salutation"] = input("Salutation: ")
            custom_fields["expertise_area"] = input("Expertise area: ")
            
            custom_fields["key_qualification_1"] = input("Key qualification 1: ")
            custom_fields["key_qualification_2"] = input("Key qualification 2: ")
            custom_fields["key_qualification_3"] = input("Key qualification 3: ")
            custom_fields["previous_clients"] = input("Previous similar clients: ")
            custom_fields["results"] = input("Results achieved: ")
            custom_fields["methodology_1"] = input("Methodology 1: ")
            custom_fields["methodology_2"] = input("Methodology 2: ")
            custom_fields["outcome"] = input("Expected outcome: ")
            custom_fields["duration"] = input("Engagement duration: ")
            custom_fields["deliverables"] = input("Deliverables: ")
            custom_fields["rate"] = input("Rate (optional): ") or "[RATE]"
            custom_fields["start_date"] = input("Start date: ")
            custom_fields["credentials"] = input("Credentials (e.g., 'PhD, MTech'): ")
            
            custom_fields["custom_paragraph_1"] = ""
            custom_fields["custom_paragraph_2"] = ""
            custom_fields["custom_paragraph_3"] = ""
        
        # Generate letter
        output_file = f"cover_letter_{template_type}_{datetime.now().strftime('%Y%m%d')}.txt"
        letter = self.generate_cover_letter(template_type, custom_fields, output_file)
        
        print(f"\n{'='*60}")
        print("PREVIEW:")
        print('='*60)
        print(letter)
        print('='*60)
        
        return letter
    
    def save_template(self, name: str, template: str, templates_dir: str = "templates"):
        """Save a custom template."""
        Path(templates_dir).mkdir(exist_ok=True)
        with open(f"{templates_dir}/{name}.txt", 'w') as f:
            f.write(template)
        print(f"✓ Template saved: {templates_dir}/{name}.txt")
    
    def load_custom_template(self, template_file: str) -> str:
        """Load a custom template from file."""
        with open(template_file, 'r') as f:
            return f.read()


# Standalone usage
if __name__ == "__main__":
    cv = CVGenerator()
    cover_letter = CoverLetterGenerator(cv)
    
    # Run interactive mode
    cover_letter.interactive_cover_letter()