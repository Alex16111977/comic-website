#!/usr/bin/env python
"""
King Lear Comic Generator - Main Entry Point
Supports 12 characters with unique journeys
"""

import json
import sys
import shutil
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

import config
from generators import IndexGenerator, LiraHTMLGenerator

def main():
    """Main generator function"""
    print("=" * 60)
    print("  KING LEAR COMIC GENERATOR - 12 CHARACTERS")
    print("=" * 60)
    
    # Create output directories
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (config.OUTPUT_DIR / "journeys").mkdir(exist_ok=True)

    # Copy static assets for browser caching
    static_src = config.BASE_DIR / "static"
    if static_src.exists():
        shutil.copytree(static_src, config.OUTPUT_DIR / "static", dirs_exist_ok=True)
    
    # Copy training.html from templates to output
    training_src = config.BASE_DIR / "templates" / "training.html"
    if training_src.exists():
        shutil.copy2(training_src, config.OUTPUT_DIR / "training.html")
        print("[OK] Copied training.html to output")
    
    # Initialize generators
    lira_gen = LiraHTMLGenerator(config)
    index_gen = IndexGenerator(config)
    
    # Get character files in specified order
    character_files = []
    missing_characters = []
    
    for char_name in config.CHARACTER_ORDER:
        char_file = config.CHARACTERS_DIR / f"{char_name}.json"
        if char_file.exists():
            character_files.append(char_file)
            print(f"[FOUND] {char_name}.json [OK]")
        else:
            missing_characters.append(char_name)
            print(f"[MISSING] {char_name}.json [X]")
    
    if missing_characters:
        print(f"\n[WARNING] Missing {len(missing_characters)} character files:")
        for char in missing_characters:
            print(f"  - {char}.json")
    
    print(f"\n[INFO] Processing {len(character_files)} characters...")
    
    # Generate journey pages for each character
    generated_count = 0
    for char_file in character_files:
        try:
            print(f"\n[GENERATING] {char_file.stem}...")
            
            # Generate journey page
            html = lira_gen.generate_journey(char_file)
            
            # Save to output
            output_path = config.OUTPUT_DIR / "journeys" / f"{char_file.stem}.html"
            lira_gen.save_file(html, output_path)
            
            print(f"[OK] Saved: {output_path.name}")
            generated_count += 1
            
        except Exception as e:
            print(f"[ERROR] Failed to generate {char_file.stem}: {e}")
    
    # Generate index page
    if character_files:
        print("\n[GENERATING] Index page...")
        try:
            index_html = index_gen.generate(character_files)
            index_gen.save_file(index_html, config.OUTPUT_DIR / "index.html")
            print("[OK] Index page created")
        except Exception as e:
            print(f"[ERROR] Failed to generate index: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"[SUMMARY]")
    print(f"  - Characters found: {len(character_files)}/12")
    print(f"  - Pages generated: {generated_count}")
    print(f"  - Output location: {config.OUTPUT_DIR}")
    
    if generated_count == 12:
        print(f"  - Status: [OK] ALL CHARACTERS READY!")
    elif generated_count > 0:
        print(f"  - Status: [WARNING] PARTIAL SUCCESS")
    else:
        print(f"  - Status: [ERROR] GENERATION FAILED")
    
    print("=" * 60)
    
    # Try to open in browser
    if generated_count > 0:
        try:
            import webbrowser
            index_path = config.OUTPUT_DIR / "index.html"
            webbrowser.open(f"file:///{index_path.absolute()}")
            print("\n[OK] Opening in browser...")
        except:
            print("\n[INFO] Please open manually: output/index.html")
    
    return 0 if generated_count > 0 else 1

if __name__ == "__main__":
    sys.exit(main())
