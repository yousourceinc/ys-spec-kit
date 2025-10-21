"""
Unit tests for division config module.
"""

import json
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch

from specify_cli.config import (
    read_project_config,
    write_project_config,
    get_project_division,
    get_valid_divisions,
    validate_division,
    find_guide,
    list_guides,
)


class TestReadProjectConfig:
    """Test read_project_config function."""
    
    def test_read_valid_config(self, tmp_path):
        """Test reading valid config file."""
        config_file = tmp_path / ".specify" / "project.json"
        config_file.parent.mkdir()
        
        config_data = {"division": "DS", "other_field": "value"}
        with open(config_file, 'w') as f:
            json.dump(config_data, f)
        
        result = read_project_config(tmp_path)
        assert result == config_data
    
    def test_read_missing_file(self, tmp_path):
        """Test reading when config file doesn't exist."""
        result = read_project_config(tmp_path)
        assert result == {"division": "SE"}
    
    def test_read_corrupted_json(self, tmp_path):
        """Test reading corrupted JSON file."""
        config_file = tmp_path / ".specify" / "project.json"
        config_file.parent.mkdir()
        
        with open(config_file, 'w') as f:
            f.write("invalid json content")
        
        result = read_project_config(tmp_path)
        assert result == {"division": "SE"}
    
    def test_read_missing_division_key(self, tmp_path):
        """Test reading config without division key."""
        config_file = tmp_path / ".specify" / "project.json"
        config_file.parent.mkdir()
        
        config_data = {"other_field": "value"}
        with open(config_file, 'w') as f:
            json.dump(config_data, f)
        
        result = read_project_config(tmp_path)
        assert result == {"division": "SE", "other_field": "value"}


class TestWriteProjectConfig:
    """Test write_project_config function."""
    
    def test_write_new_config(self, tmp_path):
        """Test creating new config file."""
        write_project_config(tmp_path, "DS")
        
        config_file = tmp_path / ".specify" / "project.json"
        assert config_file.exists()
        
        with open(config_file, 'r') as f:
            data = json.load(f)
        
        assert data == {"division": "DS"}
    
    def test_write_atomic_operation(self, tmp_path):
        """Test atomic write prevents corruption."""
        # This is hard to test directly, but we can verify the file is created correctly
        write_project_config(tmp_path, "Platform")
        
        config_file = tmp_path / ".specify" / "project.json"
        assert config_file.exists()
        
        # Verify no temp files left behind
        temp_files = list(tmp_path.glob("**/*.tmp"))
        assert len(temp_files) == 0
    
    def test_write_preserve_existing_fields(self, tmp_path):
        """Test writing preserves existing config fields."""
        config_file = tmp_path / ".specify" / "project.json"
        config_file.parent.mkdir()
        
        existing_data = {"existing_field": "value", "another": 123}
        with open(config_file, 'w') as f:
            json.dump(existing_data, f)
        
        write_project_config(tmp_path, "SE")
        
        with open(config_file, 'r') as f:
            result = json.load(f)
        
        assert result == {"existing_field": "value", "another": 123, "division": "SE"}
    
    def test_write_invalid_division_empty(self, tmp_path):
        """Test writing empty division raises ValueError."""
        with pytest.raises(ValueError, match="Division must be a non-empty string"):
            write_project_config(tmp_path, "")
    
    def test_write_invalid_division_none(self, tmp_path):
        """Test writing None division raises ValueError."""
        with pytest.raises(ValueError, match="Division must be a non-empty string"):
            write_project_config(tmp_path, None)
    
    def test_write_invalid_division_format(self, tmp_path):
        """Test writing invalid format division raises ValueError."""
        with pytest.raises(ValueError, match="Invalid division format"):
            write_project_config(tmp_path, "invalid@division")


class TestGetProjectDivision:
    """Test get_project_division function."""
    
    def test_get_division_from_config(self, tmp_path):
        """Test getting division from existing config."""
        config_file = tmp_path / ".specify" / "project.json"
        config_file.parent.mkdir()
        
        with open(config_file, 'w') as f:
            json.dump({"division": "DS"}, f)
        
        result = get_project_division(tmp_path)
        assert result == "DS"
    
    def test_get_division_missing_config(self, tmp_path):
        """Test getting division when config doesn't exist."""
        result = get_project_division(tmp_path)
        assert result == "SE"
    
    def test_get_division_missing_key(self, tmp_path):
        """Test getting division when key is missing."""
        config_file = tmp_path / ".specify" / "project.json"
        config_file.parent.mkdir()
        
        with open(config_file, 'w') as f:
            json.dump({"other": "value"}, f)
        
        result = get_project_division(tmp_path)
        assert result == "SE"


class TestGetValidDivisions:
    """Test get_valid_divisions function."""
    
    def test_get_divisions_from_directory_structure(self, tmp_path):
        """Test discovering divisions from directory structure."""
        # Create mock guide structure
        refs_dir = tmp_path / "context" / "references"
        (refs_dir / "SE").mkdir(parents=True)
        (refs_dir / "DS").mkdir(parents=True)
        (refs_dir / "Platform").mkdir(parents=True)
        
        result = get_valid_divisions(tmp_path)
        assert result == ["DS", "Platform", "SE"]  # Sorted
    
    def test_get_divisions_fallback_when_no_directory(self, tmp_path):
        """Test fallback to defaults when references directory doesn't exist."""
        result = get_valid_divisions(tmp_path)
        assert result == ["SE", "DS", "Platform"]
    
    def test_get_divisions_exclude_hidden_directories(self, tmp_path):
        """Test excluding hidden directories."""
        refs_dir = tmp_path / "context" / "references"
        (refs_dir / "SE").mkdir(parents=True)
        (refs_dir / ".hidden").mkdir(parents=True)
        (refs_dir / "DS").mkdir(parents=True)
        
        result = get_valid_divisions(tmp_path)
        assert result == ["DS", "SE"]  # Hidden excluded, sorted


