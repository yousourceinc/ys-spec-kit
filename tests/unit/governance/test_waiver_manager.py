"""
Unit tests for waiver management module.

Tests cover:
- Waiver creation and validation
- Auto-incrementing ID generation
- Markdown formatting
- File persistence
- Waiver parsing and retrieval
"""

import pytest
from pathlib import Path
from datetime import datetime, timezone
import tempfile
import shutil

from specify_cli.governance.waiver import Waiver, WaiverManager


@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def waiver_manager(temp_project_dir):
    """Create a WaiverManager instance with temporary directory."""
    return WaiverManager(project_root=temp_project_dir)


class TestWaiverClass:
    """Tests for Waiver data class."""
    
    def test_waiver_initialization(self):
        """Test basic waiver initialization."""
        waiver = Waiver(
            waiver_id="W-001",
            reason="Test waiver",
            timestamp="2025-10-21T10:00:00Z"
        )
        assert waiver.waiver_id == "W-001"
        assert waiver.reason == "Test waiver"
        assert waiver.timestamp == "2025-10-21T10:00:00Z"
        assert waiver.related_rules == []
        assert waiver.created_by is None
    
    def test_waiver_with_optional_fields(self):
        """Test waiver with optional fields."""
        waiver = Waiver(
            waiver_id="W-002",
            reason="Waiver with options",
            timestamp="2025-10-21T11:00:00Z",
            related_rules=["rule-1", "rule-2"],
            created_by="developer@example.com"
        )
        assert waiver.related_rules == ["rule-1", "rule-2"]
        assert waiver.created_by == "developer@example.com"
    
    def test_waiver_to_dict(self):
        """Test converting waiver to dictionary."""
        waiver = Waiver(
            waiver_id="W-001",
            reason="Test",
            timestamp="2025-10-21T10:00:00Z",
            related_rules=["rule-1"]
        )
        waiver_dict = waiver.to_dict()
        assert waiver_dict["id"] == "W-001"
        assert waiver_dict["reason"] == "Test"
        assert waiver_dict["timestamp"] == "2025-10-21T10:00:00Z"
        assert waiver_dict["related_rules"] == ["rule-1"]
    
    def test_waiver_repr(self):
        """Test waiver string representation."""
        waiver = Waiver(
            waiver_id="W-001",
            reason="This is a longer waiver reason",
            timestamp="2025-10-21T10:00:00Z"
        )
        assert "W-001" in repr(waiver)
        assert "This is a" in repr(waiver)


class TestWaiverIDGeneration:
    """Tests for auto-incrementing waiver ID generation."""
    
    def test_generate_waiver_id_empty_list(self):
        """Test ID generation with no existing waivers."""
        waiver_id = WaiverManager.generate_waiver_id([])
        assert waiver_id == "W-001"
    
    def test_generate_waiver_id_single_waiver(self):
        """Test ID generation with one existing waiver."""
        existing = [Waiver("W-001", "reason", "2025-10-21T10:00:00Z")]
        waiver_id = WaiverManager.generate_waiver_id(existing)
        assert waiver_id == "W-002"
    
    def test_generate_waiver_id_multiple_waivers(self):
        """Test ID generation with multiple existing waivers."""
        existing = [
            Waiver("W-001", "reason1", "2025-10-21T10:00:00Z"),
            Waiver("W-002", "reason2", "2025-10-21T11:00:00Z"),
            Waiver("W-003", "reason3", "2025-10-21T12:00:00Z"),
        ]
        waiver_id = WaiverManager.generate_waiver_id(existing)
        assert waiver_id == "W-004"
    
    def test_generate_waiver_id_padding(self):
        """Test that waiver IDs are zero-padded to 3 digits."""
        existing = [Waiver(f"W-{i:03d}", f"reason{i}", "2025-10-21T10:00:00Z") for i in range(1, 11)]
        waiver_id = WaiverManager.generate_waiver_id(existing)
        assert waiver_id == "W-011"


