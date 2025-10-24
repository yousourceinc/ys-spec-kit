"""
Integration tests for SPECIFY_GUIDES_REPO_URL environment variable override functionality.

Tests the environment variable override mechanism for the guides repository URL.
These tests focus on the core workflow functions rather than the full CLI to avoid
interactive input requirements.
"""

import os
import subprocess
from pathlib import Path
from unittest.mock import Mock, patch
import pytest

from specify_cli.core.git import clone_guides_as_submodule
from specify_cli.ui.tracker import StepTracker


class TestEnvironmentVariableOverrideIntegration:
    """Integration tests for SPECIFY_GUIDES_REPO_URL environment variable override functionality."""

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
        
        return project_dir

    @pytest.fixture
    def mock_tracker(self) -> Mock:
        """Create a mock StepTracker for testing."""
        return Mock(spec=StepTracker)

    @patch('subprocess.run')
    def test_environment_override_workflow_with_mock_success(self, mock_subprocess_run: Mock, temp_project: Path, mock_tracker: Mock):
        """Test environment variable override workflow with mocked subprocess calls."""
        # Setup: Mock all git operations to succeed
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_subprocess_run.return_value = mock_result

        override_url = "git@github.com:test-org/test-guides.git"

        # Set environment variable
        old_env = os.environ.get('SPECIFY_GUIDES_REPO_URL')
        try:
            os.environ['SPECIFY_GUIDES_REPO_URL'] = override_url

            # Simulate the environment variable override logic from init() function
            guides_repo_url = os.getenv("SPECIFY_GUIDES_REPO_URL", "").strip()
            if not guides_repo_url:
                from specify_cli.core.constants import GUIDES_REPO_URL
                guides_repo_url = GUIDES_REPO_URL

            # Act: Call clone_guides_as_submodule with override URL
            result = clone_guides_as_submodule(temp_project, guides_repo_url, mock_tracker)

            # Assert
            assert result is True
            assert guides_repo_url == override_url

            # Verify git submodule add was called with override URL
            add_calls = [call for call in mock_subprocess_run.call_args_list 
                        if len(call[0]) > 0 and isinstance(call[0][0], list) and 'submodule' in call[0][0] and 'add' in call[0][0]]
            assert len(add_calls) > 0
            
            # Check that override URL was used in the submodule add call
            found_override_url = False
            for call in mock_subprocess_run.call_args_list:
                args = call[0][0] if call[0] else []
                if isinstance(args, list) and override_url in args:
                    found_override_url = True
                    break
            assert found_override_url, f"Override URL {override_url} not found in subprocess calls"

        finally:
            # Restore environment
            if old_env is not None:
                os.environ['SPECIFY_GUIDES_REPO_URL'] = old_env
            elif 'SPECIFY_GUIDES_REPO_URL' in os.environ:
                del os.environ['SPECIFY_GUIDES_REPO_URL']

    @patch('subprocess.run')
    def test_environment_override_with_invalid_url_workflow(self, mock_subprocess_run: Mock, temp_project: Path, mock_tracker: Mock):
        """Test environment variable override workflow with invalid URL."""
        # Setup: Mock git operations to fail with repository not found
        mock_result = Mock()
        mock_result.returncode = 128
        mock_result.stdout = ""
        mock_result.stderr = "fatal: repository 'git@github.com:invalid/repo.git' not found"
        mock_subprocess_run.return_value = mock_result

        invalid_url = "git@github.com:invalid/repo.git"

        # Set environment variable to invalid URL
        old_env = os.environ.get('SPECIFY_GUIDES_REPO_URL')
        try:
            os.environ['SPECIFY_GUIDES_REPO_URL'] = invalid_url

            # Simulate the environment variable override logic from init() function
            guides_repo_url = os.getenv("SPECIFY_GUIDES_REPO_URL", "").strip()
            if not guides_repo_url:
                from specify_cli import GUIDES_REPO_URL
                guides_repo_url = GUIDES_REPO_URL

            # Act: Call clone_guides_as_submodule with invalid URL (should fail)
            result = clone_guides_as_submodule(temp_project, guides_repo_url, mock_tracker)

            # Assert
            assert result is False  # Should fail due to invalid URL
            assert guides_repo_url == invalid_url

            # Verify error was tracked
            mock_tracker.error.assert_called()

        finally:
            # Restore environment
            if old_env is not None:
                os.environ['SPECIFY_GUIDES_REPO_URL'] = old_env
            elif 'SPECIFY_GUIDES_REPO_URL' in os.environ:
                del os.environ['SPECIFY_GUIDES_REPO_URL']

    @patch('subprocess.run')
    def test_environment_override_empty_falls_back_to_hardcoded_workflow(self, mock_subprocess_run: Mock, temp_project: Path, mock_tracker: Mock):
        """Test environment variable override workflow when env var is empty falls back to hardcoded URL."""
        # Setup: Mock all git operations to succeed
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_subprocess_run.return_value = mock_result

        # Set environment variable to empty string
        old_env = os.environ.get('SPECIFY_GUIDES_REPO_URL')
        try:
            os.environ['SPECIFY_GUIDES_REPO_URL'] = ""

            # Simulate the environment variable override logic from init() function
            guides_repo_url = os.getenv("SPECIFY_GUIDES_REPO_URL", "").strip()
            if not guides_repo_url:
                from specify_cli import GUIDES_REPO_URL
                guides_repo_url = GUIDES_REPO_URL

            # Act: Call clone_guides_as_submodule (should use hardcoded URL)
            result = clone_guides_as_submodule(temp_project, guides_repo_url, mock_tracker)

            # Assert
            assert result is True
            from specify_cli.core.constants import GUIDES_REPO_URL
            assert guides_repo_url == GUIDES_REPO_URL  # Should fall back to hardcoded constant

            # Verify git submodule add was called with hardcoded URL
            add_calls = [call for call in mock_subprocess_run.call_args_list 
                        if len(call[0]) > 0 and isinstance(call[0][0], list) and 'submodule' in call[0][0] and 'add' in call[0][0]]
            assert len(add_calls) > 0
            
            # Check that hardcoded URL was used in the submodule add call
            found_hardcoded_url = False
            for call in mock_subprocess_run.call_args_list:
                args = call[0][0] if call[0] else []
                if isinstance(args, list) and GUIDES_REPO_URL in args:
                    found_hardcoded_url = True
                    break
            assert found_hardcoded_url, f"Hardcoded URL {GUIDES_REPO_URL} not found in subprocess calls"

        finally:
            # Restore environment
            if old_env is not None:
                os.environ['SPECIFY_GUIDES_REPO_URL'] = old_env
            elif 'SPECIFY_GUIDES_REPO_URL' in os.environ:
                del os.environ['SPECIFY_GUIDES_REPO_URL']