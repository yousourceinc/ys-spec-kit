"""
Integration tests for guides integration functionality.

Tests the end-to-end behavior of guides integration during project initialization.
"""

import os
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
import pytest

from specify_cli import clone_guides_as_submodule, init_git_repo, is_git_repo


class TestGuidesIntegrationWorkflow:
    """Integration tests for the complete guides integration workflow."""

    @pytest.fixture
    def temp_project(self, tmp_path: Path) -> Path:
        """Create a temporary directory for testing."""
        return tmp_path / "test_project"

    def test_complete_guides_integration_workflow(self, temp_project: Path):
        """Test the complete workflow of initializing a project with guides."""
        # Setup: Initialize git repository first
        temp_project.mkdir()
        subprocess.run(["git", "init"], cwd=temp_project, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=temp_project, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=temp_project, check=True)

        # Verify git repo is initialized
        assert is_git_repo(temp_project)

        # Mock the git submodule operations
        with patch('subprocess.run') as mock_subprocess_run:
            # Setup mock responses for successful submodule operations
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = ""
            mock_result.stderr = ""
            mock_subprocess_run.return_value = mock_result

            # Act: Clone guides as submodule
            from specify_cli import StepTracker
            tracker = StepTracker("Test")
            result = clone_guides_as_submodule(temp_project, "https://github.com/spec-driven/guides.git", tracker)

            # Assert: Operation succeeded
            assert result is True

            # Verify git commands were called correctly
            assert mock_subprocess_run.call_count == 2

            # Check submodule add call
            add_call = mock_subprocess_run.call_args_list[0]
            assert add_call[0][0] == ["git", "submodule", "add", "https://github.com/spec-driven/guides.git", "context/references"]
            assert add_call[1]["cwd"] == temp_project

            # Check submodule update call
            update_call = mock_subprocess_run.call_args_list[1]
            assert update_call[0][0] == ["git", "submodule", "update", "--init", "--recursive"]
            assert update_call[1]["cwd"] == temp_project

    def test_guides_integration_with_environment_override(self, temp_project: Path):
        """Test guides integration with environment variable override."""
        # Setup: Initialize git repository
        temp_project.mkdir()
        subprocess.run(["git", "init"], cwd=temp_project, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=temp_project, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=temp_project, check=True)

        # Set environment variable
        custom_url = "https://github.com/custom/guides.git"
        old_env = os.environ.get('SPECIFY_GUIDES_REPO_URL')
        os.environ['SPECIFY_GUIDES_REPO_URL'] = custom_url

        try:
            # Mock the git submodule operations
            with patch('subprocess.run') as mock_subprocess_run:
                mock_result = Mock()
                mock_result.returncode = 0
                mock_result.stdout = ""
                mock_result.stderr = ""
                mock_subprocess_run.return_value = mock_result

                # Act: Clone guides with environment override
                from specify_cli import StepTracker
                tracker = StepTracker("Test")
                result = clone_guides_as_submodule(temp_project, custom_url, tracker)

                # Assert: Operation succeeded
                assert result is True

                # Verify the custom URL was used
                add_call = mock_subprocess_run.call_args_list[0]
                assert add_call[0][0] == ["git", "submodule", "add", custom_url, "context/references"]

        finally:
            # Restore environment
            if old_env is not None:
                os.environ['SPECIFY_GUIDES_REPO_URL'] = old_env
            elif 'SPECIFY_GUIDES_REPO_URL' in os.environ:
                del os.environ['SPECIFY_GUIDES_REPO_URL']

    def test_guides_integration_failure_handling(self, temp_project: Path):
        """Test guides integration failure handling."""
        # Setup: Initialize git repository
        temp_project.mkdir()
        subprocess.run(["git", "init"], cwd=temp_project, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=temp_project, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=temp_project, check=True)

        # Mock git submodule failure
        with patch('subprocess.run') as mock_subprocess_run:
            mock_result = Mock()
            mock_result.returncode = 1
            mock_result.stdout = ""
            mock_result.stderr = "fatal: repository not found"
            mock_subprocess_run.return_value = mock_result

            # Act: Attempt to clone guides
            from specify_cli import StepTracker
            tracker = StepTracker("Test")
            result = clone_guides_as_submodule(temp_project, "https://invalid-url.git", tracker)

            # Assert: Operation failed
            assert result is False

    def test_guides_integration_existing_submodule(self, temp_project: Path):
        """Test guides integration when submodule already exists."""
        # Setup: Initialize git repository and create existing submodule structure
        temp_project.mkdir()
        subprocess.run(["git", "init"], cwd=temp_project, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=temp_project, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=temp_project, check=True)

        # Create guides directory and .gitmodules entry
        guides_dir = temp_project / "context" / "references"
        guides_dir.mkdir(parents=True)
        gitmodules = temp_project / ".gitmodules"
        gitmodules.write_text('[submodule "context/references"]\n\tpath = context/references\n\turl = https://github.com/spec-driven/guides.git\n')

        # Act: Attempt to clone guides (should detect existing)
        from specify_cli import StepTracker
        tracker = StepTracker("Test")
        result = clone_guides_as_submodule(temp_project, "https://github.com/spec-driven/guides.git", tracker)

        # Assert: Operation succeeded (detected existing submodule)
        assert result is True

    def test_guides_integration_directory_conflict(self, temp_project: Path):
        """Test guides integration when directory exists but is not a submodule."""
        # Setup: Initialize git repository and create conflicting directory
        temp_project.mkdir()
        subprocess.run(["git", "init"], cwd=temp_project, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=temp_project, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=temp_project, check=True)

        # Create guides directory without .gitmodules entry
        guides_dir = temp_project / "context" / "references"
        guides_dir.mkdir(parents=True)
        (guides_dir / "some-file.txt").write_text("content")

        # Act: Attempt to clone guides
        from specify_cli import StepTracker
        tracker = StepTracker("Test")
        result = clone_guides_as_submodule(temp_project, "https://github.com/spec-driven/guides.git", tracker)

        # Assert: Operation failed due to directory conflict
        assert result is False

