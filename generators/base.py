"""Base generator class"""
from pathlib import Path
import json

class BaseGenerator:
    """Base class for all generators"""
    
    def __init__(self, config):
        self.config = config
        
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
