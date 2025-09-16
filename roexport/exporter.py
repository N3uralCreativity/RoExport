"""
Roblox script exporter for converting parsed scripts to .lua files
"""

import os
import logging
from typing import List, Optional
from .parser import RobloxScript, RobloxFileParser

logger = logging.getLogger(__name__)


class RobloxExporter:
    """Exports Roblox scripts to .lua files"""
    
    def __init__(self, preserve_hierarchy: bool = True, add_headers: bool = True):
        """
        Initialize the exporter
        
        Args:
            preserve_hierarchy: Whether to preserve the original folder structure
            add_headers: Whether to add informational headers to exported files
        """
        self.preserve_hierarchy = preserve_hierarchy
        self.add_headers = add_headers
        self.parser = RobloxFileParser()
    
    def export_file(self, input_path: str, output_dir: str) -> List[str]:
        """
        Export all scripts from a Roblox file to .lua files
        
        Args:
            input_path: Path to the .rbxm or .rbxl file
            output_dir: Directory to export .lua files to
            
        Returns:
            List of exported file paths
        """
        # Parse the input file
        scripts = self.parser.parse_file(input_path)
        
        if not scripts:
            logger.warning(f"No scripts found in {input_path}")
            return []
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        exported_files = []
        
        for script in scripts:
            exported_path = self._export_script(script, output_dir)
            if exported_path:
                exported_files.append(exported_path)
        
        logger.info(f"Exported {len(exported_files)} scripts to {output_dir}")
        return exported_files
    
    def export_scripts(self, scripts: List[RobloxScript], output_dir: str) -> List[str]:
        """
        Export a list of scripts to .lua files
        
        Args:
            scripts: List of RobloxScript objects to export
            output_dir: Directory to export .lua files to
            
        Returns:
            List of exported file paths
        """
        os.makedirs(output_dir, exist_ok=True)
        
        exported_files = []
        
        for script in scripts:
            exported_path = self._export_script(script, output_dir)
            if exported_path:
                exported_files.append(exported_path)
        
        return exported_files
    
    def _export_script(self, script: RobloxScript, output_dir: str) -> Optional[str]:
        """Export a single script to a .lua file"""
        
        try:
            if self.preserve_hierarchy:
                # Create full path with hierarchy
                full_path = script.get_full_path()
                file_path = os.path.join(output_dir, full_path)
                
                # Create intermediate directories
                dir_path = os.path.dirname(file_path)
                if dir_path:
                    os.makedirs(dir_path, exist_ok=True)
            else:
                # Flat structure - just use filename
                file_path = os.path.join(output_dir, script.get_filename())
            
            # Prepare content
            content = self._prepare_content(script)
            
            # Write to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.debug(f"Exported {script.name} to {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Failed to export script {script.name}: {e}")
            return None
    
    def _prepare_content(self, script: RobloxScript) -> str:
        """Prepare the content for export"""
        
        content_parts = []
        
        if self.add_headers:
            # Add informational header
            header = self._generate_header(script)
            content_parts.append(header)
        
        # Add the actual script content
        content_parts.append(script.source)
        
        return '\n'.join(content_parts)
    
    def _generate_header(self, script: RobloxScript) -> str:
        """Generate an informational header for the script"""
        
        header_lines = [
            "-- " + "="*50,
            f"-- Script Name: {script.name}",
            f"-- Script Type: {script.script_type}",
        ]
        
        if script.parent_path:
            header_lines.append(f"-- Parent Path: {script.parent_path}")
        
        header_lines.extend([
            "-- Exported by RoExport",
            "-- " + "="*50,
            ""
        ])
        
        return '\n'.join(header_lines)
    
    def create_init_files(self, output_dir: str, scripts: List[RobloxScript]):
        """
        Create init.lua files for ModuleScript directories
        
        Args:
            output_dir: The output directory
            scripts: List of exported scripts
        """
        if not self.preserve_hierarchy:
            return
        
        # Find all directories that contain ModuleScripts
        module_dirs = set()
        for script in scripts:
            if script.script_type == "ModuleScript" and script.parent_path:
                module_dirs.add(os.path.join(output_dir, script.parent_path))
        
        # Create init.lua files
        for dir_path in module_dirs:
            init_path = os.path.join(dir_path, "init.lua")
            if not os.path.exists(init_path):
                with open(init_path, 'w', encoding='utf-8') as f:
                    f.write("-- Auto-generated init.lua\n")
                    f.write("-- This directory contains ModuleScripts\n")
                    f.write("return {}\n")
    
    def generate_summary(self, scripts: List[RobloxScript], output_dir: str):
        """Generate a summary file of exported scripts"""
        
        summary_path = os.path.join(output_dir, "EXPORT_SUMMARY.md")
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("# RoExport Summary\n\n")
            
            # Count by type
            counts = {}
            for script in scripts:
                counts[script.script_type] = counts.get(script.script_type, 0) + 1
            
            f.write("## Script Counts\n\n")
            for script_type, count in counts.items():
                f.write(f"- {script_type}: {count}\n")
            
            f.write("\n## Exported Files\n\n")
            
            # Group by type
            by_type = {}
            for script in scripts:
                if script.script_type not in by_type:
                    by_type[script.script_type] = []
                by_type[script.script_type].append(script)
            
            for script_type, type_scripts in by_type.items():
                f.write(f"### {script_type}\n\n")
                for script in type_scripts:
                    path = script.get_full_path() if self.preserve_hierarchy else script.get_filename()
                    f.write(f"- `{path}`\n")
                f.write("\n")
        
        logger.info(f"Generated summary at {summary_path}")
    
    def export_with_summary(self, input_path: str, output_dir: str) -> List[str]:
        """
        Export scripts and generate summary
        
        Args:
            input_path: Path to the .rbxm or .rbxl file
            output_dir: Directory to export .lua files to
            
        Returns:
            List of exported file paths
        """
        exported_files = self.export_file(input_path, output_dir)
        
        if exported_files:
            self.create_init_files(output_dir, self.parser.scripts)
            self.generate_summary(self.parser.scripts, output_dir)
        
        return exported_files