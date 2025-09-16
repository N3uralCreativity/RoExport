# RoExport

A clean and efficient Python tool for exporting Roblox Studio files (.rbxm and .rbxl) to .lua files that can be used in any IDE or text editor.

## Features

- **Clean Export**: Converts Roblox Studio files to standard .lua files
- **IDE Compatible**: Exported files work with any IDE (VS Code, IntelliJ, Sublime Text, etc.)
- **Preserves Structure**: Maintains folder hierarchy from your Roblox project
- **Multiple Script Types**: Supports Scripts, LocalScripts, and ModuleScripts
- **Smart Naming**: Automatically names files based on script type (.server.lua, .client.lua, .lua)
- **No Dependencies**: Uses only Python standard library
- **Command Line Interface**: Easy to use from terminal or integrate into workflows
- **Export Summary**: Generates overview of exported files

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/N3uralCreativity/RoExport.git
cd RoExport

# Install the package
pip install -e .
```

### Basic Usage

```bash
# Export a Roblox file to lua files
roexport my_game.rbxm

# Specify custom output directory
roexport my_game.rbxm exported_scripts/

# Export with flat structure (no subdirectories)
roexport my_game.rbxm --flat

# Export without headers
roexport my_game.rbxm --no-headers
```

## Usage Examples

### Command Line

```bash
# Basic export
roexport game.rbxm

# Export to specific directory
roexport game.rbxm output/

# Flat structure export
roexport game.rbxm scripts/ --flat

# Quiet export without summary
roexport game.rbxm --no-summary

# Verbose output
roexport game.rbxm --verbose
```

### Python API

```python
from roexport import RobloxExporter

# Create exporter
exporter = RobloxExporter(
    preserve_hierarchy=True,  # Maintain folder structure
    add_headers=True         # Add informational headers
)

# Export file
exported_files = exporter.export_with_summary("game.rbxm", "output/")

print(f"Exported {len(exported_files)} files")
```

### Advanced Python Usage

```python
from roexport import RobloxFileParser, RobloxExporter

# Parse file to inspect scripts first
parser = RobloxFileParser()
scripts = parser.parse_file("game.rbxm")

# Filter scripts by type
module_scripts = parser.get_scripts_by_type("ModuleScript")
local_scripts = parser.get_scripts_by_type("LocalScript")

# Get script counts
counts = parser.get_script_count()
print(f"Found {counts['ModuleScript']} ModuleScripts")

# Export with custom settings
exporter = RobloxExporter(preserve_hierarchy=False)
exporter.export_scripts(module_scripts, "modules/")
```

## File Naming Convention

RoExport uses smart naming conventions for exported files:

- **ModuleScript** → `ScriptName.lua`
- **LocalScript** → `ScriptName.client.lua`  
- **Script** → `ScriptName.server.lua`

## Output Structure

### With Hierarchy (default)
```
exported_scripts/
├── ServerScriptService/
│   ├── GameManager.server.lua
│   └── Utils/
│       └── MathHelper.lua
├── StarterPlayer/
│   └── StarterPlayerScripts/
│       └── ClientMain.client.lua
└── EXPORT_SUMMARY.md
```

### Flat Structure (`--flat`)
```
exported_scripts/
├── GameManager.server.lua
├── MathHelper.lua
├── ClientMain.client.lua
└── EXPORT_SUMMARY.md
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `input` | Path to .rbxm or .rbxl file (required) |
| `output` | Output directory (optional, defaults to input filename) |
| `--flat` | Export in flat structure without subdirectories |
| `--no-headers` | Don't add informational headers to files |
| `--no-summary` | Don't generate export summary file |
| `--verbose, -v` | Enable verbose output |
| `--version` | Show version information |

## Export Headers

By default, exported files include informational headers:

```lua
-- ==================================================
-- Script Name: GameManager
-- Script Type: Script
-- Parent Path: ServerScriptService
-- Exported by RoExport
-- ==================================================

-- Your script content here
game.Players.PlayerAdded:Connect(function(player)
    print("Player joined:", player.Name)
end)
```

## Development

### Setting up Development Environment

```bash
# Clone repository
git clone https://github.com/N3uralCreativity/RoExport.git
cd RoExport

# Install in development mode
pip install -e .

# Run tests (if available)
python -m pytest

# Run linting (if available)
python -m flake8 roexport/
```

### Project Structure

```
RoExport/
├── roexport/              # Main package
│   ├── __init__.py       # Package initialization
│   ├── parser.py         # Roblox file parser
│   ├── exporter.py       # Script exporter
│   └── cli.py            # Command line interface
├── roexport.py           # Main entry point
├── setup.py              # Package setup
├── requirements.txt      # Dependencies
├── README.md             # Documentation
└── LICENSE               # Apache 2.0 License
```

## Supported File Types

- `.rbxm` - Roblox Model files
- `.rbxl` - Roblox Place files

## Requirements

- Python 3.7 or higher
- No external dependencies (uses only Python standard library)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/N3uralCreativity/RoExport/issues) page
2. Create a new issue with detailed information about your problem
3. Include sample files if possible (without sensitive content)

## Changelog

### Version 1.0.0
- Initial release
- Support for .rbxm and .rbxl files
- Command line interface
- Python API
- Hierarchical and flat export modes
- Smart file naming
- Export summaries