class TestWaiverFormatting:
    """Tests for markdown waiver entry formatting."""
    
    def test_format_waiver_entry_basic(self):
        """Test basic waiver entry formatting."""
        entry = WaiverManager.format_waiver_entry(
            "W-001",
            "Test reason",
            "2025-10-21T10:00:00Z"
        )
        assert "## Waiver: W-001" in entry
        assert "**Reason**: Test reason" in entry
        assert "**Timestamp**: 2025-10-21T10:00:00Z" in entry
    
    def test_format_waiver_entry_with_related_rules(self):
        """Test waiver formatting with related rules."""
        entry = WaiverManager.format_waiver_entry(
            "W-001",
            "Test reason",
            "2025-10-21T10:00:00Z",
            related_rules=["rule-1", "rule-2"]
        )
        assert "**Related Rules**: [rule-1, rule-2]" in entry
    
    def test_format_waiver_entry_with_created_by(self):
        """Test waiver formatting with creator information."""
        entry = WaiverManager.format_waiver_entry(
            "W-001",
            "Test reason",
            "2025-10-21T10:00:00Z",
            created_by="developer@example.com"
        )
        assert "**Created By**: developer@example.com" in entry
    
    def test_format_waiver_entry_all_fields(self):
        """Test waiver formatting with all optional fields."""
        entry = WaiverManager.format_waiver_entry(
            "W-001",
            "Test reason",
            "2025-10-21T10:00:00Z",
            related_rules=["rule-1"],
            created_by="dev@example.com"
        )
        assert "W-001" in entry
        assert "Test reason" in entry
        assert "2025-10-21T10:00:00Z" in entry
        assert "rule-1" in entry
        assert "dev@example.com" in entry


class TestWaiverCreation:
    """Tests for creating and storing waivers."""
    
    def test_create_waiver_basic(self, waiver_manager):
        """Test creating a basic waiver."""
        waiver = waiver_manager.create_waiver("Test waiver reason")
        assert waiver.waiver_id == "W-001"
        assert waiver.reason == "Test waiver reason"
        assert waiver.timestamp.startswith("2025-10-") or waiver.timestamp.startswith("202")
    
    def test_create_waiver_with_options(self, waiver_manager):
        """Test creating waiver with optional fields."""
        waiver = waiver_manager.create_waiver(
            "Test reason",
            related_rules=["rule-1"],
            created_by="dev@example.com"
        )
        assert waiver.related_rules == ["rule-1"]
        assert waiver.created_by == "dev@example.com"
    
    def test_create_waiver_empty_reason_raises(self, waiver_manager):
        """Test that empty reason raises ValueError."""
        with pytest.raises(ValueError, match="reason cannot be empty"):
            waiver_manager.create_waiver("")
    
    def test_create_waiver_whitespace_reason_raises(self, waiver_manager):
        """Test that whitespace-only reason raises ValueError."""
        with pytest.raises(ValueError, match="reason cannot be empty"):
            waiver_manager.create_waiver("   ")
    
    def test_create_waiver_reason_too_long_raises(self, waiver_manager):
        """Test that reason exceeding 500 chars raises ValueError."""
        long_reason = "x" * 501
        with pytest.raises(ValueError, match="cannot exceed 500 characters"):
            waiver_manager.create_waiver(long_reason)
    
    def test_create_waiver_reason_500_chars_accepted(self, waiver_manager):
        """Test that reason exactly 500 chars is accepted."""
        reason_500 = "x" * 500
        waiver = waiver_manager.create_waiver(reason_500)
        assert waiver.reason == reason_500
    
    def test_create_waiver_timestamp_format(self, waiver_manager):
        """Test that waiver timestamp is ISO-8601 format."""
        waiver = waiver_manager.create_waiver("Test reason")
        # Verify ISO-8601 format: YYYY-MM-DDTHH:MM:SSZ
        assert len(waiver.timestamp) == 20
        assert "T" in waiver.timestamp
        assert waiver.timestamp.endswith("Z")
    
    def test_create_multiple_waivers_auto_increment(self, waiver_manager):
        """Test that multiple waivers get auto-incremented IDs."""
        w1 = waiver_manager.create_waiver("First waiver")
        w2 = waiver_manager.create_waiver("Second waiver")
        w3 = waiver_manager.create_waiver("Third waiver")
        assert w1.waiver_id == "W-001"
        assert w2.waiver_id == "W-002"
        assert w3.waiver_id == "W-003"


class TestWaiverFileOperations:
    """Tests for waiver file creation and updates."""
    
    def test_append_to_waivers_file_creates_file(self, waiver_manager):
        """Test that appending creates .specify/waivers.md if missing."""
        waiver = Waiver("W-001", "Test reason", "2025-10-21T10:00:00Z")
        waiver_manager.append_to_waivers_file(waiver)
        
        assert waiver_manager.waivers_file.exists()
    
    def test_append_to_waivers_file_creates_directory(self, waiver_manager):
        """Test that .specify directory is created if missing."""
        waiver = Waiver("W-001", "Test reason", "2025-10-21T10:00:00Z")
        waiver_manager.append_to_waivers_file(waiver)
        
        assert waiver_manager.waivers_dir.exists()
    
    def test_append_to_waivers_file_includes_header(self, waiver_manager):
        """Test that new file includes header."""
        waiver = Waiver("W-001", "Test reason", "2025-10-21T10:00:00Z")
        waiver_manager.append_to_waivers_file(waiver)
        
        content = waiver_manager.waivers_file.read_text()
        assert "# Compliance Waivers" in content
        assert "Formal exceptions" in content
    
    def test_append_to_waivers_file_preserves_content(self, waiver_manager):
        """Test that appending preserves existing content."""
        w1 = Waiver("W-001", "First reason", "2025-10-21T10:00:00Z")
        waiver_manager.append_to_waivers_file(w1)
        
        w2 = Waiver("W-002", "Second reason", "2025-10-21T11:00:00Z")
        waiver_manager.append_to_waivers_file(w2)
        
        content = waiver_manager.waivers_file.read_text()
        assert "W-001" in content
        assert "W-002" in content
        assert "First reason" in content
        assert "Second reason" in content


