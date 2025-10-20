"""
Integration tests for specify guides update command.

Tests the guides update functionality to ensure developers can update guides
to the latest version in existing projects.
"""

import os
import subprocess
from pathlib import Path
from unittest.mock import Mock, patch
import pytest
import click.exceptions

from specify_cli import *


class TestGuidesUpdateIntegration:
    """Integration tests for specify guides update command."""

    @pytest.fixture
    def temp_project(self, tmp_path: Path) -> Path:
        """Create a temporary git repository for testing."""
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()

        # Initialize as git repository
        subprocess.run(
            ["git", "init"],
            cwd=project_dir,
            check=True,
            capture_output=True,
        )

        # Create guides directory structure (simulate what init does)
        guides_dir = project_dir / "context" / "references"
        guides_dir.mkdir(parents=True)

        # Create a dummy .gitmodules file to simulate submodule setup
        gitmodules_content = """[submodule "context/references"]
	path = context/references
	url = https://github.com/spec-driven/guides.git
"""
        gitmodules_path = project_dir / ".gitmodules"
        gitmodules_path.write_text(gitmodules_content)

        return project_dir

    @patch('subprocess.run')
    def test_guides_update_successful_updates_submodule_to_latest_commit(self, mock_subprocess_run: Mock, temp_project: Path):
        """Test specify guides update updates submodule to latest commit."""
        def mock_run_side_effect(*args, **kwargs):
            cmd = args[0]
            if 'submodule' in cmd and 'update' in cmd:
                # Mock successful submodule update
                result = Mock()
                result.returncode = 0
                result.stdout = ""
                result.stderr = ""
                return result
            elif 'status' in cmd:
                # Mock git status showing no changes
                result = Mock()
                result.returncode = 0
                result.stdout = ""
                result.stderr = ""
                return result
            else:
                # Default mock
                result = Mock()
                result.returncode = 0
                result.stdout = ""
                result.stderr = ""
                return result

        mock_subprocess_run.side_effect = mock_run_side_effect

        # Change to temp directory
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_project)

            # Act: Run update_guides function directly
            update_guides()  # Should complete successfully without raising

            # Verify git submodule update --remote --merge was called
            update_calls = [call for call in mock_subprocess_run.call_args_list 
                          if len(call[0]) > 0 and isinstance(call[0][0], list) and 
                          'submodule' in call[0][0] and 'update' in call[0][0] and '--remote' in call[0][0]]
            assert len(update_calls) > 0

        finally:
            os.chdir(original_cwd)

    @patch('subprocess.run')
    def test_guides_update_shows_changes_and_prompts_for_commit_when_changes_detected(self, mock_subprocess_run: Mock, temp_project: Path):
        """Test specify guides update shows changes and prompts for commit when changes detected."""
        def mock_run_side_effect(*args, **kwargs):
            cmd = args[0]
            if 'submodule' in cmd and 'update' in cmd:
                # Mock successful submodule update
                result = Mock()
                result.returncode = 0
                result.stdout = ""
                result.stderr = ""
                return result
            elif 'status' in cmd:
                # Mock git status showing changes
                result = Mock()
                result.returncode = 0
                result.stdout = " M context/references/README.md\n M context/references/guides/patterns.md\n"
                result.stderr = ""
                return result
            else:
                # Default mock
                result = Mock()
                result.returncode = 0
                result.stdout = ""
                result.stderr = ""
                return result

        mock_subprocess_run.side_effect = mock_run_side_effect

        # Change to temp directory
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_project)

            # Act: Run update_guides function directly
            update_guides()  # Should complete successfully

        finally:
            os.chdir(original_cwd)

    @patch('subprocess.run')
    def test_guides_update_shows_already_up_to_date_when_no_changes(self, mock_subprocess_run: Mock, temp_project: Path):
        """Test specify guides update shows 'already up to date' when no changes."""
        def mock_run_side_effect(*args, **kwargs):
            cmd = args[0]
            if 'submodule' in cmd and 'update' in cmd:
                # Mock successful submodule update
                result = Mock()
                result.returncode = 0
                result.stdout = ""
                result.stderr = ""
                return result
            elif 'status' in cmd:
                # Mock git status showing no changes
                result = Mock()
                result.returncode = 0
                result.stdout = ""
                result.stderr = ""
                return result
            else:
                # Default mock
                result = Mock()
                result.returncode = 0
                result.stdout = ""
                result.stderr = ""
                return result

        mock_subprocess_run.side_effect = mock_run_side_effect

        # Change to temp directory
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_project)

            # Act: Run update_guides function directly
            update_guides()  # Should complete successfully

        finally:
            os.chdir(original_cwd)

    def test_guides_update_fails_gracefully_when_no_guides_present(self, tmp_path: Path):
        """Test specify guides update fails gracefully when no guides present."""
        # Create a project without guides
        project_dir = tmp_path / "test_project_no_guides"
        project_dir.mkdir()

        # Initialize as git repository but don't add guides
        subprocess.run(
            ["git", "init"],
            cwd=project_dir,
            check=True,
            capture_output=True,
        )

        # Change to temp directory
        original_cwd = os.getcwd()
        try:
            os.chdir(project_dir)

            # Act: Run update_guides function directly
            with pytest.raises(click.exceptions.Exit) as exc_info:
                update_guides()

            # Assert exit code 0 (graceful failure for missing guides)
            assert exc_info.value.exit_code == 0

        finally:
            os.chdir(original_cwd)

    def test_guides_update_fails_gracefully_when_not_in_git_repository(self, tmp_path: Path):
        """Test specify guides update fails gracefully when not in git repository."""
        # Create a directory that's not a git repository
        project_dir = tmp_path / "test_project_no_git"
        project_dir.mkdir()

        # Create guides directory
        guides_dir = project_dir / "context" / "references"
        guides_dir.mkdir(parents=True)

        # Change to temp directory
        original_cwd = os.getcwd()
        try:
            os.chdir(project_dir)

            # Act: Run update_guides function directly
            with pytest.raises(click.exceptions.Exit) as exc_info:
                update_guides()

            # Assert exit code 1 (error for not git repo)
            assert exc_info.value.exit_code == 1

        finally:
            os.chdir(original_cwd)

    @patch('subprocess.run')
    def test_guides_update_handles_directory_exists_but_not_submodule_error(self, mock_subprocess_run: Mock, temp_project: Path):
        """Test specify guides update handles directory exists but not submodule error."""
        def mock_run_side_effect(*args, **kwargs):
            cmd = args[0]
            if 'submodule' in cmd and 'update' in cmd:
                # Mock submodule update failure with "no submodule mapping" error
                result = Mock()
                result.returncode = 1
                result.stdout = ""
                result.stderr = "fatal: no submodule mapping found in .gitmodules for path 'context/references'"
                return result
            else:
                # Default mock
                result = Mock()
                result.returncode = 0
                result.stdout = ""
                result.stderr = ""
                return result

        mock_subprocess_run.side_effect = mock_run_side_effect

        # Change to temp directory
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_project)

            # Act: Run update_guides function directly
            with pytest.raises(click.exceptions.Exit) as exc_info:
                update_guides()

            # Assert exit code 1 (error)
            assert exc_info.value.exit_code == 1

        finally:
            os.chdir(original_cwd)