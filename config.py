"""
Configuration for King Lear Comic Generator
"""
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
CHARACTERS_DIR = DATA_DIR / "characters"
GENERATORS_DIR = BASE_DIR / "generators"

# Character display order (главные → второстепенные → злодеи → слуги)
CHARACTER_ORDER = [
    "king_lear",     # Король Лир
    "cordelia",      # Корделия
    "goneril",       # Гонерилья
    "regan",         # Регана
    "gloucester",    # Глостер
    "edgar",         # Эдгар
    "edmund",        # Эдмунд
    "kent",          # Кент
    "fool",          # Шут
    "albany",        # Олбани
    "cornwall",      # Корнуолл
    "oswald"         # Освальд
]

# Visual theme
THEME_COLORS = {
    "primary": "#6b5b95",
    "secondary": "#764ba2",
    "accent": "#667eea",
    "text": "#333333",
    "background": "#f5f5f5"
}
