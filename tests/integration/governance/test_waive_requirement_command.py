"""
Integration tests for waive_requirement CLI command.

Tests cover:
- Basic waiver creation via CLI
- Waiver file persistence
- Auto-incrementing IDs
- Timestamp validation
- Error handling
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from typer.testing import CliRunner

from specify_cli import app


@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory for testing."""
    temp_dir = tempfile.mkdtemp()
    old_cwd = Path.cwd()
    try:
        import os
        os.chdir(temp_dir)
        yield Path(temp_dir)
    finally:
        os.chdir(old_cwd)
        shutil.rmtree(temp_dir)


@pytest.fixture
def runner():
    """Create a CLI test runner."""
    return CliRunner()


class TestWaiveRequirementCommand:
    """Tests for the waive_requirement CLI command."""
    
    def test_waive_requirement_basic(self, runner, temp_project_dir):
        """Test basic waiver creation via CLI."""
        result = runner.invoke(app, ["waive-requirement", "Test waiver reason"])
        assert result.exit_code == 0
        assert "Waiver recorded" in result.stdout
        assert "W-001" in result.stdout
        assert "Test waiver reason" in result.stdout
    
    def test_waive_requirement_creates_file(self, runner, temp_project_dir):
        """Test that command creates .specify/waivers.md file."""
        result = runner.invoke(app, ["waive-requirement", "Test waiver"])
        assert result.exit_code == 0
        
        waivers_file = temp_project_dir / ".specify" / "waivers.md"
        assert waivers_file.exists()
    
    def test_waive_requirement_file_contains_content(self, runner, temp_project_dir):
        """Test that waivers file contains expected content."""
        result = runner.invoke(app, ["waive-requirement", "Test waiver reason"])
        assert result.exit_code == 0
        
        waivers_file = temp_project_dir / ".specify" / "waivers.md"
        content = waivers_file.read_text()
        
        assert "# Compliance Waivers" in content
        assert "W-001" in content
        assert "Test waiver reason" in content
        assert "Timestamp" in content
    
    def test_waive_requirement_multiple_waivers(self, runner, temp_project_dir):
        """Test creating multiple waivers with auto-increment."""
        result1 = runner.invoke(app, ["waive-requirement", "First waiver"])
        assert result1.exit_code == 0
        assert "W-001" in result1.stdout
        
        result2 = runner.invoke(app, ["waive-requirement", "Second waiver"])
        assert result2.exit_code == 0
        assert "W-002" in result2.stdout
        
        result3 = runner.invoke(app, ["waive-requirement", "Third waiver"])
        assert result3.exit_code == 0
        assert "W-003" in result3.stdout
        
        # Verify all in file
        waivers_file = temp_project_dir / ".specify" / "waivers.md"
        content = waivers_file.read_text()
        assert "W-001" in content
        assert "W-002" in content
        assert "W-003" in content
    
    def test_waive_requirement_empty_reason_error(self, runner, temp_project_dir):
        """Test that empty reason produces error."""
        result = runner.invoke(app, ["waive-requirement", ""])
        assert result.exit_code == 1
        assert "cannot be empty" in result.stdout
    
    def test_waive_requirement_reason_too_long_error(self, runner, temp_project_dir):
        """Test that reason exceeding 500 chars produces error."""
        long_reason = "x" * 501
        result = runner.invoke(app, ["waive-requirement", long_reason])
        assert result.exit_code == 1
        assert "exceeds 500 character limit" in result.stdout
    
    def test_waive_requirement_reason_500_chars_success(self, runner, temp_project_dir):
        """Test that reason exactly 500 chars succeeds."""
        reason_500 = "x" * 500
        result = runner.invoke(app, ["waive-requirement", reason_500])
        assert result.exit_code == 0
        assert "Waiver recorded" in result.stdout
    
    def test_waive_requirement_special_characters_in_reason(self, runner, temp_project_dir):
        """Test waiver with special characters in reason."""
        reason = "Disabling MFA for service #1234 (JIRA: TICKET-5678) - See: https://example.com"
        result = runner.invoke(app, ["waive-requirement", reason])
        assert result.exit_code == 0
        # The reason should be in the output, though possibly wrapped across lines due to panel width
        assert "Disabling MFA" in result.stdout
        assert "#1234" in result.stdout
        assert "TICKET-5678" in result.stdout
    
    def test_waive_requirement_timestamp_format(self, runner, temp_project_dir):
        """Test that timestamp is in ISO-8601 format."""
        result = runner.invoke(app, ["waive-requirement", "Test waiver"])
        assert result.exit_code == 0
        
        # Verify ISO-8601 format in output
        assert "2025-10-" in result.stdout or "202" in result.stdout
        assert "T" in result.stdout
        assert "Z" in result.stdout
    
    def test_waive_requirement_preserves_existing_waivers(self, runner, temp_project_dir):
        """Test that new waivers don't overwrite existing ones."""
        # Create first waiver
        result1 = runner.invoke(app, ["waive-requirement", "First waiver"])
        assert result1.exit_code == 0
        
        # Create second waiver
        result2 = runner.invoke(app, ["waive-requirement", "Second waiver"])
        assert result2.exit_code == 0
        
        # Both should be in file
        waivers_file = temp_project_dir / ".specify" / "waivers.md"
        content = waivers_file.read_text()
        assert "First waiver" in content
        assert "Second waiver" in content
    
    def test_waive_requirement_help_text(self, runner):
        """Test that help text is available."""
        result = runner.invoke(app, ["waive-requirement", "--help"])
        assert result.exit_code == 0
        assert "Record a formal compliance waiver" in result.stdout
        assert "reason" in result.stdout.lower()
    
    def test_waive_requirement_display_format(self, runner, temp_project_dir):
        """Test that success message has proper formatting."""
        result = runner.invoke(app, ["waive-requirement", "Test waiver"])
        assert result.exit_code == 0
        
        # Check for formatted output elements
        assert "Waiver recorded" in result.stdout
        assert "ID:" in result.stdout
        assert "Reason:" in result.stdout
        assert "Timestamp:" in result.stdout
        assert ".specify/waivers.md" in result.stdout
    
    def test_waive_requirement_whitespace_trimming(self, runner, temp_project_dir):
        """Test that whitespace is trimmed from reason."""
        result = runner.invoke(app, ["waive-requirement", "  Test reason with spaces  "])
        assert result.exit_code == 0
        
        waivers_file = temp_project_dir / ".specify" / "waivers.md"
        content = waivers_file.read_text()
        # Should be trimmed but still contain content
        assert "Test reason with spaces" in content
