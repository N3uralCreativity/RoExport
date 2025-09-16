#!/usr/bin/env python3
"""
Example usage of RoExport Python API
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from roexport import RobloxExporter, RobloxFileParser


def basic_export_example(rbxm_file: str):
    """Basic export example"""
    print("=== Basic Export Example ===")
    
    # Create exporter with default settings
    exporter = RobloxExporter()
    
    # Export the file
    output_dir = "output_basic"
    exported_files = exporter.export_with_summary(rbxm_file, output_dir)
    
    print(f"Exported {len(exported_files)} files to {output_dir}/")
    
    # Show script counts
    counts = exporter.parser.get_script_count()
    for script_type, count in counts.items():
        if count > 0:
            print(f"  {script_type}: {count}")


def advanced_parsing_example(rbxm_file: str):
    """Advanced parsing and filtering example"""
    print("\n=== Advanced Parsing Example ===")
    
    # Parse file first
    parser = RobloxFileParser()
    scripts = parser.parse_file(rbxm_file)
    
    print(f"Found {len(scripts)} total scripts")
    
    # Filter by type
    module_scripts = [s for s in scripts if s.script_type == "ModuleScript"]
    local_scripts = [s for s in scripts if s.script_type == "LocalScript"]
    server_scripts = [s for s in scripts if s.script_type == "Script"]
    
    print(f"ModuleScripts: {len(module_scripts)}")
    print(f"LocalScripts: {len(local_scripts)}")
    print(f"Server Scripts: {len(server_scripts)}")
    
    # Export different types to different directories
    exporter = RobloxExporter(preserve_hierarchy=False, add_headers=True)
    
    if module_scripts:
        exporter.export_scripts(module_scripts, "output_modules")
        print("Exported ModuleScripts to output_modules/")
    
    if local_scripts:
        exporter.export_scripts(local_scripts, "output_client")
        print("Exported LocalScripts to output_client/")
    
    if server_scripts:
        exporter.export_scripts(server_scripts, "output_server")
        print("Exported Server Scripts to output_server/")


def custom_settings_example(rbxm_file: str):
    """Example with custom settings"""
    print("\n=== Custom Settings Example ===")
    
    # Create exporter with custom settings
    exporter = RobloxExporter(
        preserve_hierarchy=False,  # Flat structure
        add_headers=False         # No headers
    )
    
    # Export with custom settings
    output_dir = "output_custom"
    exported_files = exporter.export_file(rbxm_file, output_dir)
    
    print(f"Exported {len(exported_files)} files (flat, no headers) to {output_dir}/")


def inspect_scripts_example(rbxm_file: str):
    """Example of inspecting scripts before export"""
    print("\n=== Script Inspection Example ===")
    
    parser = RobloxFileParser()
    scripts = parser.parse_file(rbxm_file)
    
    print("Script details:")
    for i, script in enumerate(scripts[:5]):  # Show first 5 scripts
        print(f"  {i+1}. {script.name} ({script.script_type})")
        print(f"     Path: {script.parent_path or 'Root'}")
        print(f"     Filename: {script.get_filename()}")
        print(f"     Content length: {len(script.source)} characters")
        print()
    
    if len(scripts) > 5:
        print(f"     ... and {len(scripts) - 5} more scripts")


def main():
    """Main example function"""
    # Check if we have a test file
    test_files = [f for f in os.listdir('.') if f.endswith(('.rbxm', '.rbxl'))]
    
    if not test_files:
        print("No .rbxm or .rbxl files found in examples directory.")
        print("Please add a Roblox Studio file to test with.")
        print("\nTo create a test file:")
        print("1. Open Roblox Studio")
        print("2. Create some scripts in your game")
        print("3. File > Export Selection... or File > Save to File...")
        print("4. Save as .rbxm or .rbxl in this directory")
        return
    
    # Use the first test file found
    test_file = test_files[0]
    print(f"Using test file: {test_file}")
    
    try:
        # Run examples
        basic_export_example(test_file)
        advanced_parsing_example(test_file)
        custom_settings_example(test_file)
        inspect_scripts_example(test_file)
        
        print("\n=== Examples Complete ===")
        print("Check the output_* directories for exported files!")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()