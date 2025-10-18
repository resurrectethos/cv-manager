# Complete Workflow Examples

Real-world scenarios showing how to use the CV management system effectively.

## 🎯 Workflow 1: Applying for an Academic Position

**Scenario**: You're applying for a Senior Lecturer position at a university.

### Steps:

```bash
# 1. Update your CV with recent publications (if needed)
python cv_cli.py add publication
# Follow prompts...

# 2. Generate research-focused CV in PDF
python cv_master.py
# Select: 2 (Generate PDF)
# Select: 1 (Research - academic style)
# Output: output/cv_research.pdf

# 3. Generate skills visualization for portfolio
python cv_master.py
# Select: 4 (Generate skills visualizations)
# Creates: output/skills/*.png

# 4. Create tailored cover letter
python cv_cover_letter.py
# Select: 1 (Academic Position)
# Fill in: University name, position, etc.
# Output: cover_letter_academic_YYYYMMDD.txt

# 5. Track the application
python cv_master.py
# Select: 8 (Add new application)
# Position: Senior Lecturer in Digital Education
# Company: Example University
# CV Version: cv_research.pdf
# Cover Letter: cover_letter_academic_20251018.txt
# Deadline: 2025-11-15
# Notes: Found via HigherEd Jobs

# 6. Commit everything
git add .
git commit -m "Applied to Example University - Senior Lecturer"
git push
```

### Two Weeks Later - Follow Up:

```bash
python cv_master.py
# Select: 9 (Update application status)
# Application ID: 1
# New status: under_review
# Notes: Sent follow-up email to Dr. Smith

# Add the follow-up
# Select: 3 (Add follow-up) in next menu
# Method: email
# Notes: Inquired about timeline, expressed continued interest
```

---

## 💼 Workflow 2: Industry Job Application

**Scenario**: Applying for a Learning Experience Designer at a tech company.

### Steps:

```bash
# 1. Generate industry-focused CV (technical, condensed)
python cv_cli.py generate -s industry -f pdf --limit-exp 3

# 2. Create modern HTML version for portfolio
python cv_cli.py generate -s industry -f html \
    --sections "profile,skills,experience,certifications"
# Output: cv_industry.html

# 3. Create industry cover letter
python cv_cover_letter.py
# Select: 2 (Industry Job)
# Company: TechCorp
# Position: Learning Experience Designer
# Why company: "Your innovative approach to AI-powered learning"
# Key achievement: "Implemented Moodle LMS for 35,000 users"
# Technical skills: Moodle, Azure, Learning Analytics

# 4. Track application
python cv_application_tracker.py
# Add application with:
# - Salary range: $80k-100k
# - Location: Remote
# - Job URL: [link from LinkedIn]

# 5. Set reminder for follow-up
# (System will automatically flag in 14 days)
```

---

## 📊 Workflow 3: Annual CV Refresh

**Scenario**: End of year - updating everything for next year's opportunities.

### Steps:

```bash
# 1. Update publication metrics (run overnight)
python cv_publication_metrics.py
# Select: 3 (Full update)
# This fetches: Google Scholar, ORCID, all citations
# Time: 15-30 minutes

# 2. Add this year's achievements
python cv_cli.py add experience
# Or edit cv_data.json directly

python cv_cli.py add publication
# Add all 2025 publications

python cv_cli.py add certification
# Any new certifications

# 3. Update skills matrix
# Edit cv_skills_matrix.py to adjust proficiency levels
python cv_skills_matrix.py
# Generates updated visualizations

# 4. Generate all fresh versions
python cv_master.py --generate-all
# Creates: All CV formats (MD, HTML, PDF) for all styles

# 5. Export everything for backup
python cv_master.py --export
# Creates: CSV exports, JSON exports, all visualizations

# 6. Review application tracker
python cv_master.py
# Select: 10 (View application tracker)
# Review: Success rates, outcomes, areas for improvement

# 7. Commit annual update
git add .
git commit -m "Annual CV update - 2025 achievements"
git tag -a v2025 -m "2025 Annual Version"
git push && git push --tags
```

---

## 🎓 Workflow 4: Conference Presentation

**Scenario**: Presenting at a conference, need updated bio and CV for proceedings.

### Steps:

```bash
# 1. Generate short academic CV (2 pages max)
python cv_cli.py generate -s academic -f pdf \
    --limit-exp 2 \
    --limit-pub 10

# 2. Extract bio from CV data
python -c "
from cv_generator import CVGenerator
cv = CVGenerator()
print(cv.data['profile']['summary'])
" > conference_bio.txt

# 3. Generate publication list only
python cv_cli.py generate -s research -f markdown \
    --sections "publications"
# Output: publication_list.md

# 4. Create presentation-ready skills chart
python -c "
from cv_generator import CVGenerator
from cv_skills_matrix import SkillsMatrix
cv = CVGenerator()
skills = SkillsMatrix(cv)
skills.generate_radar_chart(
    output_file='conference_skills_radar.png'
)
"
```

---

## 🔬 Workflow 5: Research Grant Application

**Scenario**: Applying for a major research grant - need comprehensive documentation.

### Steps:

