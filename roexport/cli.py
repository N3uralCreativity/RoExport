"""
Command-line interface for RoExport
"""

import argparse
import sys
import os
import logging
from typing import Optional
from .exporter import RobloxExporter
from . import __version__


def setup_logging(verbose: bool = False):
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(levelname)s: %(message)s'
    )


def validate_input_file(file_path: str) -> bool:
    """Validate that the input file exists and has correct extension"""
    if not os.path.exists(file_path):
        print(f"Error: Input file '{file_path}' not found")
        return False
    
    if not file_path.lower().endswith(('.rbxm', '.rbxl')):
        print(f"Error: Input file must be a .rbxm or .rbxl file")
        return False
    
    return True


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Export Roblox Studio files to .lua files',
        prog='roexport'
    )
    
    parser.add_argument(
        'input',
        help='Path to the .rbxm or .rbxl file to export'
    )
    
    parser.add_argument(
        'output',
        nargs='?',
        help='Output directory for .lua files (default: same as input file name)'
    )
    
    parser.add_argument(
        '--flat',
        action='store_true',
        help='Export files in flat structure (no subdirectories)'
    )
    
    parser.add_argument(
        '--no-headers',
        action='store_true',
        help='Don\'t add informational headers to exported files'
    )
    
    parser.add_argument(
        '--no-summary',
        action='store_true',
        help='Don\'t generate export summary file'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'RoExport {__version__}'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    # Validate input file
    if not validate_input_file(args.input):
        sys.exit(1)
    
    # Determine output directory
    if args.output:
        output_dir = args.output
    else:
        # Use input filename (without extension) as output directory
        base_name = os.path.splitext(os.path.basename(args.input))[0]
        output_dir = base_name
    
    # Create exporter
    exporter = RobloxExporter(
        preserve_hierarchy=not args.flat,
        add_headers=not args.no_headers
    )
    
    try:
        print(f"Exporting '{args.input}' to '{output_dir}'...")
        
        if args.no_summary:
            exported_files = exporter.export_file(args.input, output_dir)
        else:
            exported_files = exporter.export_with_summary(args.input, output_dir)
        
        if exported_files:
            print(f"Successfully exported {len(exported_files)} scripts!")
            
            # Show summary
            if not args.no_summary:
                counts = exporter.parser.get_script_count()
                print("\nScript counts:")
                for script_type, count in counts.items():
                    if count > 0:
                        print(f"  {script_type}: {count}")
            
            print(f"\nFiles exported to: {os.path.abspath(output_dir)}")
        else:
            print("No scripts found to export.")
            sys.exit(1)
    
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()