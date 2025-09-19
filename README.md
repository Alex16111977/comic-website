# 👑 King Lear Comic Generator

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production_Ready-success.svg)](https://github.com/Alex16111977/comic-website)

Interactive educational website generator for learning German through Shakespeare's "King Lear" tragedy.

## 🎭 Features

- **12 Characters** - From King Lear to servants, each with unique journey
- **15 Journey Stages** - Timeline visualization for each character
- **100+ German Quotes** - With transcription [ukr] and translation
- **Pure Python** - No external dependencies required
- **Single File Engine** - All logic in `main.py`
- **Responsive Design** - Works on all devices without Bootstrap

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/Alex16111977/comic-website.git
cd comic-website

# Generate website
python main.py

# Open in browser
start output/index.html
```

## 📁 Project Structure

```
comic-website/
├── main.py              # Main generator engine
├── config.py            # Character configuration
├── README.md            # This file
├── generators/          # HTML/CSS/JS generators
│   ├── base.py          # Base generator class
│   ├── css_lira.py      # CSS with gradients
│   ├── html_lira.py     # HTML journey generator
│   ├── index_gen.py     # Index page generator
│   └── js_lira.py       # JavaScript generator
├── data/                # Project data
│   ├── characters/      # 12 JSON character files
│   │   ├── king_lear.json
│   │   ├── cordelia.json
│   │   ├── goneril.json
│   │   └── ...
│   ├── comics/          # Comic images
│   ├── journey/         # Journey paths
│   └── vocabulary/      # German dictionaries
├── output/              # Generated website
│   ├── index.html       # Main page
│   └── journeys/        # 12 character journey pages
└── scripts/             # Utility scripts
```

## 🎨 Characters

### Main Heroes
- **King Lear** - The tragic king
- **Cordelia** - Youngest daughter
- **Goneril** - Eldest daughter
- **Regan** - Middle daughter

### Secondary Characters
- **Gloucester** - Earl of Gloucester
- **Edgar** - Legitimate son
- **Edmund** - Illegitimate son
- **Kent** - Loyal servant

### Servants & Villains
- **Fool** - The jester
- **Albany** - Duke of Albany
- **Cornwall** - Duke of Cornwall
- **Oswald** - Servant

## 🛠️ Technical Stack

- **Python 3.13** - Core language
- **No Dependencies** - Pure Python implementation
- **Inline CSS** - All styles embedded
- **Vanilla JS** - No frameworks needed
- **JSON Data** - Character information storage

## 📊 Generated Output

The generator creates:
- **13 HTML files** - index.html + 12 character journeys
- **Gradient Cards** - Unique for each character
- **Timeline Visualization** - 15 stages with icons
- **German Quotes** - With [ukr] transcription
- **Responsive Design** - Mobile-friendly

## 🔧 Customization

### Add New Character

1. Create JSON file in `data/characters/`:
```json
{
  "id": "new_character",
  "name": "Character Name",
  "title": "Journey Title",
  "journey": {
    "stages": [
      {
        "title": "Stage 1",
        "quote": "German quote",
        "transcription": "[Ukrainian transcription]"
      }
    ]
  }
}
```

2. Add to `config.py` CHARACTER_ORDER
3. Run generator: `python main.py`

### Modify Styles

Edit generators/css_lira.py for visual changes:
- Character gradients
- Card animations
- Timeline styles
- Responsive breakpoints

## 📝 Scripts

```bash
# Generate website
python main.py

# Check theatrical scenes
python scripts/check_theatrical_scenes.py

# Validate character data
python scripts/validate_characters.py

# Generate test report
python scripts/generate_report.py
```

## 🎯 Educational Goals

This project helps learn German through:
- **Contextual Learning** - Quotes in story context
- **Character Development** - Following hero journeys
- **Visual Memory** - Timeline and gradients
- **Interactive Experience** - Click through stages
- **Cultural Immersion** - Shakespeare in German

## 📈 Statistics

- **12 Characters** with unique stories
- **180 Journey Stages** total (15 per character)
- **100+ German Quotes** with transcription
- **13 Generated Pages** fully interactive
- **0 Dependencies** pure Python

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Shakespeare's "King Lear" for the timeless story
- German translation by [Translator Name]
- Educational concept inspired by language learning through literature

## 📞 Contact

**Alex16111977** - [GitHub Profile](https://github.com/Alex16111977)

Project Link: [https://github.com/Alex16111977/comic-website](https://github.com/Alex16111977/comic-website)

---

**Made with ❤️ for German language learners**

*"Nichts wird aus nichts" - König Lear*
