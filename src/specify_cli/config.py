"""
Division-aware project configuration management.

This module provides functions for reading and writing project configuration
(.specify/project.json) and validating divisions against the guides repository.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json
import os


def read_project_config(project_root: Path) -> Dict:
    """
    Read project configuration from .specify/project.json

    Args:
        project_root: Path to project root directory

    Returns:
        dict: Project configuration dictionary with at least {"division": str}
    """
    config_file = project_root / ".specify" / "project.json"
    
    try:
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Ensure division key exists, default to "SE"
                if "division" not in config:
                    config["division"] = "SE"
                return config
        else:
            # File doesn't exist, return default
            return {"division": "SE"}
    except (json.JSONDecodeError, OSError):
        # Corrupted JSON or read error, return default
        return {"division": "SE"}


def write_project_config(project_root: Path, division: str) -> None:
    """
    Write division to .specify/project.json

    Args:
        project_root: Path to project root directory
        division: Division identifier to store

    Raises:
        ValueError: If division is empty or invalid format
        OSError: If directory creation or file write fails
    """
    if not division or not isinstance(division, str):
        raise ValueError("Division must be a non-empty string")
    
    # Validate division format (basic check)
    if not division.replace("-", "").replace("_", "").isalnum():
        raise ValueError(f"Invalid division format: {division}")
    
    config_dir = project_root / ".specify"
    config_file = config_dir / "project.json"
    
    # Create directory if it doesn't exist
    config_dir.mkdir(parents=True, exist_ok=True)
    
    # Read existing config to preserve other fields
    existing_config = {}
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                existing_config = json.load(f)
        except (json.JSONDecodeError, OSError):
            # If we can't read existing config, start fresh
            existing_config = {}
    
    # Update division
    existing_config["division"] = division
    
    # Atomic write: write to temp file, then rename
    temp_file = config_file.with_suffix('.tmp')
    try:
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(existing_config, f, indent=2, ensure_ascii=False)
        
        # Set file permissions (readable by all, writable by owner)
        os.chmod(temp_file, 0o644)
        
        # Atomic rename
        temp_file.replace(config_file)
        
    except OSError as e:
        # Clean up temp file if it exists
        if temp_file.exists():
            temp_file.unlink()
        raise OSError(f"Failed to write project config: {e}") from e


def get_project_division(project_root: Path) -> str:
    """
    Convenience function to get division from config

    Args:
        project_root: Path to project root directory

    Returns:
        str: Division identifier (never None, defaults to "SE")
    """
    config = read_project_config(project_root)
    return config.get("division", "SE")


def get_valid_divisions(guides_path: Path) -> List[str]:
    """
    Discover valid divisions from guides repository structure

    Args:
        guides_path: Path to context/references directory

    Returns:
        list[str]: Sorted list of division identifiers
    """
    references_path = guides_path / "context" / "references"
    
    # Check if references directory exists
    if not references_path.exists() or not references_path.is_dir():
        # Fallback to hardcoded defaults
        return ["SE", "DS", "Platform"]
    
    try:
        # Get all subdirectories, exclude hidden ones
        divisions = []
        for item in references_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                divisions.append(item.name)
        
        # Return sorted list, or fallback if empty
        return sorted(divisions) if divisions else ["SE", "DS", "Platform"]
        
    except OSError:
        # Permission error or other filesystem issue
        return ["SE", "DS", "Platform"]


def validate_division(division: str, guides_path: Path) -> Tuple[bool, Optional[str]]:
    """
    Validate division against available divisions

    Args:
        division: Division to validate
        guides_path: Path to context/references directory

    Returns:
        tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    valid_divisions = get_valid_divisions(guides_path)
    
    if division in valid_divisions:
        return True, None
    else:
        error_msg = f"Invalid division '{division}'. Valid options: {', '.join(sorted(valid_divisions))}"
        return False, error_msg


def find_guide(name: str, division: str, guides_path: Path) -> Optional[Tuple[Path, str]]:
    """
    Find guide file prioritizing specified division

    Args:
        name: Guide name (with or without .md extension)
        division: Division to prioritize in search
        guides_path: Path to context/references directory

    Returns:
        Optional[tuple[Path, str]]: (guide_path, found_division) or None
    """
    # Normalize name to include .md extension
    if not name.endswith('.md'):
        name = f"{name}.md"
    
    references_path = guides_path / "context" / "references"
    
    # Search order: 1. Primary division, 2. Common, 3. Other divisions
    search_paths = [
        (references_path / division / name, division),
        (references_path / "Common" / name, "Common"),
    ]
    
    # Add other divisions
    if references_path.exists():
        try:
            for item in references_path.iterdir():
                if (item.is_dir() and 
                    not item.name.startswith('.') and 
                    item.name != division and 
                    item.name != "Common"):
                    search_paths.append((item / name, item.name))
        except OSError:
            pass  # Skip if we can't read directory
    
    # Search in order
    for guide_path, found_division in search_paths:
        if guide_path.exists() and guide_path.is_file():
            return guide_path, found_division
    
    return None


def list_guides(division: str, guides_path: Path) -> Dict[str, List[Path]]:
    """
    List all guides organized by priority

    Args:
        division: Project's division (for prioritization)
        guides_path: Path to context/references directory

    Returns:
        dict: Keys are "primary", "common", "other" with guide paths
    """
    references_path = guides_path / "context" / "references"
    result = {
        "primary": [],
        "common": [],
        "other": {}  # Should be dict, not list
    }
    
    if not references_path.exists():
        return result
    
    try:
        # Collect all guides by division
        division_guides = {}
        for item in references_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                guides = []
                try:
                    for guide_file in item.glob("*.md"):
                        if guide_file.is_file():
                            guides.append(guide_file)
                except OSError:
                    pass  # Skip directories we can't read
                division_guides[item.name] = sorted(guides)
        
        # Organize by priority
        result["primary"] = division_guides.get(division, [])
        result["common"] = division_guides.get("Common", [])
        
        # Other divisions
        other_guides = {}
        for div_name, guides in division_guides.items():
            if div_name != division and div_name != "Common":
                other_guides[div_name] = guides
        result["other"] = other_guides
        
        return result
        
    except OSError:
        return result