class TestWaiverParsing:
    """Tests for parsing waivers from file."""
    
    def test_parse_waivers_file_missing_returns_empty(self, waiver_manager):
        """Test that missing file returns empty list."""
        waivers = waiver_manager.parse_waivers_file()
        assert waivers == []
    
    def test_parse_waivers_file_single_waiver(self, waiver_manager):
        """Test parsing file with single waiver."""
        waiver = waiver_manager.create_waiver("Test reason")
        parsed = waiver_manager.parse_waivers_file()
        
        assert len(parsed) == 1
        assert parsed[0].waiver_id == "W-001"
        assert parsed[0].reason == "Test reason"
    
    def test_parse_waivers_file_multiple_waivers(self, waiver_manager):
        """Test parsing file with multiple waivers."""
        w1 = waiver_manager.create_waiver("Reason 1")
        w2 = waiver_manager.create_waiver("Reason 2")
        w3 = waiver_manager.create_waiver("Reason 3")
        
        parsed = waiver_manager.parse_waivers_file()
        assert len(parsed) == 3
        assert parsed[0].waiver_id == "W-001"
        assert parsed[1].waiver_id == "W-002"
        assert parsed[2].waiver_id == "W-003"
    
    def test_parse_waivers_file_with_related_rules(self, waiver_manager):
        """Test parsing waiver with related rules."""
        waiver = waiver_manager.create_waiver(
            "Test reason",
            related_rules=["rule-1", "rule-2"]
        )
        parsed = waiver_manager.parse_waivers_file()
        
        assert len(parsed) == 1
        assert parsed[0].related_rules == ["rule-1", "rule-2"]
    
    def test_parse_waivers_file_with_created_by(self, waiver_manager):
        """Test parsing waiver with creator information."""
        waiver = waiver_manager.create_waiver(
            "Test reason",
            created_by="developer@example.com"
        )
        parsed = waiver_manager.parse_waivers_file()
        
        assert len(parsed) == 1
        assert parsed[0].created_by == "developer@example.com"


class TestWaiverRetrieval:
    """Tests for getting specific waivers."""
    
    def test_get_waiver_by_id_found(self, waiver_manager):
        """Test retrieving existing waiver by ID."""
        waiver = waiver_manager.create_waiver("Test reason")
        retrieved = waiver_manager.get_waiver_by_id("W-001")
        
        assert retrieved is not None
        assert retrieved.waiver_id == "W-001"
        assert retrieved.reason == "Test reason"
    
    def test_get_waiver_by_id_not_found(self, waiver_manager):
        """Test retrieving non-existent waiver returns None."""
        waiver_manager.create_waiver("Test reason")
        retrieved = waiver_manager.get_waiver_by_id("W-999")
        
        assert retrieved is None
    
    def test_get_waiver_by_id_from_multiple(self, waiver_manager):
        """Test retrieving specific waiver from multiple."""
        w1 = waiver_manager.create_waiver("Reason 1")
        w2 = waiver_manager.create_waiver("Reason 2")
        w3 = waiver_manager.create_waiver("Reason 3")
        
        retrieved = waiver_manager.get_waiver_by_id("W-002")
        assert retrieved.waiver_id == "W-002"
        assert retrieved.reason == "Reason 2"
    
    def test_list_waivers_empty(self, waiver_manager):
        """Test listing waivers when none exist."""
        waivers = waiver_manager.list_waivers()
        assert waivers == []
    
    def test_list_waivers_multiple(self, waiver_manager):
        """Test listing multiple waivers in order."""
        w1 = waiver_manager.create_waiver("Reason 1")
        w2 = waiver_manager.create_waiver("Reason 2")
        w3 = waiver_manager.create_waiver("Reason 3")
        
        waivers = waiver_manager.list_waivers()
        assert len(waivers) == 3
        assert waivers[0].waiver_id == "W-001"
        assert waivers[1].waiver_id == "W-002"
        assert waivers[2].waiver_id == "W-003"
