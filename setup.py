"""
Setup configuration for King Lear Comic Generator
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="king-lear-comic-generator",
    version="1.0.0",
    author="Alex16111977",
    author_email="",
    description="Interactive educational website generator for learning German through Shakespeare's King Lear",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Alex16111977/comic-website",
    packages=find_packages(exclude=["tests", "scripts", "output", ".venv"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Topic :: Education :: Computer Aided Instruction (CAI)",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Natural Language :: German",
        "Natural Language :: Ukrainian",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    
    # No dependencies! Pure Python project
    install_requires=[
        # This project has NO external dependencies
        # It runs with standard Python library only
    ],
    
    # Optional dependencies for development
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "pylint>=3.0.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.3.0",
        ],
    },
    
    # Entry point for command line
    entry_points={
        "console_scripts": [
            "king-lear-generate=main:main",
        ],
    },
    
    # Include data files
    include_package_data=True,
    package_data={
        "": ["*.json", "*.md", "*.html", "*.css", "*.js"],
        "data": ["**/*.json"],
        "output": ["**/*.html", "**/*.css", "**/*.js"],
    },
    
    # Project URLs
    project_urls={
        "Bug Reports": "https://github.com/Alex16111977/comic-website/issues",
        "Source": "https://github.com/Alex16111977/comic-website",
    },
)
