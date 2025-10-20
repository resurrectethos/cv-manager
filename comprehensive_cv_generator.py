
import json
import yaml
from jinja2 import Environment, FileSystemLoader
import os

class ComprehensiveCVGenerator:
    """A modern CV generator using a templating engine and external config."""

    def __init__(self, config_path='config.yaml'):
        """Initializes the generator by loading config and setting up the template environment."""
        print("Initializing comprehensive CV generator...")
        self.config = self._load_config(config_path)
        self.jinja_env = Environment(loader=FileSystemLoader('templates/'), autoescape=True)

    def _load_config(self, path):
        """Loads the YAML configuration file."""
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    def _load_data(self, path):
        """Loads the JSON data file."""
        print(f"Loading data from {path}...")
        with open(path, 'r') as f:
            return json.load(f)

    def generate_and_save(self):
        """Generates the CV by rendering the template with merged data and saves it."""
        # Get paths from config
        data_path = self.config['output']['merged_data']
        output_path = self.config['output']['comprehensive_cv_html']
        template_name = 'cv_template.html.jinja' # Could also be in config

        # Load the data
        merged_data = self._load_data(data_path)

        # Load the template
        print(f"Loading template: {template_name}...")
        template = self.jinja_env.get_template(template_name)

        # Render the HTML
        print("Rendering HTML from template...")
        html_content = template.render(merged_data)

        # Save the final output
        print(f"Saving comprehensive CV to {output_path}...")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("CV generation complete.")

if __name__ == "__main__":
    generator = ComprehensiveCVGenerator()
    generator.generate_and_save()
