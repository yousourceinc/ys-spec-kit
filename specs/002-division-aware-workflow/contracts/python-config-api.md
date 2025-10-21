# API Contract: Python Config Module

**Module**: `specify_cli.config`  
**Version**: 1.0.0  
**Status**: Contract Definition

## Overview

This module provides functions for reading and writing project configuration (`.specify/project.json`) and validating divisions against the guides repository structure.

---

## Functions

### `read_project_config(project_root: Path) -> dict`

**Purpose**: Read project configuration from `.specify/project.json`

**Parameters**:
- `project_root` (Path): Path to project root directory

**Returns**: 
- `dict`: Project configuration dictionary with at least `{"division": str}`

**Behavior**:
- If file exists and is valid JSON: return parsed content
- If file missing: return `{"division": "SE"}`
- If file corrupted (invalid JSON): return `{"division": "SE"}` and log warning
- Never raises exceptions - always returns valid config with defaults

**Example**:
```python
config = read_project_config(Path("/path/to/project"))
# Returns: {"division": "SE"}
```

**Tests Required**:
- ✅ Valid config file returns correct division
- ✅ Missing file returns default
- ✅ Corrupted JSON returns default with warning logged
- ✅ Additional fields preserved (forward compatibility)

---

### `write_project_config(project_root: Path, division: str) -> None`

**Purpose**: Write division to `.specify/project.json`

**Parameters**:
- `project_root` (Path): Path to project root directory
- `division` (str): Division identifier to store

**Returns**: None

**Raises**:
- `ValueError`: If division is empty or invalid format
- `OSError`: If directory creation or file write fails

**Behavior**:
- Creates `.specify/` directory if it doesn't exist
- Writes config atomically (temp file + rename)
- Preserves existing fields in config file
- Sets file permissions to 0o644 (readable by all, writable by owner)

**Example**:
```python
write_project_config(Path("/path/to/project"), "DS")
# Creates .specify/project.json with {"division": "DS"}
```

