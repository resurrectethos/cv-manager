import pdfplumber
import re
import json
from collections import defaultdict

PDF_PATH = "/Users/preggyreddy/projects/cv-manager/Profile.pdf"

# Define the major sections we want to capture
SECTION_HEADERS = ["Summary", "Experience", "Education", "Top Skills", "Languages", "Certifications", "Publications"]

def get_section_texts(pdf_path):
    """Extracts text and groups it by document section."""
    section_texts = defaultdict(str)
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract words and sort them by vertical, then horizontal position
            words = sorted(page.extract_words(x_tolerance=2, y_tolerance=2), key=lambda w: (w['top'], w['x0']))
            
            current_section = None
            header_y_pos = 0

            # Find the section for each word based on its position relative to headers
            # This is a simplified approach; a more robust one would find header font sizes
            temp_sections = defaultdict(list)
            for word in words:
                if word['text'] in SECTION_HEADERS and word['x0'] < 100: # Headers are usually on the left
                    current_section = word['text']
                    header_y_pos = word['top']
                    temp_sections[current_section] # Initialize section
                    continue
                
                # Find which section the word belongs to by finding the last header above it
                belongs_to_section = None
                sorted_headers = sorted([(h, y) for h, y in zip(SECTION_HEADERS, [w['top'] for w in words if w['text'] in SECTION_HEADERS and w['x0'] < 100]) if y <= word['top']], key=lambda x: x[1], reverse=True)
                if sorted_headers:
                    belongs_to_section = sorted_headers[0][0]
                
                if belongs_to_section:
                    temp_sections[belongs_to_section].append(word['text'])

            for section, word_list in temp_sections.items():
                section_texts[section] += " " + " ".join(word_list)

    # Clean up extra whitespace
    for section in section_texts:
        section_texts[section] = re.sub(r'\s+', ' ', section_texts[section]).strip()
    return section_texts

def parse_experience(text):
    entries = []
    # Date ranges are the most reliable anchors for splitting job entries
    date_pattern = r'(\w+ \d{4} - (?:Present|\w+ \d{4}))(?: \((.*?)\))?'
    matches = list(re.finditer(date_pattern, text))
    
    for i, match in enumerate(matches):
        start_pos = match.end()
        end_pos = matches[i+1].start() if i + 1 < len(matches) else len(text)
        
        content_block = text[start_pos:end_pos].strip()
        period = match.group(0)

        # The text before the date is the company and title
        header_block = text[:match.start()].strip()
        header_lines = [line.strip() for line in header_block.split('  ') if line.strip()]
        
        if not header_lines:
            continue

        # This is an assumption: last two lines before date are Title and Company
        position = header_lines[-1] if len(header_lines) > 0 else ''
        company = header_lines[-2] if len(header_lines) > 1 else ''

        entries.append({
            "company": company,
            "position": position,
            "period": period,
            "responsibilities": [l.strip() for l in content_block.split('  ') if l.strip()]
        })
        # Remove the processed part of the text to simplify the next iteration
        text = text[end_pos:]

    return entries

def parse_education(text):
    entries = []
    # Date ranges are also good anchors here
    date_pattern = r'(\d{4} - \d{4})'
    matches = list(re.finditer(date_pattern, text))

    for i, match in enumerate(matches):
        # The text between the previous match and this one is the education entry
        start_pos = matches[i-1].end() if i > 0 else 0
        end_pos = match.start()
        content_block = text[start_pos:end_pos].strip()
        period = match.group(1)

        lines = [l.strip() for l in content_block.split('  ') if l.strip()]
        if not lines:
            continue
        
        institution = lines[0]
        degree = ' '.join(lines[1:])

        entries.append({
            "institution": institution,
            "degree": degree,
            "period": period,
            "description": ""
        })
    return entries

def main():
    section_texts = get_section_texts(PDF_PATH)
    cv_data = defaultdict(dict)

    if section_texts.get("Summary"):
        cv_data["profile"]["summary"] = section_texts["Summary"]
    
    if section_texts.get("Top Skills"):
        cv_data["skills"]["technical"] = section_texts["Top Skills"].split(' ')

    if section_texts.get("Experience"):
        cv_data["work_experience"] = parse_experience(section_texts["Experience"])

    if section_texts.get("Education"):
        cv_data["education"] = parse_education(section_texts["Education"])

    output_filename = "cv_data_from_linkedin.json"
    print(f"\nSaving parsed data to {output_filename}...")
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(cv_data, f, indent=4, ensure_ascii=False)
    print("Done.")

if __name__ == "__main__":
    main()