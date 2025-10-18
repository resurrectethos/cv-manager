import requests
import json

# Your ORCID ID
ORCID_ID = "0000-0002-7350-1987"
API_BASE_URL = f"https://pub.orcid.org/v3.0/{ORCID_ID}"
HEADERS = {'Accept': 'application/json'}

def fetch_data(endpoint):
    """Fetches data from a specific ORCID API endpoint."""
    url = f"{API_BASE_URL}/{endpoint}"
    print(f"Fetching {url}...")
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

def map_to_cv_format(person_data, works_data, education_data, employment_data):
    """Maps the fetched ORCID data to the target cv_data.json format."""
    
    cv_data = {
        "personal_info": {},
        "profile": {},
        "education": [],
        "work_experience": [],
        "skills": {},
        "certifications": [],
        "memberships": [],
        "hobbies": [],
        "publications": {
            "book_chapters": [],
            "conference_proceedings": [],
            "journal_articles": [],
            "other": []
        },
        "referees": []
    }

    # --- Map Personal Info ---
    if person_data:
        name_info = person_data.get('name', {})
        cv_data["personal_info"] = {
            "name": f"{name_info.get('given-names', {}).get('value', '')} {name_info.get('family-name', {}).get('value', '')}".strip(),
            "title": "",
            "phone": "",
            "email": next((email['email'] for email in person_data.get('emails', {}).get('email', []) if email['primary']), ""),
            "websites": [url['url']['value'] for url in person_data.get('researcher-urls', {}).get('researcher-url', [])],
            "location": ""
        }

    # --- Map Education ---
    if education_data:
        for edu in education_data.get('affiliation-group', []):
            summary = edu.get('summaries', [{}])[0].get('education-summary')
            if summary:
                cv_data["education"].append({
                    "institution": summary.get('organization', {}).get('name', ''),
                    "degree": summary.get('role-title', ''),
                    "period": f"{((summary.get('start-date') or {}).get('year') or {}).get('value', '')} - {((summary.get('end-date') or {}).get('year') or {}).get('value', 'Present')}",
                    "description": summary.get('department-name', ''),
                    "distinction": False
                })

    # --- Map Work Experience ---
    if employment_data:
        for emp in employment_data.get('affiliation-group', []):
            summary = emp.get('summaries', [{}])[0].get('employment-summary')
            if summary:
                cv_data["work_experience"].append({
                    "company": summary.get('organization', {}).get('name', ''),
                    "position": summary.get('role-title', ''),
                    "period": f"{((summary.get('start-date') or {}).get('year') or {}).get('value', '')} - {((summary.get('end-date') or {}).get('year') or {}).get('value', 'Present')}",
                    "responsibilities": [summary.get('department-name', '')]
                })

    # --- Map Publications (Corrected Logic) ---
    if works_data:
        for work_group in works_data.get('group', []):
            summary = work_group.get('work-summary', [{}])[0]
            put_code = summary.get('put-code')
            if not put_code:
                continue

            # Fetch the full details for this specific work to get contributors
            work_details = fetch_data(f"work/{put_code}")
            if not work_details:
                continue

            pub_type = work_details.get('type', 'other').lower().replace("_", "-")
            title = ((work_details.get('title') or {}).get('title') or {}).get('value', 'No Title')
            year = ((work_details.get('publication-date') or {}).get('year') or {}).get('value', '')

            authors = []
            contributors = (work_details.get('contributors') or {}).get('contributor', [])
            for contributor in contributors:
                if contributor.get('credit-name') and contributor['credit-name'].get('value'):
                    authors.append(contributor['credit-name']['value'])

            doi_eids = (work_details.get('external-ids') or {}).get('external-id', [])
            doi = None
            if doi_eids:
                doi = next((eid.get('external-id-value') for eid in doi_eids if eid.get('external-id-type') == 'doi'), None)

            publication_entry = {
                "title": title,
                "year": year,
                "authors": authors,
                "doi": doi
            }

            if "conference" in pub_type:
                cv_data["publications"]["conference_proceedings"].append(publication_entry)
            elif "book-chapter" in pub_type:
                cv_data["publications"]["book_chapters"].append(publication_entry)
            elif "journal-article" in pub_type:
                cv_data["publications"]["journal_articles"].append(publication_entry)
            else:
                cv_data["publications"]["other"].append(publication_entry)

    return cv_data

def main():
    """Main function to run the ORCID importer."""
    print(f"Starting ORCID data import for ID: {ORCID_ID}")
    
    person_data = fetch_data('person')
    works_data = fetch_data('works')
    education_data = fetch_data('educations')
    employment_data = fetch_data('employments')

    if not all([person_data, works_data, education_data, employment_data]):
        print("Could not fetch all required data from ORCID. Aborting.")
        return

    print("\nMapping fetched data to CV format...")
    cv_json_data = map_to_cv_format(person_data, works_data, education_data, employment_data)

    output_filename = "cv_data_from_orcid.json"
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(cv_json_data, f, indent=4, ensure_ascii=False)
        print(f"\nSuccessfully created '{output_filename}'")
    except IOError as e:
        print(f"Error writing to file {output_filename}: {e}")

if __name__ == "__main__":
    main()