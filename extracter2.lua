---------------------------------------------------------------
--  export‑selected.remodel.lua
--  Dumps scripts from the most‑used developer services only.
---------------------------------------------------------------

local INPUT_FILE  = "game2.rbxl"   -- change if needed
local OUTPUT_ROOT = "exported2"

----------------------------------------------------------------
--   helpers (same sanitise & path‑safety as before)
----------------------------------------------------------------
local ILLEGAL      = '[<>:"/\\|%?%*%z\1-\31]'
local RESERVED_WIN = { "CON","PRN","AUX","NUL",
                       "COM1","COM2","COM3","COM4","COM5","COM6","COM7","COM8","COM9",
                       "LPT1","LPT2","LPT3","LPT4","LPT5","LPT6","LPT7","LPT8","LPT9" }

local function sanitise(name)
    name = name:gsub(ILLEGAL, "_"):gsub("[%.%s]+$", "")
    if #name == 0 then name = "_" end
    if #name > 100 then name = name:sub(1,100) .. "…" end
    for _, r in ipairs(RESERVED_WIN) do
        if name:upper() == r then name = "_" .. name end
    end
    return name
end

local function safeJoin(base, name)
    local p = base .. "/" .. name
    if #p > 240 then
        local excess = #p - 240
        base = base:sub(1, #base-excess-3) .. "…"
        p = base .. "/" .. name
    end
    return p
end

local function writeScript(inst, filePath)
    local ok, src = pcall(remodel.getRawProperty, inst, "Source")
    if ok and src then
        local writeOk, writeErr = pcall(remodel.writeFile, filePath .. ".lua", src)
        if writeOk then
            print("Success:  " .. filePath .. ".lua")
        else
            print("ERROR writing file: " .. filePath .. ".lua - " .. tostring(writeErr))
        end
    else
        print("WARNING: Could not read source from " .. (inst.Name or inst.ClassName) .. " - " .. tostring(src))
    end
end

local exportCount = 0
local function export(inst, basePath, depth)
    depth = depth or 0
    local indent = string.rep("  ", depth)
    
    -- Safety check for infinite recursion
    if depth > 50 then
        print("WARNING: Maximum depth reached at " .. (inst.Name or inst.ClassName))
        return
    end
    
    local instName = inst.Name or inst.ClassName or "_"
    print(indent .. "Processing: " .. instName .. " (" .. inst.ClassName .. ")")
    
    local this = sanitise(instName)
    local here = safeJoin(basePath, this)

    -- Better error handling for directory creation
    local dirOk, dirErr = pcall(remodel.createDirAll, here)
    if not dirOk then
        print("ERROR: Could not create directory " .. here .. " - " .. tostring(dirErr))
        return
    end

    local cls = inst.ClassName
    if cls == "Script" or cls == "LocalScript" or cls == "ModuleScript" then
        exportCount = exportCount + 1
        writeScript(inst, here)
    end

    -- Better error handling for getting children
    local childOk, children = pcall(function() return inst:GetChildren() end)
    if not childOk then
        print("WARNING: Could not get children of " .. instName .. " - " .. tostring(children))
        return
    end
    
    for i, child in ipairs(children) do
        -- Add progress indicator for large numbers of children
        if #children > 10 and i % 10 == 0 then
            print(indent .. "  Progress: " .. i .. "/" .. #children .. " children processed")
        end
        
        -- Wrap each child export in error handling
        local exportOk, exportErr = pcall(export, child, here, depth + 1)
        if not exportOk then
            print("ERROR: Failed to export child " .. (child.Name or child.ClassName) .. " - " .. tostring(exportErr))
        end
    end
end

----------------------------------------------------------------
--  load place
----------------------------------------------------------------
local okPlace, place = pcall(remodel.readPlaceFile, INPUT_FILE)
assert(okPlace and place, "Cannot open "..INPUT_FILE)

print("> Exporting scripts from "..INPUT_FILE.." …")

-- List only the developer‑facing services we want
local TARGET_SERVICES = {
    { place.ServerScriptService,                         "ServerScriptService"      },
    { place.ServerStorage,                               "ServerStorage"            },
    { place.ReplicatedStorage,                           "ReplicatedStorage"        },
    { place.StarterPlayer and
      place.StarterPlayer.StarterPlayerScripts,          "StarterPlayerScripts"     },
    { place.StarterGui,                                  "StarterGui"               },
    { place.StarterPack,                                 "StarterPack"              },
    { place.Workspace,                                   "Workspace"                },
}

for _, pair in ipairs(TARGET_SERVICES) do
    local svc, label = pair[1], pair[2]
    if svc then
        print("\n=== Exporting " .. label .. " ===")
        local serviceOk, serviceErr = pcall(export, svc, OUTPUT_ROOT .. "/" .. label)
        if not serviceOk then
            print("ERROR: Failed to export service " .. label .. " - " .. tostring(serviceErr))
        else
            print("=== Completed " .. label .. " ===")
        end
    else
        print("WARNING: Service " .. label .. " not found or is nil")
    end
end

print("\n>  Finished!  Exported " .. exportCount .. " scripts to \"" .. OUTPUT_ROOT .. "\".")