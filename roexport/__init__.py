"""
RoExport - A Python library for exporting Roblox Studio files to .lua files
"""

__version__ = "1.0.0"
__author__ = "N3uralCreativity"
__description__ = "Export Roblox Studio files (.rbxm) to .lua files usable in any IDE"

from .exporter import RobloxExporter
from .parser import RobloxFileParser

__all__ = ["RobloxExporter", "RobloxFileParser"]