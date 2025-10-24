# Guides command implementation
import subprocess
from pathlib import Path

import typer
from rich.console import Console

from ..core.git import check_tool, is_git_repo
from ..ui.tracker import show_banner

console = Console()


def guides_command(
    action: str = typer.Argument(
        ...,
        help="Action to perform: update"
    )
):
    """
    Manage implementation guides in your project.

    Guides are implementation patterns and best practices bundled with your project.
    They are automatically available in context/references/ and referenced by AI agents
    during /specify, /plan, and /tasks commands.

    Currently supported command:
        specify guides update    Update guides to the latest version using git submodule

    The update command runs 'git submodule update --remote --merge' to fetch the latest
    changes from the guides repository. After updating, you'll see a list of changed files
    (if any) and instructions on how to commit them to your project.

    Future commands (planned):
        specify guides search    Search guides by keyword
        specify guides show      Display a specific guide

    Note: Guide repository configuration is set at the binary level via the
    SPECIFY_GUIDES_REPO_URL environment variable during project initialization.

    Examples:
        specify guides update
    """

    if action == "update":
        update_guides()
    else:
        console.print(f"[red]Error:[/red] Unknown action: {action}")
        console.print("Available actions: update")
        console.print("\nPlanned actions (not yet implemented): search, show")
        raise typer.Exit(1)


def update_guides():
    """Update guides to the latest version using git submodule update."""
    show_banner()

    project_path = Path.cwd()
    guides_path = project_path / "context" / "references"

    console.print("[bold]Updating implementation guides...[/bold]\n")

    # Check if guides directory exists
    if not guides_path.exists():
        console.print(
            "[yellow]⚠[/yellow]  No implementation guides found in this project."
        )
        console.print(f"[dim]Expected location: {guides_path}[/dim]")
        console.print("\n[dim]Guides are configured via SPECIFY_GUIDES_REPO_URL environment variable")
        console.print("[dim]during project initialization with 'specify init'.[/dim]")
        raise typer.Exit(0)

    # Check if this is a git repository
    if not is_git_repo(project_path):
        console.print(
            "[red]Error:[/red] Current directory is not a git repository."
        )
        console.print("[dim]Guides management requires git.[/dim]")
        raise typer.Exit(1)

    # Check if git is available
    if not check_tool("git", "https://git-scm.com/downloads"):
        console.print("[red]Error:[/red] git is not installed or not in PATH")
        raise typer.Exit(1)

    try:
        # Update submodule to latest version
        console.print("[cyan]Fetching latest changes from guides repository...[/cyan]")

        result = subprocess.run(
            ["git", "submodule", "update", "--remote", "--merge"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            console.print("[green]✓[/green] Implementation guides updated to latest version")

            # Show what changed (if anything)
            status_result = subprocess.run(
                ["git", "status", "--short", str(guides_path)],
                cwd=project_path,
                capture_output=True,
                text=True
            )

            if status_result.stdout.strip():
                console.print("\n[cyan]Changes detected:[/cyan]")
                console.print(status_result.stdout)
                console.print("\n[dim]To commit these changes:[/dim]")
                console.print(f"  [cyan]git add {guides_path.relative_to(project_path)}[/cyan]")
                console.print(f"  [cyan]git commit -m 'Update implementation guides'[/cyan]")
            else:
                console.print("[dim]Guides are already up to date[/dim]")
        else:
            error_msg = result.stderr or result.stdout

            # Check if it's not a submodule error
            if "not a git repository" in error_msg.lower() or "no submodule mapping" in error_msg.lower():
                console.print(
                    "[yellow]⚠[/yellow]  Guides directory exists but is not configured as a git submodule."
                )
                console.print(f"[dim]Directory: {guides_path}[/dim]")
                console.print("\n[dim]This might happen if guides were added manually.")
                console.print("[dim]Consider re-initializing with SPECIFY_GUIDES_REPO_URL set.[/dim]")
            else:
                console.print(f"[red]Error updating guides:[/red] {error_msg}")

            raise typer.Exit(1)

    except subprocess.TimeoutExpired:
        console.print("[red]Error:[/red] Update operation timed out")
        console.print("[dim]The guides repository might be too large or network is slow.[/dim]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error updating guides:[/red] {e}")
        raise typer.Exit(1)