import os
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
import pytest

from specify_cli import app, StepTracker


class TestInitWithGuidesIntegration:
    """Integration tests for specify init command with guides integration."""

    @pytest.fixture
    def temp_project(self, tmp_path: Path) -> Path:
        """Create a temporary directory for testing."""
        return tmp_path / "test_project"

    @pytest.fixture
    def mock_tracker(self) -> Mock:
        """Create a mock StepTracker for testing."""
        return Mock(spec=StepTracker)

    @patch('subprocess.run')
    def test_init_with_guides_successful(self, mock_subprocess_run: Mock, temp_project: Path, tmp_path: Path):
        """Test successful init command with automatic guides integration."""
        # Setup: Mock all git operations to succeed
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_subprocess_run.return_value = mock_result

        # Change to temp directory
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Act: Run specify init (guides integration is automatic)
            from typer.testing import CliRunner
            runner = CliRunner()
            result = runner.invoke(app, ["init", temp_project.name, "--ignore-agent-tools"])

            # Assert
            assert result.exit_code == 0
            assert "Project ready" in result.output or "Project initialized successfully" in result.output

            # Verify guides directory was created
            guides_dir = temp_project / "context" / "references"
            assert guides_dir.exists()

            # Verify .gitmodules was created
            gitmodules = temp_project / ".gitmodules"
            assert gitmodules.exists()
            content = gitmodules.read_text()
            assert "context/references" in content
            assert "https://github.com/spec-driven/guides.git" in content

        finally:
            os.chdir(original_cwd)

    @patch('subprocess.run')
    def test_init_with_custom_guides_url(self, mock_subprocess_run: Mock, temp_project: Path, tmp_path: Path):
        """Test init command with custom guides URL via environment variable."""
        # Setup: Mock all git operations to succeed
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_subprocess_run.return_value = mock_result

        custom_url = "https://github.com/custom/guides.git"

        # Change to temp directory
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Set environment variable
            old_env = os.environ.get('SPECIFY_GUIDES_REPO_URL')
            os.environ['SPECIFY_GUIDES_REPO_URL'] = custom_url

            # Act: Run specify init with custom guides URL via env var
            from typer.testing import CliRunner
            runner = CliRunner()
            result = runner.invoke(app, ["init", temp_project.name, "--ignore-agent-tools"])

            # Assert
            assert result.exit_code == 0
            assert "Project ready" in result.output or "Project initialized successfully" in result.output

            # Verify .gitmodules contains custom URL
            gitmodules = temp_project / ".gitmodules"
            assert gitmodules.exists()
            content = gitmodules.read_text()
            assert custom_url in content

        finally:
            # Restore environment
            if old_env is not None:
                os.environ['SPECIFY_GUIDES_REPO_URL'] = old_env
            elif 'SPECIFY_GUIDES_REPO_URL' in os.environ:
                del os.environ['SPECIFY_GUIDES_REPO_URL']
            os.chdir(original_cwd)

    @patch('subprocess.run')
    def test_init_with_guides_git_failure(self, mock_subprocess_run: Mock, temp_project: Path, tmp_path: Path):
        """Test init command when git submodule operations fail."""
        # Setup: Mock git operations to fail on submodule add
        add_result = Mock()
        add_result.returncode = 1
        add_result.stdout = ""
        add_result.stderr = "fatal: repository not found"

        mock_subprocess_run.return_value = add_result

        # Change to temp directory
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Act: Run specify init with guides failure
            from typer.testing import CliRunner
            runner = CliRunner()
            result = runner.invoke(app, ["init", temp_project.name, "--ignore-agent-tools"])

            # Assert
            assert result.exit_code == 1
            assert "Failed to clone implementation guides" in result.output or "Initialization failed" in result.output

        finally:
            os.chdir(original_cwd)

    @patch('subprocess.run')
    def test_init_without_git_repo(self, mock_subprocess_run: Mock, temp_project: Path, tmp_path: Path):
        """Test init command with --no-git flag (guides should still be attempted but fail)."""
        # Setup: Mock git init to succeed but guides operations to fail appropriately
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_subprocess_run.return_value = mock_result

        # Change to temp directory
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Act: Run specify init with --no-git (guides will fail since no git repo)
            from typer.testing import CliRunner
            runner = CliRunner()
            result = runner.invoke(app, ["init", temp_project.name, "--ignore-agent-tools", "--no-git"])

            # Assert
            assert result.exit_code == 1
            assert "requires git repository" in result.output or "Failed to clone implementation guides" in result.output

        finally:
            os.chdir(original_cwd)

    @patch('subprocess.run')
    def test_init_with_environment_override(self, mock_subprocess_run: Mock, temp_project: Path, tmp_path: Path):
        """Test init command with GUIDES_REPO_URL environment variable override."""
        # Setup: Mock all git operations to succeed
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_subprocess_run.return_value = mock_result

        env_url = "https://github.com/env/guides.git"

        # Change to temp directory
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Set environment variable
            old_env = os.environ.get('GUIDES_REPO_URL')
            os.environ['GUIDES_REPO_URL'] = env_url

            # Act: Run specify init with environment override
            from typer.testing import CliRunner
            runner = CliRunner()
            result = runner.invoke(app, ["init", temp_project.name, "--ignore-agent-tools"])

            # Assert
            assert result.exit_code == 0
            assert "Project ready" in result.output or "Project initialized successfully" in result.output

            # Verify .gitmodules contains environment URL
            gitmodules = temp_project / ".gitmodules"
            assert gitmodules.exists()
            content = gitmodules.read_text()
            assert env_url in content

        finally:
            # Restore environment
            if old_env is not None:
                os.environ['GUIDES_REPO_URL'] = old_env
            elif 'GUIDES_REPO_URL' in os.environ:
                del os.environ['GUIDES_REPO_URL']
            os.chdir(original_cwd)

