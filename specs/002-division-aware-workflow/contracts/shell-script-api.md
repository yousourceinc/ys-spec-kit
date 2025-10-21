# API Contract: Shell Scripts

**Scripts**: `update-agent-context.sh` and `update-agent-context.ps1`  
**Version**: 1.0.0  
**Status**: Contract Definition

## Overview

These scripts generate AI agent context files by reading project configuration, extracting division information, and listing guides organized by division priority.

---

## Bash Script Functions

### `get_project_division()`

**Purpose**: Read division from `.specify/project.json`

**Parameters**: None (reads from current directory)

**Returns**: Division string (stdout)

**Behavior**:
- Reads `.specify/project.json` if exists
- Extracts `division` field using `jq`
- Falls back to `python3 -c` if `jq` not available
- Returns "SE" if file missing or parse error
- Never exits with error

**Implementation**:
```bash
get_project_division() {
    local config_file=".specify/project.json"
    
    if [ ! -f "$config_file" ]; then
        echo "SE"
        return 0
    fi
    
    # Try jq first
    if command -v jq >/dev/null 2>&1; then
        jq -r '.division // "SE"' "$config_file" 2>/dev/null || echo "SE"
    else
        # Fallback to Python
        python3 -c "import json; print(json.load(open('$config_file')).get('division', 'SE'))" 2>/dev/null || echo "SE"
    fi
}
```

**Tests Required**:
- ✅ Returns division from valid config
- ✅ Returns "SE" when file missing
- ✅ Returns "SE" when JSON invalid
- ✅ Works with jq available
- ✅ Works without jq (Python fallback)

---

### `list_division_guides(division, guides_root)`

**Purpose**: List guide files for specified division

**Parameters**:
- `$1` (division): Division name (e.g., "SE")
- `$2` (guides_root): Path to `context/references/` directory

**Returns**: Newline-separated list of guide paths (stdout)

**Behavior**:
- Finds all `.md` files in `{guides_root}/{division}/`
- Returns relative paths from guides_root
- Returns empty if division directory doesn't exist
- Sorted alphabetically

**Implementation**:
```bash
list_division_guides() {
    local division="$1"
    local guides_root="$2"
    local division_path="$guides_root/$division"
    
    if [ ! -d "$division_path" ]; then
        return 0
    fi
    
    find "$division_path" -name "*.md" -type f | sort
}
```

**Tests Required**:
- ✅ Lists guides from division directory
- ✅ Returns empty for non-existent division
- ✅ Handles spaces in filenames
- ✅ Returns sorted results

---

### `generate_division_context(division, guides_root)`

**Purpose**: Generate division-aware guide listing for agent context

**Parameters**:
- `$1` (division): Project division
- `$2` (guides_root): Path to `context/references/` directory

**Returns**: Formatted Markdown text (stdout)

**Behavior**:
1. Generate "Project Division" header with division name
2. List primary division guides
3. List Common guides (if directory exists)
4. List other division guides with labels

**Implementation**:
```bash
generate_division_context() {
    local division="$1"
    local guides_root="$2"
    
    echo "## Project Division"
    echo ""
    echo "**Division**: $division"
    echo "**Guide Priority**: Guides from \`context/references/$division/\` should be prioritized."
    echo ""
    
    echo "## Available Guides ($division Division)"
    echo ""
    list_division_guides "$division" "$guides_root" | while read -r guide; do
        echo "- $guide"
    done
    echo ""
    
    if [ -d "$guides_root/Common" ]; then
        echo "## Available Guides (Common)"
        echo ""
        list_division_guides "Common" "$guides_root" | while read -r guide; do
            echo "- $guide"
        done
        echo ""
    fi
    
    echo "## Available Guides (Other Divisions)"
    echo ""
    for other_div in "$guides_root"/*; do
        local div_name=$(basename "$other_div")
        if [ "$div_name" != "$division" ] && [ "$div_name" != "Common" ] && [ -d "$other_div" ]; then
            echo "### $div_name"
            list_division_guides "$div_name" "$guides_root" | while read -r guide; do
                echo "- $guide"
            done
            echo ""
        fi
    done
}
```

**Tests Required**:
- ✅ Generates correct Markdown structure
- ✅ Prioritizes project division
- ✅ Includes Common guides
- ✅ Lists other divisions
- ✅ Handles missing directories gracefully

---

## PowerShell Script Functions

### `Get-ProjectDivision`

**Purpose**: Read division from `.specify/project.json`

