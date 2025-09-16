"""
Setup script for RoExport
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read version from __init__.py
def get_version():
    with open("roexport/__init__.py", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"')
    return "1.0.0"

version_info = {
    "__version__": get_version(),
    "__author__": "N3uralCreativity",
    "__description__": "Export Roblox Studio files (.rbxm) to .lua files usable in any IDE"
}

setup(
    name="roexport",
    version=version_info["__version__"],
    author=version_info["__author__"],
    description=version_info["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/N3uralCreativity/RoExport",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Tools",
        "Topic :: Games/Entertainment",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "roexport=roexport.cli:main",
        ],
    },
    keywords="roblox export lua script development",
    project_urls={
        "Bug Reports": "https://github.com/N3uralCreativity/RoExport/issues",
        "Source": "https://github.com/N3uralCreativity/RoExport",
    },
)