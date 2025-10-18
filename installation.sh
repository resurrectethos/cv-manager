mkdir cv-manager && cd cv-manager
python -m venv venv
source venv/bin/activate
pip install weasyprint markdown2 matplotlib numpy scholarly requests
# Add all the .py files
python cv_master.py