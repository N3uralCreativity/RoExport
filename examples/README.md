# Examples

This directory contains example usage of RoExport.

## Quick Test

Since we don't include actual .rbxm files in the repository, you can test RoExport with your own Roblox Studio files:

1. Export a model or place from Roblox Studio as `.rbxm` or `.rbxl`
2. Place it in this directory
3. Run the examples below

## Command Line Examples

```bash
# Basic export
roexport your_game.rbxm

# Export to specific directory
roexport your_game.rbxm output/

# Flat structure
roexport your_game.rbxm output/ --flat

# No headers
roexport your_game.rbxm output/ --no-headers --no-summary

# Verbose mode
roexport your_game.rbxm --verbose
```

## Python API Examples

Check out `example_usage.py` for Python API examples.

## Sample Output Structure

After running RoExport on a typical Roblox game, you might see:

```
output/
├── ServerScriptService/
│   ├── GameManager.server.lua
│   ├── DataManager.server.lua
│   └── Modules/
│       ├── PlayerData.lua
│       └── GameConfig.lua
├── StarterPlayer/
│   └── StarterPlayerScripts/
│       ├── ClientMain.client.lua
│       └── GUI/
│           └── MenuHandler.client.lua
├── ReplicatedStorage/
│   └── Shared/
│       ├── RemoteEvents.lua
│       └── Constants.lua
└── EXPORT_SUMMARY.md
```