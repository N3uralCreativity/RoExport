"""
Roblox file parser for extracting scripts from .rbxm files
"""

import xml.etree.ElementTree as ET
import os
import logging
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)


class RobloxScript:
    """Represents a Roblox script with its metadata"""
    
    def __init__(self, name: str, source: str, script_type: str, parent_path: str = ""):
        self.name = name
        self.source = source
        self.script_type = script_type  # Script, LocalScript, ModuleScript
        self.parent_path = parent_path
        
    def get_filename(self) -> str:
        """Generate appropriate filename for the script"""
        # Clean the name for filesystem
        clean_name = "".join(c for c in self.name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        if not clean_name:
            clean_name = "script"
        
        # Add appropriate extension
        if self.script_type == "ModuleScript":
            return f"{clean_name}.lua"
        elif self.script_type == "LocalScript":
            return f"{clean_name}.client.lua"
        else:  # Regular Script
            return f"{clean_name}.server.lua"
            
    def get_full_path(self) -> str:
        """Get the full path including parent hierarchy"""
        if self.parent_path:
            return os.path.join(self.parent_path, self.get_filename())
        return self.get_filename()


class RobloxFileParser:
    """Parser for Roblox Studio files (.rbxm and .rbxl)"""
    
    def __init__(self):
        self.scripts: List[RobloxScript] = []
        
    def parse_file(self, file_path: str) -> List[RobloxScript]:
        """
        Parse a Roblox file and extract all scripts
        
        Args:
            file_path: Path to the .rbxm or .rbxl file
            
        Returns:
            List of RobloxScript objects
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        if not file_path.lower().endswith(('.rbxm', '.rbxl')):
            raise ValueError("File must be a .rbxm or .rbxl file")
            
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            self.scripts = []
            self._parse_element(root, "")
            
            logger.info(f"Parsed {len(self.scripts)} scripts from {file_path}")
            return self.scripts
            
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML format in file {file_path}: {e}")
        except Exception as e:
            raise RuntimeError(f"Error parsing file {file_path}: {e}")
    
    def _parse_element(self, element: ET.Element, parent_path: str):
        """Recursively parse XML elements to find scripts"""
        
        # Check if this element is a script
        class_name = element.get('class', '')
        if class_name in ['Script', 'LocalScript', 'ModuleScript']:
            script = self._extract_script(element, class_name, parent_path)
            if script:
                self.scripts.append(script)
        
        # Build path for children
        name = self._get_element_name(element)
        if name and class_name not in ['Script', 'LocalScript', 'ModuleScript']:
            current_path = os.path.join(parent_path, name) if parent_path else name
        else:
            current_path = parent_path
            
        # Recursively parse children
        for child in element:
            self._parse_element(child, current_path)
    
    def _extract_script(self, element: ET.Element, script_type: str, parent_path: str) -> Optional[RobloxScript]:
        """Extract script information from an XML element"""
        
        name = self._get_element_name(element)
        if not name:
            name = f"unnamed_{script_type.lower()}"
            
        # Find the Source property
        source = ""
        for prop in element.findall('.//Properties'):
            for child in prop:
                if child.get('name') == 'Source':
                    source = child.text or ""
                    break
        
        # Also check direct string properties
        if not source:
            for string_elem in element.findall('.//string[@name="Source"]'):
                source = string_elem.text or ""
                break
        
        if source.strip():  # Only include scripts with actual content
            return RobloxScript(name, source, script_type, parent_path)
        
        return None
    
    def _get_element_name(self, element: ET.Element) -> str:
        """Extract the name of an element"""
        
        # Try to find name in Properties
        for prop in element.findall('.//Properties'):
            for child in prop:
                if child.get('name') == 'Name':
                    return child.text or ""
        
        # Try direct string property
        for string_elem in element.findall('.//string[@name="Name"]'):
            return string_elem.text or ""
            
        # Fallback to referent or class
        return element.get('referent', element.get('class', ''))
    
    def get_scripts_by_type(self, script_type: str) -> List[RobloxScript]:
        """Get all scripts of a specific type"""
        return [script for script in self.scripts if script.script_type == script_type]
    
    def get_script_count(self) -> Dict[str, int]:
        """Get count of scripts by type"""
        counts = {"Script": 0, "LocalScript": 0, "ModuleScript": 0}
        for script in self.scripts:
            if script.script_type in counts:
                counts[script.script_type] += 1
        return counts