import os
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
import pytest

from specify_cli import app, StepTracker


class TestInitWithGuidesIntegration:
    """Integration tests for specify init command with guides integration."""

    @pytest.fixture
    def temp_project(self, tmp_path: Path) -> Path:
        """Create a temporary directory for testing."""
        return tmp_path / "test_project"

    @pytest.fixture
    def mock_tracker(self) -> Mock:
        """Create a mock StepTracker for testing."""
        return Mock(spec=StepTracker)

    @patch('subprocess.run')
    def test_init_with_guides_successful(self, mock_subprocess_run: Mock, temp_project: Path, tmp_path: Path):
        """Test successful init command with guides integration."""
        # Setup: Mock all git operations to succeed
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_subprocess_run.return_value = mock_result

        # Change to temp directory
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Act: Run specify init with guides
            from typer.testing import CliRunner
            runner = CliRunner()
            result = runner.invoke(app, ["init", "--guides", temp_project.name])

            # Assert
            assert result.exit_code == 0
            assert "Project initialized successfully" in result.output

            # Verify guides directory was created
            guides_dir = temp_project / "context" / "references"
            assert guides_dir.exists()

            # Verify .gitmodules was created
            gitmodules = temp_project / ".gitmodules"
            assert gitmodules.exists()
            content = gitmodules.read_text()
            assert "context/references" in content
            assert "https://github.com/spec-driven/guides.git" in content

        finally:
            os.chdir(original_cwd)

    @patch('subprocess.run')
    def test_init_with_guides_custom_url(self, mock_subprocess_run: Mock, temp_project: Path, tmp_path: Path):
        """Test init command with custom guides URL."""
        # Setup: Mock all git operations to succeed
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_subprocess_run.return_value = mock_result

        custom_url = "https://github.com/custom/guides.git"

        # Change to temp directory
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Act: Run specify init with custom guides URL
            from typer.testing import CliRunner
            runner = CliRunner()
            result = runner.invoke(app, ["init", "--guides", "--guides-url", custom_url, temp_project.name])

            # Assert
            assert result.exit_code == 0
            assert "Project initialized successfully" in result.output

            # Verify .gitmodules contains custom URL
            gitmodules = temp_project / ".gitmodules"
            assert gitmodules.exists()
            content = gitmodules.read_text()
            assert custom_url in content

        finally:
            os.chdir(original_cwd)

    @patch('subprocess.run')
    def test_init_with_guides_git_failure(self, mock_subprocess_run: Mock, temp_project: Path, tmp_path: Path):
        """Test init command when git submodule operations fail."""
        # Setup: Mock git operations to fail
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "fatal: repository not found"
        mock_subprocess_run.return_value = mock_result

        # Change to temp directory
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Act: Run specify init with guides
            from typer.testing import CliRunner
            runner = CliRunner()
            result = runner.invoke(app, ["init", "--guides", temp_project.name])

            # Assert
            assert result.exit_code == 1
            assert "Failed to initialize guides" in result.output or "Error" in result.output

        finally:
            os.chdir(original_cwd)

    @patch('subprocess.run')
    def test_init_without_guides_flag(self, mock_subprocess_run: Mock, temp_project: Path, tmp_path: Path):
        """Test init command without --guides flag doesn't create guides."""
        # Setup: Mock git init to succeed (but no submodule operations)
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_subprocess_run.return_value = mock_result

        # Change to temp directory
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Act: Run specify init without --guides flag
            from typer.testing import CliRunner
            runner = CliRunner()
            result = runner.invoke(app, ["init", temp_project.name])

            # Assert
            assert result.exit_code == 0
            assert "Project initialized successfully" in result.output

            # Verify guides directory was NOT created
            guides_dir = temp_project / "context" / "references"
            assert not guides_dir.exists()

            # Verify .gitmodules was NOT created
            gitmodules = temp_project / ".gitmodules"
            assert not gitmodules.exists()

        finally:
            os.chdir(original_cwd)

    @patch('subprocess.run')
    def test_init_with_guides_environment_override(self, mock_subprocess_run: Mock, temp_project: Path, tmp_path: Path):
        """Test init command with GUIDES_REPO_URL environment variable override."""
        # Setup: Mock all git operations to succeed
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_subprocess_run.return_value = mock_result

        env_url = "https://github.com/env/guides.git"

        # Change to temp directory
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Set environment variable
            old_env = os.environ.get('GUIDES_REPO_URL')
            os.environ['GUIDES_REPO_URL'] = env_url

            # Act: Run specify init with --guides (no explicit URL)
            from typer.testing import CliRunner
            runner = CliRunner()
            result = runner.invoke(app, ["init", "--guides", temp_project.name])

            # Assert
            assert result.exit_code == 0
            assert "Project initialized successfully" in result.output

            # Verify .gitmodules contains environment URL
            gitmodules = temp_project / ".gitmodules"
            assert gitmodules.exists()
            content = gitmodules.read_text()
            assert env_url in content

        finally:
            # Restore environment
            if old_env is not None:
                os.environ['GUIDES_REPO_URL'] = old_env
            elif 'GUIDES_REPO_URL' in os.environ:
                del os.environ['GUIDES_REPO_URL']
            os.chdir(original_cwd)