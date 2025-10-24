"""
Edge case and verification tests for guides integration functionality.

Tests edge cases, error conditions, and implementation verification for User Story 1.
"""

import os
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
import pytest

from specify_cli.core.git import clone_guides_as_submodule


class TestGuidesEdgeCases:
    """Edge case tests for guides integration."""

    @pytest.fixture
    def temp_project(self, tmp_path: Path) -> Path:
        """Create a temporary directory for testing."""
        return tmp_path / "test_project"

    def test_clone_guides_with_empty_url(self, temp_project: Path):
        """Test handling of empty guides URL."""
        # Setup: Initialize git repository
        temp_project.mkdir()
        subprocess.run(["git", "init"], cwd=temp_project, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=temp_project, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=temp_project, check=True)

                                        # Act: Attempt to clone with network error
        from specify_cli.ui.tracker import StepTracker
        tracker = StepTracker("Test")
        result = clone_guides_as_submodule(temp_project, "", tracker)

        # Assert: Should fail gracefully
        assert result is False

    def test_clone_guides_with_whitespace_url(self, temp_project: Path):
        """Test handling of whitespace-only guides URL."""
        # Setup: Initialize git repository
        temp_project.mkdir()
        subprocess.run(["git", "init"], cwd=temp_project, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=temp_project, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=temp_project, check=True)

        # Act: Attempt to clone with whitespace URL
        from specify_cli.ui.tracker import StepTracker
        tracker = StepTracker("Test")
        result = clone_guides_as_submodule(temp_project, "   ", tracker)

        # Assert: Should fail gracefully
        assert result is False

    def test_clone_guides_with_malformed_url(self, temp_project: Path):
        """Test handling of malformed URLs."""
        # Setup: Initialize git repository
        temp_project.mkdir()
        subprocess.run(["git", "init"], cwd=temp_project, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=temp_project, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=temp_project, check=True)

        # Mock git failure with malformed URL
        with patch('subprocess.run') as mock_subprocess_run:
            mock_result = Mock()
            mock_result.returncode = 1
            mock_result.stdout = ""
            mock_result.stderr = "fatal: 'not-a-url' is not a valid URL"
            mock_subprocess_run.return_value = mock_result

            # Act: Attempt to clone with malformed URL
            from specify_cli.ui.tracker import StepTracker
            tracker = StepTracker("Test")
            result = clone_guides_as_submodule(temp_project, "not-a-url", tracker)

            # Assert: Should fail
            assert result is False

    def test_clone_guides_with_network_timeout(self, temp_project: Path):
        """Test handling of network timeouts during clone."""
        # Setup: Initialize git repository
        temp_project.mkdir()
        subprocess.run(["git", "init"], cwd=temp_project, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=temp_project, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=temp_project, check=True)

        # Mock timeout on submodule add
        with patch('subprocess.run') as mock_subprocess_run:
            from subprocess import TimeoutExpired
            mock_subprocess_run.side_effect = TimeoutExpired(
                cmd=["git", "submodule", "add", "https://github.com/test/repo.git", "context/references"],
                timeout=30
            )

            # Act: Attempt to clone (should timeout)
            from specify_cli.ui.tracker import StepTracker
            tracker = StepTracker("Test")
            result = clone_guides_as_submodule(temp_project, "https://github.com/test/repo.git", tracker)

            # Assert: Should fail due to timeout
            assert result is False

    def test_clone_guides_with_permission_denied(self, temp_project: Path):
        """Test handling of permission denied errors."""
        # Setup: Initialize git repository
        temp_project.mkdir()
        subprocess.run(["git", "init"], cwd=temp_project, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=temp_project, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=temp_project, check=True)

        # Mock permission denied error
        with patch('subprocess.run') as mock_subprocess_run:
            mock_result = Mock()
            mock_result.returncode = 1
            mock_result.stdout = ""
            mock_result.stderr = "fatal: could not create work tree dir 'context/references': Permission denied"
            mock_subprocess_run.return_value = mock_result

            # Act: Attempt to clone
            from specify_cli.ui.tracker import StepTracker
            tracker = StepTracker("Test")
            result = clone_guides_as_submodule(temp_project, "https://github.com/test/repo.git", tracker)

            # Assert: Should fail
            assert result is False

    def test_clone_guides_with_disk_full(self, temp_project: Path):
        """Test handling of disk full errors."""
        # Setup: Initialize git repository
        temp_project.mkdir()
        subprocess.run(["git", "init"], cwd=temp_project, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=temp_project, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=temp_project, check=True)

        # Mock disk full error
        with patch('subprocess.run') as mock_subprocess_run:
            mock_result = Mock()
            mock_result.returncode = 1
            mock_result.stdout = ""
            mock_result.stderr = "fatal: write error: No space left on device"
            mock_subprocess_run.return_value = mock_result

            # Act: Attempt to clone
            from specify_cli.ui.tracker import StepTracker
            tracker = StepTracker("Test")
            result = clone_guides_as_submodule(temp_project, "https://github.com/test/repo.git", tracker)

            # Assert: Should fail
            assert result is False

    def test_clone_guides_with_corrupt_repository(self, temp_project: Path):
        """Test handling of corrupt remote repository."""
        # Setup: Initialize git repository
        temp_project.mkdir()
        subprocess.run(["git", "init"], cwd=temp_project, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=temp_project, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=temp_project, check=True)

        # Mock corrupt repository error
        with patch('subprocess.run') as mock_subprocess_run:
            mock_result = Mock()
            mock_result.returncode = 1
            mock_result.stdout = ""
            mock_result.stderr = "fatal: remote did not send all necessary objects"
            mock_subprocess_run.return_value = mock_result

            # Act: Attempt to clone
            from specify_cli.ui.tracker import StepTracker
            tracker = StepTracker("Test")
            result = clone_guides_as_submodule(temp_project, "https://github.com/test/corrupt-repo.git", tracker)

            # Assert: Should fail
            assert result is False

    def test_clone_guides_with_nonexistent_remote_branch(self, temp_project: Path):
        """Test handling of nonexistent remote branch."""
        # Setup: Initialize git repository
        temp_project.mkdir()
        subprocess.run(["git", "init"], cwd=temp_project, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=temp_project, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=temp_project, check=True)

        # Mock nonexistent branch error
        with patch('subprocess.run') as mock_subprocess_run:
            mock_result = Mock()
            mock_result.returncode = 1
            mock_result.stdout = ""
            mock_result.stderr = "fatal: remote branch nonexistent-branch not found in upstream origin"
            mock_subprocess_run.return_value = mock_result

            # Act: Attempt to clone
            from specify_cli.ui.tracker import StepTracker
            tracker = StepTracker("Test")
            result = clone_guides_as_submodule(temp_project, "https://github.com/test/repo.git", tracker)

            # Assert: Should fail
            assert result is False

    def test_clone_guides_with_authentication_failure(self, temp_project: Path):
        """Test handling of authentication failures."""
        # Setup: Initialize git repository
        temp_project.mkdir()
        subprocess.run(["git", "init"], cwd=temp_project, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=temp_project, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=temp_project, check=True)

        # Mock authentication failure
        with patch('subprocess.run') as mock_subprocess_run:
            mock_result = Mock()
            mock_result.returncode = 1
            mock_result.stdout = ""
            mock_result.stderr = "fatal: Authentication failed for 'https://github.com/private/repo.git/'"
            mock_subprocess_run.return_value = mock_result

            # Act: Attempt to clone private repo
            from specify_cli.ui.tracker import StepTracker
            tracker = StepTracker("Test")
            result = clone_guides_as_submodule(temp_project, "https://github.com/private/repo.git", tracker)

            # Assert: Should fail
            assert result is False

    def test_clone_guides_with_large_repository(self, temp_project: Path):
        """Test handling of large repository (timeout on update)."""
        # Setup: Initialize git repository
        temp_project.mkdir()
        subprocess.run(["git", "init"], cwd=temp_project, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=temp_project, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=temp_project, check=True)

        # Mock successful add but timeout on update
        with patch('subprocess.run') as mock_subprocess_run:
            add_result = Mock()
            add_result.returncode = 0
            add_result.stdout = ""
            add_result.stderr = ""

            update_result = Mock()
            update_result.returncode = 1
            update_result.stdout = ""
            update_result.stderr = "timeout"

            mock_subprocess_run.side_effect = [add_result, update_result]

            # Act: Attempt to clone large repo
            from specify_cli.ui.tracker import StepTracker
            tracker = StepTracker("Test")
            result = clone_guides_as_submodule(temp_project, "https://github.com/test/large-repo.git", tracker)

            # Assert: Should fail due to update timeout
            assert result is False