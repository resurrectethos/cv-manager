# Quick Start Guide - Get Running in 5 Minutes

## 🚀 Super Fast Setup

### Step 1: Install (2 minutes)

```bash
# Create directory and navigate
mkdir cv-manager && cd cv-manager

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r enhanced_requirements.txt
```

### Step 2: Add Files (1 minute)

1. Save all the Python files (`.py`) to the `cv-manager` folder
2. Save `cv_data.json` to the same folder
3. Create `output` folder: `mkdir output`

### Step 3: First Run (2 minutes)

```bash
# Launch master interface
python cv_master.py

# Or try generating a CV immediately
python cv_cli.py generate -s research -f markdown
```

That's it! You now have a working CV management system.

## 📋 Your First Tasks

### Task 1: Generate Your First CV
```bash
python cv_cli.py generate -s research -f markdown -o my_first_cv.md
```

### Task 2: Create a PDF
```bash
python cv_master.py
# Select option 2 → Select style → Done!
```

### Task 3: Track an Application
```bash
python cv_master.py
# Select option 8 → Fill in details → Done!
```

## 🎯 Most Common Commands

```bash
# Interactive menu (easiest)
python cv_master.py

# Generate all CV versions
python cv_master.py --generate-all

# Add new work experience
python cv_cli.py add experience

# View CV summary
python cv_cli.py summary

# Create cover letter
python cv_cover_letter.py
```

## 📝 Quick Edits

To update your CV data, just edit `cv_data.json` in VS Code or any text editor.

**Most common updates:**
- Add work experience → Edit `work_experience` array
- Add publication → Edit `publications` object
- Update contact → Edit `personal_info` object

## 🆘 Quick Troubleshooting

**"Module not found"**
```bash
# Make sure virtual environment is active
source venv/bin/activate

# Reinstall
pip install -r requirements.txt
```

**"File not found"**
```bash
# Make sure you're in the right directory
pwd  # Should show cv-manager path
ls   # Should show cv_*.py files
```

**"JSON error"**
- Check for missing commas in `cv_data.json`
- Use VS Code for syntax highlighting
- Validate at jsonlint.com

## 💡 Pro Tips

1. **Start Simple**: Use the basic CLI first, then explore advanced features
2. **Git Early**: Run `git init` and commit your first version
3. **Update Often**: Set a reminder to update monthly
4. **Test First**: Always preview before sending
5. **Use Templates**: Start with existing formats, customize later

## 📚 Next Steps

Once comfortable:
1. Read the full README.md for advanced features
2. Customize `cv_data.json` completely
3. Set up publication metrics tracking
4. Create custom templates
5. Deploy to Cloudflare Pages

## 🎓 Learning Path

**Week 1**: Basic CV generation  
**Week 2**: Add application tracking  
**Week 3**: Set up publication metrics  
**Week 4**: Customize templates and styles  

---

**You're ready to go! Start with `python cv_master.py` 🚀**