```bash
# 1. Update all metrics first
python cv_master.py --update-metrics

# 2. Generate comprehensive research CV
python cv_cli.py generate -s research -f pdf
# Include: All publications, full research history

# 3. Export publication metrics
python -c "
from cv_generator import CVGenerator
from cv_publication_metrics import PublicationMetrics
cv = CVGenerator()
metrics = PublicationMetrics(cv)
metrics.export_metrics_to_json('grant_metrics.json')
print(metrics.generate_metrics_summary())
" > grant_metrics_summary.txt

# 4. Create grant proposal cover letter
python cv_cover_letter.py
# Select: 3 (Research Grant)
# Fill in: Grant details, research objectives, etc.

# 5. Generate research impact visualization
python -c "
from cv_generator import CVGenerator
from cv_skills_matrix import SkillsMatrix
cv = CVGenerator()
skills = SkillsMatrix(cv)
skills.generate_horizontal_bar_chart(
    skill_category='research',
    output_file='research_expertise.png'
)
"

# 6. Track grant application
python cv_application_tracker.py
# Type: research
# Track: Submission date, review period, outcome
```

---

## 🌐 Workflow 6: Online Portfolio Update

**Scenario**: Updating your professional website with latest CV and visualizations.

### Steps:

```bash
# 1. Generate web-ready HTML CV
python cv_cli.py generate -s research -f html -o index.html

# 2. Generate all visualizations for portfolio
python cv_master.py --skills

# 3. Create multiple versions for download
python cv_master.py --generate-all

# 4. Set up auto-deployment
git add .
git commit -m "Portfolio update $(date +%Y-%m-%d)"
git push
# Cloudflare Pages automatically rebuilds

# 5. Test live site
# Visit: https://your-cv.pages.dev
```

---

## 📧 Workflow 7: Mass Application Campaign

**Scenario**: Applying to multiple positions simultaneously.

### Steps:

```bash
# 1. Prepare base versions
python cv_master.py --generate-all

# 2. Create application tracker entries
python -c "
from cv_application_tracker import ApplicationTracker
tracker = ApplicationTracker()

positions = [
    ('Position 1', 'Company A', 'academic', 'cv_research.pdf'),
    ('Position 2', 'Company B', 'industry', 'cv_industry.pdf'),
    ('Position 3', 'Company C', 'academic', 'cv_research.pdf'),
]

for pos, company, type, cv in positions:
    tracker.add_application(
        position=pos,
        company=company,
        application_type=type,
        cv_version=cv
    )
"

# 3. Generate custom cover letters
for company in CompanyA CompanyB CompanyC; do
    python cv_cover_letter.py
    # Save as: cover_letter_${company}.txt
done

# 4. Set up follow-up schedule
python -c "
from cv_application_tracker import ApplicationTracker
tracker = ApplicationTracker()
apps = tracker.get_applications_needing_followup(days=7)
for app in apps:
    print(f'{app[\"id\"]}: {app[\"company\"]} - Follow up by: ...')
"
```

---

## 🔄 Workflow 8: Post-Interview Follow-Up

**Scenario**: You've had an interview - tracking next steps.

### Steps:

```bash
# 1. Record interview details
python cv_application_tracker.py
# Select: Add interview
# Application ID: 5
# Interview date: 2025-10-20
# Type: panel
# Interviewers: Dr. Smith, Prof. Jones, Dr. Williams
# Notes: Focused on research plans, teaching philosophy

# 2. Update status
python cv_master.py
# Select: 9 (Update status)
# ID: 5
# Status: interviewed
# Notes: Positive feedback, discussed start date

# 3. Send thank you and track it
python cv_master.py
# Select: Follow-up
# Method: email
# Notes: Sent thank you to all panel members

# 4. Check for other applications needing attention
python cv_master.py
# Select: 11 (Applications needing follow-up)
```

---

## 💾 Workflow 9: Backing Up Everything

**Scenario**: Regular backup routine (monthly recommended).

### Steps:

```bash
# 1. Export all tracking data
python cv_master.py --export

# 2. Commit to Git
git add .
git commit -m "Monthly backup - $(date +%Y-%m)"

# 3. Create archive
DATE=$(date +%Y%m%d)
tar -czf "cv_backup_${DATE}.tar.gz" \
    cv_data.json \
    applications_tracker.json \
    publication_metrics.json \
    output/

# 4. Upload to cloud storage
# (use your preferred method: Dropbox, Google Drive, etc.)

# 5. Push to remote repository
git push

# 6. Create monthly tag
git tag -a "backup-$(date +%Y-%m)" -m "Monthly backup"
git push --tags
```

---

## 🎨 Workflow 10: Customizing for Specific Country/Region

**Scenario**: Adapting CV for EU Europass format.

### Steps:

```python
# Create custom generator: cv_europass.py

from cv_generator import CVGenerator

class EuropassGenerator(CVGenerator):
    def generate_europass(self):
        # Custom Europass format
        ep = []
        ep.append("CURRICULUM VITAE")
        ep.append("\nPERSONAL INFORMATION")
        ep.append(f"Name: {self.data['personal_info']['name']}")
        # ... add Europass-specific sections
        
        return "\n".join(ep)

# Usage:
cv = EuropassGenerator()
europass_cv = cv.generate_europass()
with open('cv_europass.txt', 'w') as f:
    f.write(europass_cv)
```

---

## 📊 Pro Tips for All Workflows

1. **Always commit before and after**: Track every change
2. **Use descriptive filenames**: Include date and purpose
3. **Test before sending**: Preview all generated files
4. **Keep tracker updated**: Log applications immediately
5. **Set reminders**: Use system for follow-up timing
6. **Regular exports**: Backup tracker data monthly
7. **Version your CVs**: Tag important versions in Git
8. **Customize per role**: Never send generic CVs
9. **Update metrics quarterly**: Keep citations current
10. **Review analytics**: Learn from application success rates

---

**Choose the workflow that matches your need, or mix and match steps!** 🚀