
import json
import copy

# Define file paths
ORIGINAL_PATH = "cv_data.json"
LINKEDIN_PATH = "cv_data_from_linkedin.json"
ORCID_PATH = "cv_data_from_orcid.json"
OUTPUT_PATH = "cv_data_merged.json"

def transform_to_merged_format(data, source_name):
    """Recursively transforms a simple JSON object into the new merged format."""
    if isinstance(data, dict):
        new_dict = {}
        for k, v in data.items():
            new_dict[k] = transform_to_merged_format(v, source_name)
        return new_dict
    elif isinstance(data, list):
        return [transform_to_merged_format(item, source_name) for item in data]
    else:
        return {"value": data, "source": source_name, "conflicts": []}

def get_item_key(item, item_type):
    """Creates a unique key for an item in a list, handling both simple and merged formats."""
    if not isinstance(item, dict):
        return str(item)

    if item_type == 'work_experience':
        company_val = item.get('company', '')
        company = company_val.get('value') if isinstance(company_val, dict) else company_val
        position_val = item.get('position', '')
        position = position_val.get('value') if isinstance(position_val, dict) else position_val
        return f"{company}_{position}".lower()

    if item_type == 'education':
        institution_val = item.get('institution', '')
        institution = institution_val.get('value') if isinstance(institution_val, dict) else institution_val
        degree_val = item.get('degree', '')
        degree = degree_val.get('value') if isinstance(degree_val, dict) else degree_val
        return f"{institution}_{degree}".lower()

    return str(item) # Fallback

def merge_sources(merged_data, new_data, source_name):
    """Recursively merges a new data source into the merged_data structure."""
    for key, new_value in new_data.items():
        if key not in merged_data:
            # New key, simply add it after transforming
            merged_data[key] = transform_to_merged_format(new_value, source_name)
            continue

        merged_value = merged_data[key]

        if isinstance(new_value, dict) and isinstance(merged_value, dict):
            # Recurse into dictionaries
            merge_sources(merged_value, new_value, source_name)
        elif isinstance(new_value, list) and isinstance(merged_value, list):
            # Handle list merging (the complex part)
            merged_items_map = {get_item_key(item, key): item for item in merged_value}
            for item in new_value:
                item_key = get_item_key(item, key)
                if item_key in merged_items_map:
                    # Existing item, merge it recursively
                    merge_sources(merged_items_map[item_key], item, source_name)
                else:
                    # New item, add to the list
                    merged_value.append(transform_to_merged_format(item, source_name))
        elif isinstance(merged_value, dict) and 'value' in merged_value:
            # This is a leaf node in our merged structure
            if merged_value['value'] != new_value:
                # Conflict detected!
                is_duplicate_conflict = any(
                    c['value'] == new_value and c['source'] == source_name 
                    for c in merged_value['conflicts']
                )
                if not is_duplicate_conflict:
                    merged_value['conflicts'].append({"value": new_value, "source": source_name})

def main():
    """Main function to load, merge, and save the data."""
    print("Starting data merge...")
    # Load all data sources
    try:
        with open(ORIGINAL_PATH, 'r') as f:
            original_data = json.load(f)
        with open(LINKEDIN_PATH, 'r') as f:
            linkedin_data = json.load(f)
        with open(ORCID_PATH, 'r') as f:
            orcid_data = json.load(f)
    except FileNotFoundError as e:
        print(f"Error: Could not find a source file. {e}")
        return

    # 1. Transform the original data to be the base of our merged structure
    print("Transforming original data as the baseline...")
    merged_data = transform_to_merged_format(original_data, "original")

    # 2. Merge in LinkedIn data
    print("Merging data from LinkedIn...")
    merge_sources(merged_data, linkedin_data, "linkedin")

    # 3. Merge in ORCID data
    print("Merging data from ORCID...")
    merge_sources(merged_data, orcid_data, "orcid")

    # 4. Save the final merged file
    print(f"Saving merged data to {OUTPUT_PATH}...")
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, indent=4, ensure_ascii=False)
    
    print("Merge complete.")

if __name__ == "__main__":
    main()
