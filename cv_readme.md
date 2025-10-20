# CV Management System - Complete Suite

A comprehensive, JSON-based CV management system with advanced features including PDF generation, skills visualization, publication metrics tracking, cover letter generation, and application tracking.

## 🌟 Features Overview

### Core Features
✨ **Single Source of Truth**: All CV data in one structured JSON file  
🎯 **Multiple Audiences**: Generate research, industry, academic, or technical versions  
📝 **Easy Updates**: CLI tools for quick additions and modifications  
🔄 **Version Control**: Track changes with Git  

### Advanced Features
📄 **PDF Generation**: Professional PDF CVs with custom styling  
📊 **Skills Visualization**: Interactive charts, radar plots, and heatmaps  
📈 **Publication Metrics**: Auto-fetch citations from Google Scholar & ORCID  
✉️ **Cover Letters**: Template-based cover letter generation  
📋 **Application Tracking**: Complete job application management system  

## 📁 Project Structure

```
cv-manager/
├── cv_data.json                    # Your CV data (single source)
├── cv_master.py                    # Master CLI (all features)
├── cv_generator.py                 # Core CV generation
├── cv_pdf_generator.py             # PDF generation
├── cv_skills_matrix.py             # Skills visualizations
├── cv_publication_metrics.py       # Citation tracking
├── cv_cover_letter.py              # Cover letter generator
├── cv_application_tracker.py       # Application tracking
├── enhanced_requirements.txt       # Dependencies
├── README.md                       # This file
├── documents/                      # Generated files (PDF, HTML, MD)
└── templates/
    ├── cv_template.html.jinja
    └── style.css                   # Stylesheet for HTML CVs
```

## 🚀 Installation & Setup

### 1. Prerequisites

- Python 3.8 or higher
- VS Code (recommended)
- Git

### 2. Initial Setup

```bash
# Create project directory
mkdir cv-manager
cd cv-manager

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r enhanced_requirements.txt
```

### 3. VS Code Setup

```bash
# Open in VS Code
code .

# Install recommended extensions:
# - Python (Microsoft)
# - JSON (built-in)
# - Markdown Preview Enhanced
# - GitLens
```

### 4. Initialize Data

1. Save all the provided Python files to your project directory
2. Save `cv_data.json` with your information
3. Make scripts executable (Mac/Linux):
   ```bash
   chmod +x cv_master.py
   ```

## 💻 Usage

### Master CLI (Recommended)

The easiest way to use all features:

```bash
python cv_master.py -i
```

This launches an interactive menu with all features:
- CV generation (Markdown, HTML, PDF)
- And other features...

### Quick Commands

```bash
# Generate a research-focused CV in markdown format
python cv_master.py generate -s research -f markdown

# Generate an industry-focused CV in html format with limited entries
python cv_master.py generate -s industry -f html --limit-exp 3

# Generate a technical CV in pdf format
python cv_master.py generate -s technical -f pdf
```

## 📄 CV Generation

### Markdown/HTML/PDF Generation

Generation is handled via the master CLI.

```bash
# Research-focused CV
python cv_master.py generate -s research -f markdown

# Industry CV (condensed)
python cv_master.py generate -s industry -f html --limit-exp 3

# Custom sections only
python cv_master.py generate -s technical --sections "profile,core_competencies,experience"

# PDF Generation
python cv_master.py generate -s academic -f pdf
```

### CV Styles

| Style | Best For | Features |
|---|---|---|
| **Hybrid** | Independent Contractor | Balanced strategic and technical focus. **(New Default)** |
| **Research** | Academic positions, grants | Full publications, research emphasis |
| **Industry** | Tech companies, startups | Technical skills first, condensed |
| **Academic** | University positions | Comprehensive, teaching focus |
| **Technical** | IT/Software roles | Skills prominent, project-focused, reordered sections |

## 📈 Publication Metrics

Auto-fetch citation counts and metrics:

```bash
python cv_publication_metrics.py
```

Features:
- Google Scholar profile metrics (h-index, citations)
- Individual publication citations
- ORCID integration
- Metrics export to JSON
- Enhanced CV data with citation counts

**Important**: Fetching all publications can take 10-30 minutes due to rate limiting.

### Usage Example

```python
from cv_publication_metrics import PublicationMetrics
from cv_generator import CVGenerator

cv = CVGenerator()
metrics = PublicationMetrics(cv)

# Fetch Google Scholar profile
metrics.fetch_google_scholar_profile()

# Fetch citations for all publications (slow)
metrics.fetch_all_publication_metrics()

# View summary
print(metrics.generate_metrics_summary())

# Add to CV data
metrics.add_metrics_to_cv_data()
```

## ✉️ Cover Letter Generation

Create customized cover letters from templates:

```bash
python cv_cover_letter.py
```

Available templates:
- Academic positions
- Industry jobs
- Research grants
- Consulting proposals

The generator automatically pulls relevant data from your CV (experience, publications, skills) and prompts you for position-specific information.

### Programmatic Usage

```python
from cv_cover_letter import CoverLetterGenerator

cover_letter = CoverLetterGenerator(cv)

custom_fields = {
    "position": "Senior Researcher",
    "institution": "University Name",
    "why_institution": "Your cutting-edge AI research",
    # ... other fields
}

letter = cover_letter.generate_cover_letter(
    template_type="academic",
    custom_fields=custom_fields,
    output_file="cover_letter.txt"
)
```

## 📋 Application Tracking

Track job applications, follow-ups, and outcomes:

```bash
python cv_application_tracker.py
```

Features:
- Track multiple applications
- Record interviews and follow-ups
- Status updates
- Deadline reminders
- Export to CSV
- Analytics