class TestValidateDivision:
    """Test validate_division function."""
    
    def test_validate_valid_division(self, tmp_path):
        """Test validating a valid division."""
        refs_dir = tmp_path / "context" / "references"
        (refs_dir / "SE").mkdir(parents=True)
        (refs_dir / "DS").mkdir(parents=True)
        
        is_valid, error = validate_division("SE", tmp_path)
        assert is_valid is True
        assert error is None
    
    def test_validate_invalid_division(self, tmp_path):
        """Test validating an invalid division."""
        refs_dir = tmp_path / "context" / "references"
        (refs_dir / "SE").mkdir(parents=True)
        (refs_dir / "DS").mkdir(parents=True)
        
        is_valid, error = validate_division("INVALID", tmp_path)
        assert is_valid is False
        assert "Invalid division 'INVALID'" in error
        assert "DS" in error and "SE" in error  # Order may vary due to sorting
    
    def test_validate_fallback_divisions(self, tmp_path):
        """Test validation with fallback divisions."""
        is_valid, error = validate_division("SE", tmp_path)
        assert is_valid is True
        assert error is None


class TestFindGuide:
    """Test find_guide function."""
    
    def test_find_guide_in_primary_division(self, tmp_path):
        """Test finding guide in primary division."""
        # Create guide files
        se_guide = tmp_path / "context" / "references" / "SE" / "backend-patterns.md"
        se_guide.parent.mkdir(parents=True)
        se_guide.write_text("# Backend Patterns")
        
        ds_guide = tmp_path / "context" / "references" / "DS" / "backend-patterns.md"
        ds_guide.parent.mkdir(parents=True)
        ds_guide.write_text("# DS Backend Patterns")
        
        result = find_guide("backend-patterns", "SE", tmp_path)
        assert result is not None
        assert result[0] == se_guide
        assert result[1] == "SE"
    
    def test_find_guide_in_common_directory(self, tmp_path):
        """Test finding guide in Common directory."""
        # Create guide in Common
        common_guide = tmp_path / "context" / "references" / "Common" / "git-workflow.md"
        common_guide.parent.mkdir(parents=True)
        common_guide.write_text("# Git Workflow")
        
        result = find_guide("git-workflow", "SE", tmp_path)
        assert result is not None
        assert result[0] == common_guide
        assert result[1] == "Common"
    
    def test_find_guide_in_other_division(self, tmp_path):
        """Test finding guide in other division."""
        # Create guide in DS for SE project
        ds_guide = tmp_path / "context" / "references" / "DS" / "data-pipelines.md"
        ds_guide.parent.mkdir(parents=True)
        ds_guide.write_text("# Data Pipelines")
        
        result = find_guide("data-pipelines", "SE", tmp_path)
        assert result is not None
        assert result[0] == ds_guide
        assert result[1] == "DS"
    
    def test_find_guide_not_found(self, tmp_path):
        """Test guide not found."""
        result = find_guide("nonexistent", "SE", tmp_path)
        assert result is None
    
    def test_find_guide_with_md_extension(self, tmp_path):
        """Test finding guide with .md extension in name."""
        guide = tmp_path / "context" / "references" / "SE" / "test.md"
        guide.parent.mkdir(parents=True)
        guide.write_text("# Test Guide")
        
        result = find_guide("test.md", "SE", tmp_path)
        assert result is not None
        assert result[0] == guide


class TestListGuides:
    """Test list_guides function."""
    
    def test_list_guides_organized_by_priority(self, tmp_path):
        """Test listing guides organized by priority."""
        # Create guide files
        se_guide1 = tmp_path / "context" / "references" / "SE" / "backend.md"
        se_guide1.parent.mkdir(parents=True)
        se_guide1.write_text("# Backend")
        
        se_guide2 = tmp_path / "context" / "references" / "SE" / "api.md"
        se_guide2.write_text("# API")
        
        common_guide = tmp_path / "context" / "references" / "Common" / "git.md"
        common_guide.parent.mkdir(parents=True)
        common_guide.write_text("# Git")
        
        ds_guide = tmp_path / "context" / "references" / "DS" / "data.md"
        ds_guide.parent.mkdir(parents=True)
        ds_guide.write_text("# Data")
        
        result = list_guides("SE", tmp_path)
        
        # Check primary division
        assert len(result["primary"]) == 2
        assert se_guide1 in result["primary"]
        assert se_guide2 in result["primary"]
        
        # Check common
        assert len(result["common"]) == 1
        assert common_guide in result["common"]
        
        # Check other
        assert isinstance(result["other"], dict)
        assert "DS" in result["other"]  # Should contain DS division
        assert len(result["other"]["DS"]) == 1
        assert ds_guide in result["other"]["DS"]
    
    def test_list_guides_no_references_directory(self, tmp_path):
        """Test listing guides when references directory doesn't exist."""
        result = list_guides("SE", tmp_path)
        
        assert result["primary"] == []
        assert result["common"] == []
        assert result["other"] == {}  # Should be empty dict, not empty list