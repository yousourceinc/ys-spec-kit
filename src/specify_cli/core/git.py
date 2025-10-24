# Core utilities for Specify CLI
import os
import subprocess
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Optional, Tuple

import httpx
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

import ssl
import truststore

from .constants import CLAUDE_LOCAL_PATH
from ..ui.tracker import StepTracker

ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
console = Console()


def run_command(cmd: list[str], check_return: bool = True, capture: bool = False, shell: bool = False) -> Optional[str]:
    """Run a shell command and optionally capture output."""
    try:
        if capture:
            result = subprocess.run(cmd, check=check_return, capture_output=True, text=True, shell=shell)
            return result.stdout.strip()
        else:
            subprocess.run(cmd, check=check_return, shell=shell)
            return None
    except subprocess.CalledProcessError as e:
        if check_return:
            console.print(f"[red]Error running command:[/red] {' '.join(cmd)}")
            console.print(f"[red]Exit code:[/red] {e.returncode}")
            if hasattr(e, 'stderr') and e.stderr:
                console.print(f"[red]Error output:[/red] {e.stderr}")
            raise
        return None


def check_tool_for_tracker(tool: str, tracker: StepTracker) -> bool:
    """Check if a tool is installed and update tracker."""
    if shutil.which(tool):
        tracker.complete(tool, "available")
        return True
    else:
        tracker.error(tool, "not found")
        return False


def check_tool(tool: str, install_hint: str) -> bool:
    """Check if a tool is installed."""

    # Special handling for Claude CLI after `claude migrate-installer`
    # See: https://github.com/github/spec-kit/issues/123
    # The migrate-installer command REMOVES the original executable from PATH
    # and creates an alias at ~/.claude/local/claude instead
    # This path should be prioritized over other claude executables in PATH
    if tool == "claude":
        if CLAUDE_LOCAL_PATH.exists() and CLAUDE_LOCAL_PATH.is_file():
            return True

    if shutil.which(tool):
        return True
    else:
        return False


def is_git_repo(path: Path = None) -> bool:
    """Check if the specified path is inside a git repository."""
    if path is None:
        path = Path.cwd()

    if not path.is_dir():
        return False

    try:
        # Use git command to check if inside a work tree
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            cwd=path,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def init_git_repo(project_path: Path, quiet: bool = False) -> bool:
    """Initialize a git repository in the specified path.
    quiet: if True suppress console output (tracker handles status)
    """
    try:
        original_cwd = Path.cwd()
        os.chdir(project_path)
        if not quiet:
            console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial commit from Specify template"], check=True, capture_output=True)
        if not quiet:
            console.print("[green]✓[/green] Git repository initialized")
        return True

    except subprocess.CalledProcessError as e:
        if not quiet:
            console.print(f"[red]Error initializing git repository:[/red] {e}")
        return False
    finally:
        os.chdir(original_cwd)


def clone_guides_as_submodule(project_path: Path, guides_repo_url: str, tracker: StepTracker | None = None) -> bool:
    """Clone implementation guides as a git submodule in context/references/.

    Returns True if successful, False otherwise.
    Requires an existing git repository in project_path.
    """
    try:
        guides_dir = project_path / "context" / "references"

        if tracker:
            tracker.start("guides", "Cloning guides repository as submodule")

        # Check if guides directory already exists
        if guides_dir.exists():
            # Check if it's already a valid submodule
            gitmodules_path = project_path / ".gitmodules"
            if gitmodules_path.exists():
                gitmodules_content = gitmodules_path.read_text()
                if str(guides_dir.relative_to(project_path)) in gitmodules_content:
                    if tracker:
                        tracker.complete("guides", "Guides submodule already exists")
                    else:
                        console.print("[yellow]Note:[/yellow] Implementation guides submodule already exists")
                    return True

            # Directory exists but not a submodule - error
            if tracker:
                tracker.error("guides", f"Directory {guides_dir} already exists but is not a submodule")
            else:
                console.print(f"[red]Error:[/red] Directory {guides_dir} already exists but is not a submodule")
            return False

        # Create context directory if it doesn't exist
        guides_dir.parent.mkdir(parents=True, exist_ok=True)

        # Add git submodule
        result = subprocess.run(
            ["git", "submodule", "add", guides_repo_url, str(guides_dir.relative_to(project_path))],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            error_msg = result.stderr or result.stdout
            # Check if it's the "already exists" error
            if "already exists" in error_msg.lower():
                if tracker:
                    tracker.complete("guides", "Guides submodule already configured")
                else:
                    console.print("[yellow]Note:[/yellow] Guides submodule already configured")
                return True

            if tracker:
                tracker.error("guides", f"Failed to add submodule: {error_msg}")
            else:
                console.print(f"[red]Error adding guides submodule:[/red] {error_msg}")
            return False

        # Initialize and update the submodule
        result = subprocess.run(
            ["git", "submodule", "update", "--init", "--recursive"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            error_msg = result.stderr or result.stdout
            if tracker:
                tracker.error("guides", f"Failed to initialize submodule: {error_msg}")
            else:
                console.print(f"[red]Error initializing guides submodule:[/red] {error_msg}")
            return False

        if tracker:
            tracker.complete("guides", "Guides submodule initialized")
        else:
            console.print("[green]✓[/green] Implementation guides cloned successfully")

        return True

    except subprocess.TimeoutExpired:
        if tracker:
            tracker.error("guides", "Clone operation timed out")
        else:
            console.print("[red]Error:[/red] Guides repository clone timed out")
        return False
    except Exception as e:
        if tracker:
            tracker.error("guides", str(e))
        else:
            console.print(f"[red]Error cloning guides:[/red] {e}")
        return False