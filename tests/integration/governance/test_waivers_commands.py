"""
Integration tests for waivers list and show commands.

Tests the CLI commands for viewing and managing compliance waivers.
"""

import tempfile
from pathlib import Path
from typing import Generator

import pytest
from typer.testing import CliRunner

from specify_cli import app
from specify_cli.governance.waiver import WaiverManager


@pytest.fixture
def cli_runner() -> CliRunner:
    """Provide a Typer CLI test runner."""
    return CliRunner()


@pytest.fixture
def temp_project() -> Generator[Path, None, None]:
    """Provide a temporary project directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir)
        
        # Create .specify directory
        specify_dir = project_root / ".specify"
        specify_dir.mkdir(parents=True, exist_ok=True)
        
        # Change to temp directory for test
        import os
        old_cwd = os.getcwd()
        os.chdir(project_root)
        
        yield project_root
        
        # Restore original directory
        os.chdir(old_cwd)


class TestWaiverListCommand:
    """Tests for 'waivers list' command."""
    
    def test_waivers_list_no_waivers(self, cli_runner: CliRunner, temp_project: Path):
        """Test 'waivers list' when no waivers exist."""
        result = cli_runner.invoke(app, ["waivers", "list"])
        
        assert result.exit_code == 0
        assert "No waivers found" in result.stdout or "No waivers found" in result.output
    
    def test_waivers_list_single_waiver(self, cli_runner: CliRunner, temp_project: Path):
        """Test 'waivers list' with a single waiver."""
        # Create a waiver
        manager = WaiverManager()
        waiver = manager.create_waiver("Test waiver reason")
        
        # Run list command
        result = cli_runner.invoke(app, ["waivers", "list"])
        
        assert result.exit_code == 0
        assert waiver.waiver_id in result.output
        assert "Test waiver reason" in result.output
        assert "1 total" in result.output
    
    def test_waivers_list_multiple_waivers(self, cli_runner: CliRunner, temp_project: Path):
        """Test 'waivers list' with multiple waivers."""
        # Create multiple waivers
        manager = WaiverManager()
        waiver1 = manager.create_waiver("First waiver")
        waiver2 = manager.create_waiver("Second waiver")
        waiver3 = manager.create_waiver("Third waiver")
        
        # Run list command
        result = cli_runner.invoke(app, ["waivers", "list"])
        
        assert result.exit_code == 0
        assert waiver1.waiver_id in result.output
        assert waiver2.waiver_id in result.output
        assert waiver3.waiver_id in result.output
        assert "First waiver" in result.output
        assert "Second waiver" in result.output
        assert "Third waiver" in result.output
        assert "3 total" in result.output
    
    def test_waivers_list_table_format(self, cli_runner: CliRunner, temp_project: Path):
        """Test that 'waivers list' shows a formatted table."""
        manager = WaiverManager()
        manager.create_waiver("Waiver for testing")
        
        # Run list command without verbose
        result = cli_runner.invoke(app, ["waivers", "list"])
        
        assert result.exit_code == 0
        # Should show table header
        assert "ID" in result.output or "Waiver" in result.output
        assert "Reason" in result.output or "waiver" in result.output.lower()
        assert "Timestamp" in result.output or "timestamp" in result.output.lower()
    
    def test_waivers_list_verbose_format(self, cli_runner: CliRunner, temp_project: Path):
        """Test 'waivers list --verbose' shows detailed information."""
        manager = WaiverManager()
        waiver = manager.create_waiver(
            "Test waiver",
            related_rules=["R-001", "R-002"],
            created_by="test-user"
        )
        
        # Run list command with verbose flag
        result = cli_runner.invoke(app, ["waivers", "list", "--verbose"])
        
        assert result.exit_code == 0
        assert waiver.waiver_id in result.output
        assert "Test waiver" in result.output
        assert "test-user" in result.output
        assert "R-001" in result.output
        assert "R-002" in result.output
    
    def test_waivers_list_chronological_order(self, cli_runner: CliRunner, temp_project: Path):
        """Test that 'waivers list' shows waivers in chronological order."""
        manager = WaiverManager()
        waiver1 = manager.create_waiver("First waiver")
        waiver2 = manager.create_waiver("Second waiver")
        waiver3 = manager.create_waiver("Third waiver")
        
        # Run list command
        result = cli_runner.invoke(app, ["waivers", "list"])
        
        # Check that waivers appear in order
        idx1 = result.output.find(waiver1.waiver_id)
        idx2 = result.output.find(waiver2.waiver_id)
        idx3 = result.output.find(waiver3.waiver_id)
        
        assert idx1 < idx2 < idx3


class TestWaiverShowCommand:
    """Tests for 'waivers show' command."""
    
    def test_waivers_show_waiver_found(self, cli_runner: CliRunner, temp_project: Path):
        """Test 'waivers show' with an existing waiver."""
        manager = WaiverManager()
        waiver = manager.create_waiver("Test waiver reason")
        
        # Run show command
        result = cli_runner.invoke(app, ["waivers", "show", waiver.waiver_id])
        
        assert result.exit_code == 0
        assert waiver.waiver_id in result.output
        assert "Test waiver reason" in result.output
        assert waiver.timestamp in result.output
    
    def test_waivers_show_waiver_not_found(self, cli_runner: CliRunner, temp_project: Path):
        """Test 'waivers show' with non-existent waiver."""
        result = cli_runner.invoke(app, ["waivers", "show", "W-999"])
        
        assert result.exit_code != 0
        assert "not found" in result.output.lower()
    
    def test_waivers_show_invalid_id_format(self, cli_runner: CliRunner, temp_project: Path):
        """Test 'waivers show' with invalid waiver ID format."""
        result = cli_runner.invoke(app, ["waivers", "show", "INVALID-123"])
        
        assert result.exit_code != 0
        assert "must start with 'W-'" in result.output
    
    def test_waivers_show_full_details(self, cli_runner: CliRunner, temp_project: Path):
        """Test 'waivers show' displays full waiver details."""
        manager = WaiverManager()
        waiver = manager.create_waiver(
            "Test waiver with full details",
            related_rules=["R-001", "R-002", "R-003"],
            created_by="john.doe@example.com"
        )
        
        # Run show command
        result = cli_runner.invoke(app, ["waivers", "show", waiver.waiver_id])
        
        assert result.exit_code == 0
        assert waiver.waiver_id in result.output
        assert "Test waiver with full details" in result.output
        assert waiver.timestamp in result.output
        assert "john.doe@example.com" in result.output
        assert "R-001" in result.output
        assert "R-002" in result.output
        assert "R-003" in result.output
    
    def test_waivers_show_details_formatting(self, cli_runner: CliRunner, temp_project: Path):
        """Test that 'waivers show' formats details nicely."""
        manager = WaiverManager()
        waiver = manager.create_waiver("Formatted details test")
        
        # Run show command
        result = cli_runner.invoke(app, ["waivers", "show", waiver.waiver_id])
        
        assert result.exit_code == 0
        # Should have formatted labels
        assert "ID:" in result.output
        assert "Reason:" in result.output
        assert "Timestamp:" in result.output
    
    def test_waivers_show_multiple_commands_same_waiver(self, cli_runner: CliRunner, temp_project: Path):
        """Test showing the same waiver multiple times."""
        manager = WaiverManager()
        waiver = manager.create_waiver("Waiver for multiple shows")
        
        # Run show command twice
        result1 = cli_runner.invoke(app, ["waivers", "show", waiver.waiver_id])
        result2 = cli_runner.invoke(app, ["waivers", "show", waiver.waiver_id])
        
        assert result1.exit_code == 0
        assert result2.exit_code == 0
        assert waiver.waiver_id in result1.output
        assert waiver.waiver_id in result2.output


class TestWaiverCommandIntegration:
    """Integration tests combining list and show commands."""
    
    def test_list_then_show_workflow(self, cli_runner: CliRunner, temp_project: Path):
        """Test workflow: list waivers, then show a specific one."""
        manager = WaiverManager()
        waiver1 = manager.create_waiver("Waiver 1")
        waiver2 = manager.create_waiver("Waiver 2")
        
        # List all waivers
        list_result = cli_runner.invoke(app, ["waivers", "list"])
        assert list_result.exit_code == 0
        assert waiver1.waiver_id in list_result.output
        assert waiver2.waiver_id in list_result.output
        
        # Show specific waiver
        show_result = cli_runner.invoke(app, ["waivers", "show", waiver2.waiver_id])
        assert show_result.exit_code == 0
        assert waiver2.waiver_id in show_result.output
        assert "Waiver 2" in show_result.output
    
    def test_create_list_show_workflow(self, cli_runner: CliRunner, temp_project: Path):
        """Test complete workflow: create, list, show."""
        # Create waiver using create command
        manager = WaiverManager()
        waiver = manager.create_waiver(
            "Integration test waiver",
            related_rules=["R-001"],
            created_by="tester"
        )
        
        # List waivers
        list_result = cli_runner.invoke(app, ["waivers", "list"])
        assert list_result.exit_code == 0
        assert waiver.waiver_id in list_result.output
        
        # Show waiver
        show_result = cli_runner.invoke(app, ["waivers", "show", waiver.waiver_id])
        assert show_result.exit_code == 0
        assert "Integration test waiver" in show_result.output
        assert "R-001" in show_result.output
        assert "tester" in show_result.output
    
    def test_waivers_persistence_across_commands(self, cli_runner: CliRunner, temp_project: Path):
        """Test that waivers persist across multiple command invocations."""
        # Create waivers in first session
        manager1 = WaiverManager()
        waiver1 = manager1.create_waiver("Persistent waiver 1")
        waiver2 = manager1.create_waiver("Persistent waiver 2")
        
        # List in new manager instance
        manager2 = WaiverManager()
        waivers = manager2.list_waivers()
        
        assert len(waivers) == 2
        assert any(w.waiver_id == waiver1.waiver_id for w in waivers)
        assert any(w.waiver_id == waiver2.waiver_id for w in waivers)
        
        # Show via CLI should also see persisted waivers
        result = cli_runner.invoke(app, ["waivers", "show", waiver1.waiver_id])
        assert result.exit_code == 0
        assert waiver1.waiver_id in result.output


class TestWaiverCommandEdgeCases:
    """Edge case tests for waiver commands."""
    
    def test_waivers_list_with_long_reason(self, cli_runner: CliRunner, temp_project: Path):
        """Test listing waivers with very long reasons."""
        manager = WaiverManager()
        long_reason = "A" * 400  # Near the 500 char limit
        waiver = manager.create_waiver(long_reason)
        
        # List should handle long reasons
        result = cli_runner.invoke(app, ["waivers", "list"])
        assert result.exit_code == 0
        assert waiver.waiver_id in result.output
    
    def test_waivers_show_with_special_characters(self, cli_runner: CliRunner, temp_project: Path):
        """Test showing waivers with special characters in reason."""
        manager = WaiverManager()
        special_reason = "Waiver for 'special' chars: @#$%^&*()"
        waiver = manager.create_waiver(special_reason)
        
        result = cli_runner.invoke(app, ["waivers", "show", waiver.waiver_id])
        assert result.exit_code == 0
        assert waiver.waiver_id in result.output
        assert special_reason in result.output
    
    def test_waivers_list_case_sensitivity(self, cli_runner: CliRunner, temp_project: Path):
        """Test that waiver ID case sensitivity is handled correctly."""
        manager = WaiverManager()
        waiver = manager.create_waiver("Test waiver")
        
        # Try to show with lowercase (should fail)
        result_lower = cli_runner.invoke(app, ["waivers", "show", waiver.waiver_id.lower()])
        
        # Try to show with correct case (should work)
        result_correct = cli_runner.invoke(app, ["waivers", "show", waiver.waiver_id])
        
        assert result_lower.exit_code != 0  # Lowercase should fail format check
        assert result_correct.exit_code == 0

