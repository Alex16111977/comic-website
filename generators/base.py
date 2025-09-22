"""Base generator class"""
from pathlib import Path
import json

from jinja2 import Environment, FileSystemLoader, select_autoescape

class BaseGenerator:
    """Base class for all generators"""
    
    def __init__(self, config):
        self.config = config
        self.templates_dir = self.config.BASE_DIR / "templates"
        self.static_dir = self.config.BASE_DIR / "static"
        self._env = Environment(
            loader=FileSystemLoader(self.templates_dir),
            autoescape=select_autoescape(["html", "xml"]),
        )
        
    def load_character(self, character_file):
        """Load character data from JSON"""
        with open(character_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_file(self, content, filepath):
        """Save content to file"""
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath

    def render_template(self, template_name, **context):
        """Render template using the configured environment"""
        template = self._env.get_template(template_name)
        return template.render(**context)
