"""
Shared pytest fixtures and utilities for specify-cli tests.

This module provides:
- Fixtures for temporary directories, git repositories, and mock guides repos
- Helper functions for git operations and test utilities
- Configuration for pytest and test discovery
"""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Generator
import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests that is cleaned up afterward."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def temp_project(temp_dir: Path) -> Generator[Path, None, None]:
    """Create a temporary directory initialized as a git repository."""
    project_dir = temp_dir / "test_project"
    project_dir.mkdir()
    
    # Initialize as git repository
    subprocess.run(
        ["git", "init"],
        cwd=project_dir,
        check=True,
        capture_output=True,
    )
    
    # Configure git user for commit operations
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
    
    yield project_dir


@pytest.fixture
def mock_guides_repo(temp_dir: Path) -> Generator[Path, None, None]:
    """Create a mock guides repository that can be used as a submodule source."""
    guides_repo = temp_dir / "mock_guides"
    guides_repo.mkdir()
    
    # Initialize as bare git repository (suitable for submodule)
    subprocess.run(
        ["git", "init", "--bare"],
        cwd=guides_repo,
        check=True,
        capture_output=True,
    )
    
    # Create a temporary clone to add content
    clone_dir = temp_dir / "mock_guides_clone"
    subprocess.run(
        ["git", "clone", str(guides_repo), str(clone_dir)],
        check=True,
        capture_output=True,
    )
    
    # Configure git user
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=clone_dir,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=clone_dir,
        check=True,
        capture_output=True,
    )
    
    # Add initial content
    readme_path = clone_dir / "README.md"
    readme_path.write_text("# Mock Implementation Guides\n\nThis is a test guides repository.\n")
    
    # Create guides directory structure
    (clone_dir / "guides").mkdir()
    (clone_dir / "guides" / "getting-started.md").write_text("# Getting Started\n\nGuide content here.\n")
    
    # Commit and push
    subprocess.run(
        ["git", "add", "."],
        cwd=clone_dir,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "commit", "-m", "Initial commit"],
        cwd=clone_dir,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "push"],
        cwd=clone_dir,
        check=True,
        capture_output=True,
    )
    
    yield guides_repo


@pytest.fixture
def mock_guides_url(mock_guides_repo: Path) -> str:
    """Get the file:// URL for the mock guides repository."""
    return f"file://{mock_guides_repo}"


def run_git_command(
    cmd: list[str],
    cwd: Path,
    timeout: int = 10,
    check: bool = True,
) -> subprocess.CompletedProcess:
    """
    Run a git command in the specified directory.
    
    Args:
        cmd: List of command arguments (e.g., ["git", "submodule", "add", "..."])
        cwd: Working directory for the command
        timeout: Timeout in seconds
        check: Raise CalledProcessError if return code is non-zero
        
    Returns:
        CompletedProcess with stdout, stderr, returncode
    """
    return subprocess.run(
        cmd,
        cwd=cwd,
        timeout=timeout,
        capture_output=True,
        text=True,
        check=check,
    )


def get_git_remote_url(repo_dir: Path) -> str:
    """Get the remote URL of a git repository."""
    result = run_git_command(
        ["git", "config", "get", "remote.origin.url"],
        repo_dir,
    )
    return result.stdout.strip()


def git_submodule_exists(repo_dir: Path, submodule_path: str) -> bool:
    """Check if a git submodule exists in a repository."""
    gitmodules_path = repo_dir / ".gitmodules"
    if not gitmodules_path.exists():
        return False
    
    content = gitmodules_path.read_text()
    return f'path = {submodule_path}' in content


def git_submodule_url(repo_dir: Path, submodule_path: str) -> str | None:
    """Get the URL of a git submodule if it exists."""
    if not git_submodule_exists(repo_dir, submodule_path):
        return None
    
    result = run_git_command(
        ["git", "config", "-f", ".gitmodules", "get", f"submodule.{submodule_path}.url"],
        repo_dir,
    )
    return result.stdout.strip() if result.returncode == 0 else None


@pytest.fixture
def mock_env_override() -> dict[str, str]:
    """
    Fixture providing environment variable overrides for testing.
    
    Returns a dict that can be merged with os.environ for testing
    override mechanisms.
    """
    return {
        "SPECIFY_GUIDES_REPO_URL": "",
    }


def assert_directory_is_git_repo(path: Path) -> None:
    """Assert that a directory is a valid git repository."""
    git_dir = path / ".git"
    assert git_dir.exists(), f"Directory {path} is not a git repository (.git missing)"


def assert_submodule_initialized(repo_dir: Path, submodule_path: str) -> None:
    """Assert that a git submodule is properly initialized."""
    gitmodules = repo_dir / ".gitmodules"
    assert gitmodules.exists(), f".gitmodules file not found in {repo_dir}"
    
    submodule_dir = repo_dir / submodule_path
    assert submodule_dir.exists(), f"Submodule directory {submodule_path} does not exist"
    
    # Check that submodule has content
    files = list(submodule_dir.iterdir())
    assert len(files) > 0, f"Submodule directory {submodule_path} is empty"