**Tests Required**:
- ✅ Creates new config file with division
- ✅ Updates existing config preserving other fields
- ✅ Raises ValueError for invalid division
- ✅ Raises OSError for permission errors
- ✅ Atomic write (test interruption doesn't corrupt file)

---

### `get_project_division(project_root: Path) -> str`

**Purpose**: Convenience function to get division from config

**Parameters**:
- `project_root` (Path): Path to project root directory

**Returns**: 
- `str`: Division identifier (never None, defaults to "SE")

**Behavior**:
- Calls `read_project_config()` and extracts `division` key
- Returns "SE" if key missing or invalid
- Never raises exceptions

**Example**:
```python
division = get_project_division(Path("/path/to/project"))
# Returns: "SE"
```

**Tests Required**:
- ✅ Returns division from valid config
- ✅ Returns "SE" for missing config
- ✅ Returns "SE" for missing division key

---

### `get_valid_divisions(guides_path: Path) -> list[str]`

**Purpose**: Discover valid divisions from guides repository structure

**Parameters**:
- `guides_path` (Path): Path to `context/references/` directory

**Returns**: 
- `list[str]`: Sorted list of division identifiers

**Behavior**:
- Scans `guides_path` for subdirectories (non-hidden)
- Returns directory names as valid divisions
- Falls back to `["SE", "DS", "Platform"]` if path doesn't exist
- Excludes hidden directories (starting with `.`)
- Returns sorted list for consistent ordering

**Example**:
```python
divisions = get_valid_divisions(Path("/path/to/context/references"))
# Returns: ["DS", "Platform", "SE"]
```

**Tests Required**:
- ✅ Returns divisions from directory structure
- ✅ Falls back to defaults when path missing
- ✅ Excludes hidden directories
- ✅ Returns sorted list
- ✅ Handles permission errors gracefully

---

### `validate_division(division: str, guides_path: Path) -> tuple[bool, Optional[str]]`

**Purpose**: Validate division against available divisions

**Parameters**:
- `division` (str): Division to validate
- `guides_path` (Path): Path to `context/references/` directory

**Returns**: 
- `tuple[bool, Optional[str]]`: (is_valid, error_message)

**Behavior**:
- Calls `get_valid_divisions()` to get available divisions
- Returns `(True, None)` if division in valid list
- Returns `(False, error_msg)` with helpful message if invalid
- Error message includes list of valid options

**Example**:
```python
valid, error = validate_division("XYZ", Path("/path/to/context/references"))
# Returns: (False, "Invalid division 'XYZ'. Valid options: DS, Platform, SE")
```

**Tests Required**:
- ✅ Returns True for valid division
- ✅ Returns False with error for invalid division
- ✅ Error message lists valid options
- ✅ Case-sensitive validation

---

### `find_guide(name: str, division: str, guides_path: Path) -> Optional[tuple[Path, str]]`

**Purpose**: Find guide file prioritizing specified division

**Parameters**:
- `name` (str): Guide name (with or without `.md` extension)
- `division` (str): Division to prioritize in search
- `guides_path` (Path): Path to `context/references/` directory

**Returns**: 
- `Optional[tuple[Path, str]]`: (guide_path, found_division) or None

**Behavior**:
1. Search in `{guides_path}/{division}/{name}.md`
2. Search in `{guides_path}/Common/{name}.md` (if exists)
3. Search in other division directories
4. Return None if not found

**Example**:
```python
result = find_guide("backend-patterns", "SE", Path("/path/to/context/references"))
# Returns: (Path(".../SE/backend-patterns.md"), "SE")

result = find_guide("backend-patterns", "DS", Path("/path/to/context/references"))
# Returns: (Path(".../SE/backend-patterns.md"), "SE")  # Found in other division
```

**Tests Required**:
- ✅ Finds guide in primary division
- ✅ Finds guide in Common directory
- ✅ Finds guide in other division
- ✅ Returns None when not found
- ✅ Handles guides with/without .md extension
- ✅ Returns correct found_division

---

### `list_guides(division: str, guides_path: Path) -> dict[str, list[Path]]`

**Purpose**: List all guides organized by priority

**Parameters**:
- `division` (str): Project's division (for prioritization)
- `guides_path` (Path): Path to `context/references/` directory

**Returns**: 
- `dict[str, list[Path]]`: Keys are "primary", "common", "other"

**Behavior**:
- "primary": Guides from specified division
- "common": Guides from Common/ directory (if exists)
- "other": Dict of division -> guides for other divisions

**Example**:
```python
guides = list_guides("SE", Path("/path/to/context/references"))
# Returns: {
#   "primary": [Path(".../SE/backend.md"), Path(".../SE/api.md")],
#   "common": [Path(".../Common/git.md")],
#   "other": {
#     "DS": [Path(".../DS/pipelines.md")],
#     "Platform": [Path(".../Platform/k8s.md")]
#   }
# }
```

**Tests Required**:
- ✅ Lists primary division guides
- ✅ Lists common guides
- ✅ Lists other division guides
- ✅ Handles missing directories
- ✅ Returns empty lists for divisions with no guides

---

## Error Handling Contract

All functions follow these error handling principles:

1. **Config read operations**: Never raise, always return defaults
2. **Config write operations**: Raise specific exceptions (ValueError, OSError)
3. **Validation operations**: Return (bool, error_msg) tuples, never raise
4. **Discovery operations**: Return empty lists/None on errors, never raise

## Performance Contract

- `read_project_config()`: O(1) - single file read
- `write_project_config()`: O(1) - single file write
- `get_valid_divisions()`: O(n) where n = number of subdirectories
- `list_guides()`: O(m) where m = total number of guide files
- All operations should complete in <100ms for typical repositories

## Backward Compatibility

- All functions must handle missing `.specify/project.json` gracefully
- Default division "SE" must be used when config missing
- Additional config fields must be preserved (don't overwrite entire file)
- Functions must work with guides repos that don't have division structure yet

---

**Status**: Ready for implementation  
**Next**: Implement functions with TDD approach
