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
├── cv_generator.py                 # Core CV generation
├── cv_cli.py                       # Basic CLI tool
├── cv_master.py                    # Master CLI (all features)
├── cv_pdf_generator.py             # PDF generation
├── cv_skills_matrix.py             # Skills visualizations
├── cv_publication_metrics.py       # Citation tracking
├── cv_cover_letter.py              # Cover letter generator
├── cv_application_tracker.py       # Application tracking
├── requirements.txt                # Dependencies
├── README.md                       # This file
├── output/                         # Generated files
│   ├── pdf/                       # PDF CVs
│   ├── skills/                    # Skill visualizations
│   └── ...
└── templates/                      # Custom templates
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
pip install -r requirements.txt
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
   chmod +x cv_master.py cv_cli.py
   ```

## 💻 Usage

### Master CLI (Recommended)

The easiest way to use all features:

```bash
python cv_master.py
```

This launches an interactive menu with all features:
- CV generation (Markdown, HTML, PDF)
- Skills visualizations
- Publication metrics
- Cover letter creation
- Application tracking

### Quick Commands

```bash
# Generate all CV versions
python cv_master.py --generate-all

# Update publication metrics
python cv_master.py --update-metrics

# Generate skills visualizations
python cv_master.py --skills

# Export everything
python cv_master.py --export
```

## 📄 CV Generation

### Markdown/HTML Generation

```bash
# Research-focused CV
python cv_cli.py generate -s research -f markdown

# Industry CV (condensed)
python cv_cli.py generate -s industry -f html --limit-exp 3

# Custom sections only
python cv_cli.py generate -s technical --sections "profile,skills,experience"
```

### PDF Generation

```bash
# Generate single PDF
python -c "from cv_generator import CVGenerator; from cv_pdf_generator import PDFGenerator; cv = CVGenerator(); pdf = PDFGenerator(cv); pdf.generate_pdf('cv.pdf', style='research')"

# Or use master CLI
python cv_master.py  # Then select option 2
```

### CV Styles

| Style | Best For | Features |
|-------|----------|----------|
| **Research** | Academic positions, grants | Full publications, research emphasis |
| **Industry** | Tech companies, startups | Technical skills first, condensed |
| **Academic** | University positions | Comprehensive, teaching focus |
| **Technical** | IT/Software roles | Skills prominent, project-focused |

## 📊 Skills Visualization

Generate professional visualizations of your skills:

```bash
python cv_skills_matrix.py
```

Generates:
- Horizontal bar charts (by category and overall)
- Radar chart (category comparison)
- Heatmap (skills matrix)

**Customizing Skill Levels:**

Edit `cv_skills_matrix.py`:

```python
skills = SkillsMatrix(cv)
skills.update_skill_level("Python", 5)  # 1-5 scale
skills.generate_all_visualizations()
```

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