**Parameters**: None (reads from current directory)

**Returns**: Division string (stdout)

**Behavior**:
- Reads `.specify/project.json` if exists
- Parses JSON using `ConvertFrom-Json`
- Returns "SE" if file missing or parse error
- Never throws exceptions

**Implementation**:
```powershell
function Get-ProjectDivision {
    $configFile = ".specify/project.json"
    
    if (-not (Test-Path $configFile)) {
        return "SE"
    }
    
    try {
        $config = Get-Content $configFile -Raw | ConvertFrom-Json
        if ($config.division) {
            return $config.division
        }
        return "SE"
    } catch {
        Write-Warning "Failed to read project config: $_"
        return "SE"
    }
}
```

**Tests Required**:
- ✅ Returns division from valid config
- ✅ Returns "SE" when file missing
- ✅ Returns "SE" when JSON invalid
- ✅ Logs warning on parse error

---

### `Get-DivisionGuides`

**Purpose**: List guide files for specified division

**Parameters**:
- `Division` (string): Division name
- `GuidesRoot` (string): Path to `context/references/` directory

**Returns**: Array of guide paths

**Behavior**:
- Finds all `.md` files in `{GuidesRoot}/{Division}/`
- Returns file paths
- Returns empty array if division directory doesn't exist
- Sorted alphabetically

**Implementation**:
```powershell
function Get-DivisionGuides {
    param(
        [string]$Division,
        [string]$GuidesRoot
    )
    
    $divisionPath = Join-Path $GuidesRoot $Division
    
    if (-not (Test-Path $divisionPath)) {
        return @()
    }
    
    Get-ChildItem -Path $divisionPath -Filter "*.md" -Recurse -File |
        Sort-Object Name |
        Select-Object -ExpandProperty FullName
}
```

**Tests Required**:
- ✅ Lists guides from division directory
- ✅ Returns empty for non-existent division
- ✅ Handles spaces in filenames
- ✅ Returns sorted results

---

### `New-DivisionContext`

**Purpose**: Generate division-aware guide listing for agent context

**Parameters**:
- `Division` (string): Project division
- `GuidesRoot` (string): Path to `context/references/` directory

**Returns**: Formatted Markdown text (stdout)

**Behavior**:
Same as bash version - generates Markdown with division priority

**Implementation**:
```powershell
function New-DivisionContext {
    param(
        [string]$Division,
        [string]$GuidesRoot
    )
    
    $output = @"
## Project Division

**Division**: $Division
**Guide Priority**: Guides from ``context/references/$Division/`` should be prioritized.

## Available Guides ($Division Division)

"@
    
    Get-DivisionGuides -Division $Division -GuidesRoot $GuidesRoot | ForEach-Object {
        $output += "- $_`n"
    }
    
    $commonPath = Join-Path $GuidesRoot "Common"
    if (Test-Path $commonPath) {
        $output += "`n## Available Guides (Common)`n`n"
        Get-DivisionGuides -Division "Common" -GuidesRoot $GuidesRoot | ForEach-Object {
            $output += "- $_`n"
        }
    }
    
    $output += "`n## Available Guides (Other Divisions)`n`n"
    Get-ChildItem -Path $GuidesRoot -Directory | Where-Object {
        $_.Name -ne $Division -and $_.Name -ne "Common"
    } | ForEach-Object {
        $output += "### $($_.Name)`n"
        Get-DivisionGuides -Division $_.Name -GuidesRoot $GuidesRoot | ForEach-Object {
            $output += "- $_`n"
        }
        $output += "`n"
    }
    
    return $output
}
```

**Tests Required**:
- ✅ Generates correct Markdown structure
- ✅ Prioritizes project division
- ✅ Includes Common guides
- ✅ Lists other divisions
- ✅ Handles missing directories gracefully

---

## Integration Points

Both scripts must:

1. **Read division** from `.specify/project.json` at script start
2. **Pass division** to guide listing functions
3. **Update agent context files** with division-aware content
4. **Preserve manual additions** between `<!-- BEGIN AUTO-GENERATED -->` and `<!-- END AUTO-GENERATED -->` markers
5. **Handle errors gracefully** - never exit with failure if config missing

## Backward Compatibility

- Scripts must work without `.specify/project.json` (default to "SE")
- Scripts must work with guides repos without division structure
- Existing agent context files without division markers remain valid
- Manual content in agent files must be preserved

---

**Status**: Ready for implementation  
**Next**: Update existing scripts with division awareness
