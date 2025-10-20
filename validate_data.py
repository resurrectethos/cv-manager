
import json
import yaml

def load_config(config_path='config.yaml'):
    """Loads the YAML configuration file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

class DataValidator:
    """Analyzes the merged CV data to find quality issues and conflicts."""

    def __init__(self, config):
        self.config = config
        self.data_path = self.config['output']['merged_data']
        self.issues = []
        try:
            with open(self.data_path, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = None
            print(f"Error: Merged data file not found at {self.data_path}")

    def validate(self):
        """Runs all validation checks."""
        if not self.data:
            return
        
        print("Starting data validation...")
        self._traverse(self.data)
        print("Validation complete.")

    def _traverse(self, node, path=""):
        """Recursively traverses the data structure to check each node."""
        if isinstance(node, dict):
            # Check for our rich data object structure
            if 'value' in node and 'source' in node:
                self._validate_field(node, path)
            else: # Otherwise, keep traversing
                for key, value in node.items():
                    self._traverse(value, f"{path}.{key}" if path else key)
        
        elif isinstance(node, list):
            # Check for required fields in complex lists
            if path.endswith('work_experience'):
                self._validate_list_items(node, path, ['company', 'position'])
            elif path.endswith('education'):
                self._validate_list_items(node, path, ['institution', 'degree'])

            for i, item in enumerate(node):
                self._traverse(item, f"{path}[{i}]")

    def _validate_field(self, field, path):
        """Validates a single field with the {value, source, ...} structure."""
        # 1. Check for empty or null primary values
        if field['value'] is None or field['value'] == '':
            self.issues.append({
                'type': 'Missing Value',
                'path': path,
                'details': f"The primary value is empty or null. Source: {field['source']}."
            })

        # 2. Check for conflicts
        if field.get('conflicts') and len(field['conflicts']) > 0:
            self.issues.append({
                'type': 'Conflict Found',
                'path': path,
                'details': f"{len(field['conflicts'])} conflicting value(s) exist."
            })

    def _validate_list_items(self, item_list, path, required_fields):
        """Validates that items in a list have certain required fields."""
        for i, item in enumerate(item_list):
            if not isinstance(item, dict):
                continue
            for field_name in required_fields:
                if field_name not in item or item[field_name].get('value') in [None, '']:
                    self.issues.append({
                        'type': 'Missing Required Field',
                        'path': f"{path}[{i}]",
                        'details': f"Entry is missing a value for required field: '{field_name}'."
                    })

    def print_report(self):
        """Prints a formatted summary of all found issues."""
        print("\n--- Data Quality Report ---")
        if not self.issues:
            print("\n✅ No issues found. The data quality looks good!\n")
            return

        # Group issues by type
        grouped_issues = {}
        for issue in self.issues:
            if issue['type'] not in grouped_issues:
                grouped_issues[issue['type']] = []
            grouped_issues[issue['type']].append(issue)

        for issue_type, issues in grouped_issues.items():
            print(f"\n🔸 {issue_type} ({len(issues)} found):")
            for issue in issues:
                print(f"  - Path: {issue['path']}")
                print(f"    Details: {issue['details']}")
        
        print("\n--- End of Report ---\n")

if __name__ == "__main__":
    config = load_config()
    validator = DataValidator(config)
    validator.validate()
    validator.print_report()
