import json
import copy
import yaml
from datetime import datetime, timezone
from thefuzz import fuzz

def load_config(config_path='config.yaml'):
    """Loads the YAML configuration file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def transform_to_merged_format(data, source_name, confidence):
    """Recursively transforms a simple JSON object into the new, rich merged format."""
    timestamp = datetime.now(timezone.utc).isoformat()
    if isinstance(data, dict):
        return {k: transform_to_merged_format(v, source_name, confidence) for k, v in data.items()}
    elif isinstance(data, list):
        return [transform_to_merged_format(item, source_name, confidence) for item in data]
    else:
        return {
            "value": data,
            "source": source_name,
            "timestamp": timestamp,
            "confidence": confidence,
            "conflicts": []
        }

def get_comparison_string(item, item_type):
    """Creates a representative string for an item for fuzzy matching."""
    if not isinstance(item, dict):
        return str(item)
    
    key_fields = {
        'work_experience': ['company', 'position'],
        'education': ['institution', 'degree']
    }
    if item_type not in key_fields:
        return str(item)

    parts = []
    for field in key_fields[item_type]:
        val = item.get(field, '')
        part = val.get('value') if isinstance(val, dict) else val
        parts.append(str(part))
    
    return " ".join(parts).lower()

def merge_sources(merged_data, new_data, source_name, config):
    """Recursively merges a new data source, using fuzzy matching for lists."""
    strategy = config['merging_rules']['strategy']
    new_confidence = config['data_sources'][source_name]['confidence']
    threshold = config['merging_rules']['list_matching_threshold'] * 100

    for key, new_value in new_data.items():
        if key not in merged_data:
            merged_data[key] = transform_to_merged_format(new_value, source_name, new_confidence)
            continue

        merged_node = merged_data[key]
        if isinstance(new_value, dict) and isinstance(merged_node, dict):
            merge_sources(merged_node, new_value, source_name, config)
        elif isinstance(new_value, list) and isinstance(merged_node, list):
            # --- Fuzzy Matching Logic for Lists ---
            unmatched_new_items = []
            for new_item in new_value:
                best_match_score = 0
                best_match_node = None
                new_item_str = get_comparison_string(new_item, key)

                for existing_item in merged_node:
                    existing_item_str = get_comparison_string(existing_item, key)
                    score = fuzz.ratio(new_item_str, existing_item_str)
                    if score > best_match_score:
                        best_match_score = score
                        best_match_node = existing_item

                if best_match_node and best_match_score >= threshold:
                    # Found a confident match, merge this item recursively
                    if isinstance(new_item, dict):
                         merge_sources(best_match_node, new_item, source_name, config)
                else:
                    # No confident match found, add to a temporary list
                    unmatched_new_items.append(new_item)
            
            # Add all unmatched new items to the merged list
            for item in unmatched_new_items:
                merged_node.append(transform_to_merged_format(item, source_name, new_confidence))

        elif isinstance(merged_node, dict) and 'value' in merged_node:
            if merged_node['value'] == new_value:
                continue # No conflict

            # --- Conflict Resolution Logic ---
            if strategy == 'highest_confidence_wins':
                current_confidence = merged_node.get('confidence', 0)
                if new_confidence > current_confidence:
                    old_winner = copy.deepcopy(merged_node)
                    del old_winner['conflicts']
                    merged_node['conflicts'].append(old_winner)
                    
                    merged_node.update({
                        'value': new_value,
                        'source': source_name,
                        'timestamp': datetime.now(timezone.utc).isoformat(),
                        'confidence': new_confidence
                    })
                else:
                    merged_node['conflicts'].append({
                        "value": new_value,
                        "source": source_name,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "confidence": new_confidence
                    })
            else: # Default to 'primary_wins'
                merged_node['conflicts'].append(transform_to_merged_format(new_value, source_name, new_confidence))

def main():
    config = load_config()
    sources = sorted(config['data_sources'].items(), key=lambda item: item[1]['priority'])
    
    primary_source_name, primary_config = sources[0]
    print(f"Loading primary source: {primary_source_name}...")
    try:
        with open(primary_config['path'], 'r') as f:
            primary_data = json.load(f)
    except FileNotFoundError as e:
        print(f"Error: Primary source file not found. {e}")
        return

    print("Transforming primary data as the baseline...")
    merged_data = transform_to_merged_format(primary_data, primary_source_name, primary_config['confidence'])

    for source_name, source_config in sources[1:]:
        print(f"Merging data from {source_name}...")
        try:
            with open(source_config['path'], 'r') as f:
                new_data = json.load(f)
            merge_sources(merged_data, new_data, source_name, config)
        except FileNotFoundError:
            print(f"Warning: Source file not found for '{source_name}'. Skipping.")
            continue

    output_path = config['output']['merged_data']
    print(f"Saving merged data to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, indent=4, ensure_ascii=False)
    
    print("Fuzzy merge complete.")

if __name__ == "__main__":
    main()