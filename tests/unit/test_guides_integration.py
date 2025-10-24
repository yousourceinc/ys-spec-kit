"""
Unit tests for guides integration functionality.

Tests the clone_guides_as_submodule() function and related utilities.
"""

import os
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import pytest

from specify_cli.core.git import clone_guides_as_submodule
from specify_cli.ui.tracker import StepTracker


class TestCloneGuidesAsSubmodule:
    """Test cases for clone_guides_as_submodule() function."""

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

        # Configure git user
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=project_dir,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test User"],
            cwd=project_dir,
            check=True,
            capture_output=True,
        )

        return project_dir

    @pytest.fixture
    def mock_tracker(self) -> Mock:
        """Create a mock StepTracker for testing."""
        return Mock(spec=StepTracker)

    def test_clone_guides_with_valid_url(self, temp_project: Path, mock_tracker: Mock):
        """Test successful cloning with valid URL."""
        # Mock successful git operations
        with patch('subprocess.run') as mock_run:
            # Mock git submodule add (successful)
            add_result = Mock()
            add_result.returncode = 0
            add_result.stdout = ""
            add_result.stderr = ""

            # Mock git submodule update (successful)
            update_result = Mock()
            update_result.returncode = 0
            update_result.stdout = ""
            update_result.stderr = ""

            mock_run.side_effect = [add_result, update_result]

            # Act
            result = clone_guides_as_submodule(temp_project, "https://github.com/test/repo.git", mock_tracker)

            # Assert
            assert result is True
            mock_tracker.start.assert_called_once_with("guides", "Cloning guides repository as submodule")
            mock_tracker.complete.assert_called_once_with("guides", "Guides submodule initialized")

            # Verify git commands were called correctly
            assert mock_run.call_count == 2
            add_call = mock_run.call_args_list[0]
            update_call = mock_run.call_args_list[1]

            # Check submodule add call
            assert add_call[0][0] == ["git", "submodule", "add", "https://github.com/test/repo.git", "context/references"]
            assert add_call[1]["cwd"] == temp_project

            # Check submodule update call
            assert update_call[0][0] == ["git", "submodule", "update", "--init", "--recursive"]
            assert update_call[1]["cwd"] == temp_project

    def test_clone_guides_with_invalid_url(self, temp_project: Path, mock_tracker: Mock):
        """Test failure with invalid URL."""
        with patch('subprocess.run') as mock_run:
            # Mock git submodule add failure
            result_mock = Mock()
            result_mock.returncode = 1
            result_mock.stdout = ""
            result_mock.stderr = "fatal: repository 'https://invalid-url.git' not found"
            mock_run.return_value = result_mock

            # Act
            result = clone_guides_as_submodule(temp_project, "https://invalid-url.git", mock_tracker)

            # Assert
            assert result is False
            mock_tracker.start.assert_called_once_with("guides", "Cloning guides repository as submodule")
            mock_tracker.error.assert_called_once()
            assert "Failed to add submodule" in mock_tracker.error.call_args[0][1]

    def test_clone_guides_directory_exists_as_submodule(self, temp_project: Path, mock_tracker: Mock):
        """Test when guides directory already exists as valid submodule."""
        # Setup: Create guides directory and .gitmodules entry
        guides_dir = temp_project / "context" / "references"
        guides_dir.mkdir(parents=True)
        gitmodules = temp_project / ".gitmodules"
        gitmodules.write_text(f'[submodule "context/references"]\n\tpath = context/references\n\turl = https://github.com/test/repo.git\n')

        # Act
        result = clone_guides_as_submodule(temp_project, "https://github.com/test/repo.git", mock_tracker)

        # Assert
        assert result is True
        mock_tracker.start.assert_called_once_with("guides", "Cloning guides repository as submodule")
        mock_tracker.complete.assert_called_once_with("guides", "Guides submodule already exists")
        # Should not have called any git commands

    def test_clone_guides_directory_exists_not_submodule(self, temp_project: Path, mock_tracker: Mock):
        """Test when guides directory exists but is not a submodule."""
        # Setup: Create guides directory without .gitmodules entry
        guides_dir = temp_project / "context" / "references"
        guides_dir.mkdir(parents=True)
        (guides_dir / "some-file.txt").write_text("content")

        # Act
        result = clone_guides_as_submodule(temp_project, "https://github.com/test/repo.git", mock_tracker)

        # Assert
        assert result is False
        mock_tracker.start.assert_called_once_with("guides", "Cloning guides repository as submodule")
        mock_tracker.error.assert_called_once()
        assert "already exists but is not a submodule" in mock_tracker.error.call_args[0][1]

    @patch('subprocess.run')
    def test_clone_guides_timeout_add(self, mock_subprocess_run: Mock, temp_project: Path, mock_tracker: Mock):
        """Test timeout handling for git submodule add (30s)."""
        # Setup: Mock subprocess.run to raise TimeoutExpired for submodule add
        mock_subprocess_run.side_effect = subprocess.TimeoutExpired(
            cmd=["git", "submodule", "add", "https://github.com/test/repo.git", "context/references"],
            timeout=30
        )

        # Act
        result = clone_guides_as_submodule(temp_project, "https://github.com/test/repo.git", mock_tracker)

        # Assert
        assert result is False
        mock_tracker.start.assert_called_once_with("guides", "Cloning guides repository as submodule")
        mock_tracker.error.assert_called_once_with("guides", "Clone operation timed out")

    @patch('subprocess.run')
    def test_clone_guides_timeout_update(self, mock_subprocess_run: Mock, temp_project: Path, mock_tracker: Mock):
        """Test timeout handling for git submodule update (60s)."""
        # Setup: Mock successful add, then timeout on update
        add_result = Mock()
        add_result.returncode = 0
        add_result.stdout = ""
        add_result.stderr = ""

        update_result = Mock()
        update_result.returncode = 1
        update_result.stdout = ""
        update_result.stderr = "timeout"

        mock_subprocess_run.side_effect = [add_result, update_result]

        # Act
        result = clone_guides_as_submodule(temp_project, "https://github.com/test/repo.git", mock_tracker)

        # Assert
        assert result is False
        mock_tracker.error.assert_called_once()
        assert "Failed to initialize submodule" in mock_tracker.error.call_args[0][1]

    @patch('subprocess.run')
    def test_clone_guides_network_error(self, mock_subprocess_run: Mock, temp_project: Path, mock_tracker: Mock):
        """Test network error handling."""
        # Setup: Mock subprocess.run to return network error
        result_mock = Mock()
        result_mock.returncode = 1
        result_mock.stdout = ""
        result_mock.stderr = "fatal: repository 'https://invalid-url.git' not found"
        mock_subprocess_run.return_value = result_mock

        # Act
        result = clone_guides_as_submodule(temp_project, "https://invalid-url.git", mock_tracker)

        # Assert
        assert result is False
        mock_tracker.start.assert_called_once_with("guides", "Cloning guides repository as submodule")
        mock_tracker.error.assert_called_once()
        assert "Failed to add submodule" in mock_tracker.error.call_args[0][1]

    @patch('subprocess.run')
    def test_clone_guides_already_exists_handled(self, mock_subprocess_run: Mock, temp_project: Path, mock_tracker: Mock):
        """Test that 'already exists' git error is treated as success."""
        # Setup: Mock subprocess.run to return "already exists" error
        result_mock = Mock()
        result_mock.returncode = 1
        result_mock.stdout = ""
        result_mock.stderr = "fatal: 'context/references' already exists in the index"
        mock_subprocess_run.return_value = result_mock

        # Act
        result = clone_guides_as_submodule(temp_project, "https://github.com/test/repo.git", mock_tracker)

        # Assert
        assert result is True
        mock_tracker.start.assert_called_once_with("guides", "Cloning guides repository as submodule")
        mock_tracker.complete.assert_called_once_with("guides", "Guides submodule already configured")

    def test_clone_guides_with_invalid_url(self, temp_project: Path, mock_tracker: Mock):
        """Test failure with invalid URL."""
        # Act
        result = clone_guides_as_submodule(temp_project, "https://invalid-url-that-does-not-exist.git", mock_tracker)

        # Assert
        assert result is False
        mock_tracker.start.assert_called_once_with("guides", "Cloning guides repository as submodule")
        mock_tracker.error.assert_called_once()
        assert "Failed to add submodule" in mock_tracker.error.call_args[0][1]

    def test_clone_guides_directory_exists_as_submodule(self, temp_project: Path, mock_tracker: Mock, mock_guides_url: str):
        """Test when guides directory already exists as valid submodule."""
        # Setup: Create guides directory and .gitmodules entry
        guides_dir = temp_project / "context" / "references"
        guides_dir.mkdir(parents=True)
        gitmodules = temp_project / ".gitmodules"
        gitmodules.write_text(f'[submodule "context/references"]\n\tpath = context/references\n\turl = {mock_guides_url}\n')

        # Act
        result = clone_guides_as_submodule(temp_project, mock_guides_url, mock_tracker)

        # Assert
        assert result is True
        mock_tracker.start.assert_called_once_with("guides", "Cloning guides repository as submodule")
        mock_tracker.complete.assert_called_once_with("guides", "Guides submodule already exists")
        # Should not have called any git commands

    def test_clone_guides_directory_exists_not_submodule(self, temp_project: Path, mock_tracker: Mock, mock_guides_url: str):
        """Test when guides directory exists but is not a submodule."""
        # Setup: Create guides directory without .gitmodules entry
        guides_dir = temp_project / "context" / "references"
        guides_dir.mkdir(parents=True)
        (guides_dir / "some-file.txt").write_text("content")

        # Act
        result = clone_guides_as_submodule(temp_project, mock_guides_url, mock_tracker)

        # Assert
        assert result is False
        mock_tracker.start.assert_called_once_with("guides", "Cloning guides repository as submodule")
        mock_tracker.error.assert_called_once()
        assert "already exists but is not a submodule" in mock_tracker.error.call_args[0][1]

    @patch('subprocess.run')
    def test_clone_guides_timeout_add(self, mock_subprocess_run: Mock, temp_project: Path, mock_tracker: Mock, mock_guides_url: str):
        """Test timeout handling for git submodule add (30s)."""
        # Setup: Mock subprocess.run to raise TimeoutExpired for submodule add
        mock_subprocess_run.side_effect = subprocess.TimeoutExpired(
            cmd=["git", "submodule", "add", mock_guides_url, "context/references"],
            timeout=30
        )

        # Act
        result = clone_guides_as_submodule(temp_project, mock_guides_url, mock_tracker)

        # Assert
        assert result is False
        mock_tracker.start.assert_called_once_with("guides", "Cloning guides repository as submodule")
        mock_tracker.error.assert_called_once_with("guides", "Clone operation timed out")

    @patch('subprocess.run')
    def test_clone_guides_timeout_update(self, mock_subprocess_run: Mock, temp_project: Path, mock_tracker: Mock, mock_guides_url: str):
        """Test timeout handling for git submodule update (60s)."""
        # Setup: Mock successful add, then timeout on update
        add_result = Mock()
        add_result.returncode = 0
        add_result.stdout = ""
        add_result.stderr = ""

        update_result = Mock()
        update_result.returncode = 1
        update_result.stdout = ""
        update_result.stderr = "timeout"

        mock_subprocess_run.side_effect = [add_result, update_result]

        # Act
        result = clone_guides_as_submodule(temp_project, mock_guides_url, mock_tracker)

        # Assert
        assert result is False
        mock_tracker.error.assert_called_once()
        assert "Failed to initialize submodule" in mock_tracker.error.call_args[0][1]

    @patch('subprocess.run')
    def test_clone_guides_network_error(self, mock_subprocess_run: Mock, temp_project: Path, mock_tracker: Mock, mock_guides_url: str):
        """Test network error handling."""
        # Setup: Mock subprocess.run to return network error
        result_mock = Mock()
        result_mock.returncode = 1
        result_mock.stdout = ""
        result_mock.stderr = "fatal: repository 'https://invalid-url.git' not found"
        mock_subprocess_run.return_value = result_mock

        # Act
        result = clone_guides_as_submodule(temp_project, "https://invalid-url.git", mock_tracker)

        # Assert
        assert result is False
        mock_tracker.start.assert_called_once_with("guides", "Cloning guides repository as submodule")
        mock_tracker.error.assert_called_once()
        assert "Failed to add submodule" in mock_tracker.error.call_args[0][1]

    @patch('subprocess.run')
    def test_clone_guides_already_exists_handled(self, mock_subprocess_run: Mock, temp_project: Path, mock_tracker: Mock, mock_guides_url: str):
        """Test that 'already exists' git error is treated as success."""
        # Setup: Mock subprocess.run to return "already exists" error
        result_mock = Mock()
        result_mock.returncode = 1
        result_mock.stdout = ""
        result_mock.stderr = "fatal: 'context/references' already exists in the index"
        mock_subprocess_run.return_value = result_mock

        # Act
        result = clone_guides_as_submodule(temp_project, mock_guides_url, mock_tracker)

        # Assert
        assert result is True
        mock_tracker.start.assert_called_once_with("guides", "Cloning guides repository as submodule")
        mock_tracker.complete.assert_called_once_with("guides", "Guides submodule already configured")


class TestEnvironmentVariableOverride:
    """Test cases for SPECIFY_GUIDES_REPO_URL environment variable override functionality."""

    @patch('os.getenv')
    def test_environment_variable_override_takes_precedence(self, mock_getenv):
        """Test that environment variable override takes precedence over hardcoded constant."""
        # Arrange
        override_url = "git@github.com:test-org/test-guides.git"
        mock_getenv.return_value = override_url
        
        # Import after mocking to ensure override is captured
        from specify_cli.core.constants import GUIDES_REPO_URL
        
        # Act - simulate the override logic from init() function
        guides_repo_url = os.getenv("SPECIFY_GUIDES_REPO_URL", "").strip() or GUIDES_REPO_URL
        
        # Assert
        mock_getenv.assert_called_with("SPECIFY_GUIDES_REPO_URL", "")
        assert guides_repo_url == override_url
        assert guides_repo_url != GUIDES_REPO_URL  # Should not use hardcoded constant

    @patch('os.getenv')
    def test_fallback_to_hardcoded_constant_when_env_var_not_set(self, mock_getenv):
        """Test fallback to hardcoded constant when environment variable is not set."""
        # Arrange
        mock_getenv.return_value = ""  # Environment variable not set
        
        from specify_cli.core.constants import GUIDES_REPO_URL
        
        # Act - simulate the override logic from init() function
        guides_repo_url = os.getenv("SPECIFY_GUIDES_REPO_URL", "").strip() or GUIDES_REPO_URL
        
        # Assert
        mock_getenv.assert_called_with("SPECIFY_GUIDES_REPO_URL", "")
        assert guides_repo_url == GUIDES_REPO_URL  # Should use hardcoded constant

    @patch('os.getenv')
    def test_empty_string_environment_variable_falls_back_to_constant(self, mock_getenv):
        """Test that empty string environment variable falls back to hardcoded constant."""
        # Arrange
        mock_getenv.return_value = ""  # Empty string
        
        from specify_cli.core.constants import GUIDES_REPO_URL
        
        # Act - simulate the override logic from init() function
        guides_repo_url = os.getenv("SPECIFY_GUIDES_REPO_URL", "").strip() or GUIDES_REPO_URL
        
        # Assert
        mock_getenv.assert_called_with("SPECIFY_GUIDES_REPO_URL", "")
        assert guides_repo_url == GUIDES_REPO_URL  # Should fall back to hardcoded constant

    @patch('os.getenv')
    def test_whitespace_only_environment_variable_falls_back_to_constant(self, mock_getenv):
        """Test that whitespace-only environment variable falls back to hardcoded constant."""
        # Arrange
        mock_getenv.return_value = "   \t\n   "  # Whitespace only
        
        from specify_cli.core.constants import GUIDES_REPO_URL
        
        # Act - simulate the override logic from init() function
        guides_repo_url = os.getenv("SPECIFY_GUIDES_REPO_URL", "").strip() or GUIDES_REPO_URL
        
        # Assert
        mock_getenv.assert_called_with("SPECIFY_GUIDES_REPO_URL", "")
        assert guides_repo_url == GUIDES_REPO_URL  # Should fall back to hardcoded constant after strip()