#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "typer",
#     "rich",
#     "platformdirs",
#     "readchar",
#     "httpx",
# ]
# ///
"""
Specify CLI - Setup tool for Specify projects

Usage:
    uvx specify-cli.py init <project-name>
    uvx specify-cli.py init .
    uvx specify-cli.py init --here

Or install globally:
    uv tool install --from specify-cli.py specify-cli
    specify init <project-name>
    specify init .
    specify init --here
"""

import os
import subprocess
import sys
import zipfile
import tempfile
import shutil
import shlex
import json
from pathlib import Path
from typing import Optional, Tuple

import typer
import httpx
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.live import Live
from rich.align import Align
from rich.table import Table
from rich.tree import Tree
from typer.core import TyperGroup

# For cross-platform keyboard input
import readchar

# Import config module
from .config import write_project_config, validate_division, get_valid_divisions

# Import governance module
from .governance.waiver import WaiverManager
from .governance.compliance import ComplianceChecker
from .governance.report import ComplianceReportGenerator
import ssl
import truststore

ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
client = httpx.Client(verify=ssl_context)

def _github_token(cli_token: str | None = None) -> str | None:
    """Return sanitized GitHub token (cli arg takes precedence) or None."""
    return ((cli_token or os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN") or "").strip()) or None

def _github_auth_headers(cli_token: str | None = None) -> dict:
    """Return Authorization header dict only when a non-empty token exists."""
    token = _github_token(cli_token)
    return {"Authorization": f"Bearer {token}"} if token else {}

# Constants
AI_CHOICES = {
    "copilot": "GitHub Copilot",
    "claude": "Claude Code",
    "gemini": "Gemini CLI",
    "cursor": "Cursor",
    "qwen": "Qwen Code",
    "opencode": "opencode",
    "codex": "Codex CLI",
    "windsurf": "Windsurf",
    "kilocode": "Kilo Code",
    "auggie": "Auggie CLI",
    "roo": "Roo Code",
    "q": "Amazon Q Developer CLI",
}
# Add script type choices
SCRIPT_TYPE_CHOICES = {"sh": "POSIX Shell (bash/zsh)", "ps": "PowerShell"}

# Official implementation guides repository URL
# This is the canonical source for implementation guides that will be automatically
# integrated into every project initialized with specify init.
# Override: Set SPECIFY_GUIDES_REPO_URL environment variable to use a different repository.
GUIDES_REPO_URL = "git@github.com:yousourceinc/implementation-guides.git"

# Claude CLI local installation path after migrate-installer
CLAUDE_LOCAL_PATH = Path.home() / ".claude" / "local" / "claude"

# ASCII Art Banner
BANNER = """
██╗   ██╗███████╗    ███████╗██████╗ ███████╗ ██████╗██╗███████╗██╗   ██╗
╚██╗ ██╔╝██╔════╝    ██╔════╝██╔══██╗██╔════╝██╔════╝██║██╔════╝╚██╗ ██╔╝
 ╚████╔╝ ███████╗    ███████╗██████╔╝█████╗  ██║     ██║█████╗   ╚████╔╝ 
  ╚██╔╝  ╚════██║    ╚════██║██╔═══╝ ██╔══╝  ██║     ██║██╔══╝    ╚██╔╝  
   ██║   ███████║    ███████║██║     ███████╗╚██████╗██║██║        ██║   
   ╚═╝   ╚══════╝    ╚══════╝╚═╝     ╚══════╝ ╚═════╝╚═╝╚═╝        ╚═╝   
"""

TAGLINE = "YourSource Spec Kit - Spec-Driven Development Toolkit"
class StepTracker:
    """Track and render hierarchical steps without emojis, similar to Claude Code tree output.
    Supports live auto-refresh via an attached refresh callback.
    """
    def __init__(self, title: str):
        self.title = title
        self.steps = []  # list of dicts: {key, label, status, detail}
        self.status_order = {"pending": 0, "running": 1, "done": 2, "error": 3, "skipped": 4}
        self._refresh_cb = None  # callable to trigger UI refresh

    def attach_refresh(self, cb):
        self._refresh_cb = cb

    def add(self, key: str, label: str):
        if key not in [s["key"] for s in self.steps]:
            self.steps.append({"key": key, "label": label, "status": "pending", "detail": ""})
            self._maybe_refresh()

    def start(self, key: str, detail: str = ""):
        self._update(key, status="running", detail=detail)

    def complete(self, key: str, detail: str = ""):
        self._update(key, status="done", detail=detail)

    def error(self, key: str, detail: str = ""):
        self._update(key, status="error", detail=detail)

    def skip(self, key: str, detail: str = ""):
        self._update(key, status="skipped", detail=detail)

    def _update(self, key: str, status: str, detail: str):
        for s in self.steps:
            if s["key"] == key:
                s["status"] = status
                if detail:
                    s["detail"] = detail
                self._maybe_refresh()
                return
        # If not present, add it
        self.steps.append({"key": key, "label": key, "status": status, "detail": detail})
        self._maybe_refresh()

    def _maybe_refresh(self):
        if self._refresh_cb:
            try:
                self._refresh_cb()
            except Exception:
                pass

    def render(self):
        tree = Tree(f"[cyan]{self.title}[/cyan]", guide_style="grey50")
        for step in self.steps:
            label = step["label"]
            detail_text = step["detail"].strip() if step["detail"] else ""

            # Circles (unchanged styling)
            status = step["status"]
            if status == "done":
                symbol = "[green]●[/green]"
            elif status == "pending":
                symbol = "[green dim]○[/green dim]"
            elif status == "running":
                symbol = "[cyan]○[/cyan]"
            elif status == "error":
                symbol = "[red]●[/red]"
            elif status == "skipped":
                symbol = "[yellow]○[/yellow]"
            else:
                symbol = " "

            if status == "pending":
                # Entire line light gray (pending)
                if detail_text:
                    line = f"{symbol} [bright_black]{label} ({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [bright_black]{label}[/bright_black]"
            else:
                # Label white, detail (if any) light gray in parentheses
                if detail_text:
                    line = f"{symbol} [white]{label}[/white] [bright_black]({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [white]{label}[/white]"

            tree.add(line)
        return tree



MINI_BANNER = """
╔═╗╔═╗╔═╗╔═╗╦╔═╗╦ ╦
╚═╗╠═╝║╣ ║  ║╠╣ ╚╦╝
╚═╝╩  ╚═╝╚═╝╩╚   ╩ 
"""

def get_key():
    """Get a single keypress in a cross-platform way using readchar."""
    key = readchar.readkey()
    
    # Arrow keys
    if key == readchar.key.UP or key == readchar.key.CTRL_P:
        return 'up'
    if key == readchar.key.DOWN or key == readchar.key.CTRL_N:
        return 'down'
    
    # Enter/Return
    if key == readchar.key.ENTER:
        return 'enter'
    
    # Escape
    if key == readchar.key.ESC:
        return 'escape'
        
    # Ctrl+C
    if key == readchar.key.CTRL_C:
        raise KeyboardInterrupt

    return key



def select_with_arrows(options: dict, prompt_text: str = "Select an option", default_key: str = None) -> str:
    """
    Interactive selection using arrow keys with Rich Live display.
    
    Args:
        options: Dict with keys as option keys and values as descriptions
        prompt_text: Text to show above the options
        default_key: Default option key to start with
        
    Returns:
        Selected option key
    """
    option_keys = list(options.keys())
    if default_key and default_key in option_keys:
        selected_index = option_keys.index(default_key)
    else:
        selected_index = 0
    
    selected_key = None

    def create_selection_panel():
        """Create the selection panel with current selection highlighted."""
        table = Table.grid(padding=(0, 2))
        table.add_column(style="cyan", justify="left", width=3)
        table.add_column(style="white", justify="left")
        
        for i, key in enumerate(option_keys):
            if i == selected_index:
                table.add_row("▶", f"[cyan]{key}[/cyan] [dim]({options[key]})[/dim]")
            else:
                table.add_row(" ", f"[cyan]{key}[/cyan] [dim]({options[key]})[/dim]")
        
        table.add_row("", "")
        table.add_row("", "[dim]Use ↑/↓ to navigate, Enter to select, Esc to cancel[/dim]")
        
        return Panel(
            table,
            title=f"[bold]{prompt_text}[/bold]",
            border_style="cyan",
            padding=(1, 2)
        )
    
    console.print()

    def run_selection_loop():
        nonlocal selected_key, selected_index
        with Live(create_selection_panel(), console=console, transient=True, auto_refresh=False) as live:
            while True:
                try:
                    key = get_key()
                    if key == 'up':
                        selected_index = (selected_index - 1) % len(option_keys)
                    elif key == 'down':
                        selected_index = (selected_index + 1) % len(option_keys)
                    elif key == 'enter':
                        selected_key = option_keys[selected_index]
                        break
                    elif key == 'escape':
                        console.print("\n[yellow]Selection cancelled[/yellow]")
                        raise typer.Exit(1)
                    
                    live.update(create_selection_panel(), refresh=True)

                except KeyboardInterrupt:
                    console.print("\n[yellow]Selection cancelled[/yellow]")
                    raise typer.Exit(1)

    run_selection_loop()

    if selected_key is None:
        console.print("\n[red]Selection failed.[/red]")
        raise typer.Exit(1)

    # Suppress explicit selection print; tracker / later logic will report consolidated status
    return selected_key



console = Console()


class BannerGroup(TyperGroup):
    """Custom group that shows banner before help."""
    
    def format_help(self, ctx, formatter):
        # Show banner before help
        show_banner()
        super().format_help(ctx, formatter)


app = typer.Typer(
    name="specify",
    help="Setup tool for Specify spec-driven development projects",
    add_completion=False,
    invoke_without_command=True,
    cls=BannerGroup,
)


def show_banner():
    """Display the ASCII art banner."""
    # Create gradient effect with different colors
    banner_lines = BANNER.strip().split('\n')
    colors = ["bright_blue", "blue", "cyan", "bright_cyan", "white", "bright_white"]
    
    styled_banner = Text()
    for i, line in enumerate(banner_lines):
        color = colors[i % len(colors)]
        styled_banner.append(line + "\n", style=color)
    
    console.print(Align.center(styled_banner))
    console.print(Align.center(Text(TAGLINE, style="italic bright_yellow")))
    console.print()


@app.callback()
def callback(ctx: typer.Context):
    """Show banner when no subcommand is provided."""
    # Show banner only when no subcommand and no help flag
    # (help is handled by BannerGroup)
    if ctx.invoked_subcommand is None and "--help" not in sys.argv and "-h" not in sys.argv:
        show_banner()
        console.print(Align.center("[dim]Run 'specify --help' for usage information[/dim]"))
        console.print()


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


def download_template_from_github(ai_assistant: str, download_dir: Path, *, script_type: str = "sh", verbose: bool = True, show_progress: bool = True, client: httpx.Client = None, debug: bool = False, github_token: str = None) -> Tuple[Path, dict]:
    repo_owner = "github"
    repo_name = "spec-kit"
    if client is None:
        client = httpx.Client(verify=ssl_context)
    
    if verbose:
        console.print("[cyan]Fetching latest release information...[/cyan]")
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    
    try:
        response = client.get(
            api_url,
            timeout=30,
            follow_redirects=True,
            headers=_github_auth_headers(github_token),
        )
        status = response.status_code
        if status != 200:
            msg = f"GitHub API returned {status} for {api_url}"
            if debug:
                msg += f"\nResponse headers: {response.headers}\nBody (truncated 500): {response.text[:500]}"
            raise RuntimeError(msg)
        try:
            release_data = response.json()
        except ValueError as je:
            raise RuntimeError(f"Failed to parse release JSON: {je}\nRaw (truncated 400): {response.text[:400]}")
    except Exception as e:
        console.print(f"[red]Error fetching release information[/red]")
        console.print(Panel(str(e), title="Fetch Error", border_style="red"))
        raise typer.Exit(1)
    
    # Find the template asset for the specified AI assistant
    assets = release_data.get("assets", [])
    pattern = f"spec-kit-template-{ai_assistant}-{script_type}"
    matching_assets = [
        asset for asset in assets
        if pattern in asset["name"] and asset["name"].endswith(".zip")
    ]

    asset = matching_assets[0] if matching_assets else None

    if asset is None:
        console.print(f"[red]No matching release asset found[/red] for [bold]{ai_assistant}[/bold] (expected pattern: [bold]{pattern}[/bold])")
        asset_names = [a.get('name', '?') for a in assets]
        console.print(Panel("\n".join(asset_names) or "(no assets)", title="Available Assets", border_style="yellow"))
        raise typer.Exit(1)

    download_url = asset["browser_download_url"]
    filename = asset["name"]
    file_size = asset["size"]
    
    if verbose:
        console.print(f"[cyan]Found template:[/cyan] {filename}")
        console.print(f"[cyan]Size:[/cyan] {file_size:,} bytes")
        console.print(f"[cyan]Release:[/cyan] {release_data['tag_name']}")

    zip_path = download_dir / filename
    if verbose:
        console.print(f"[cyan]Downloading template...[/cyan]")
    
    try:
        with client.stream(
            "GET",
            download_url,
            timeout=60,
            follow_redirects=True,
            headers=_github_auth_headers(github_token),
        ) as response:
            if response.status_code != 200:
                body_sample = response.text[:400]
                raise RuntimeError(f"Download failed with {response.status_code}\nHeaders: {response.headers}\nBody (truncated): {body_sample}")
            total_size = int(response.headers.get('content-length', 0))
            with open(zip_path, 'wb') as f:
                if total_size == 0:
                    for chunk in response.iter_bytes(chunk_size=8192):
                        f.write(chunk)
                else:
                    if show_progress:
                        with Progress(
                            SpinnerColumn(),
                            TextColumn("[progress.description]{task.description}"),
                            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                            console=console,
                        ) as progress:
                            task = progress.add_task("Downloading...", total=total_size)
                            downloaded = 0
                            for chunk in response.iter_bytes(chunk_size=8192):
                                f.write(chunk)
                                downloaded += len(chunk)
                                progress.update(task, completed=downloaded)
                    else:
                        for chunk in response.iter_bytes(chunk_size=8192):
                            f.write(chunk)
    except Exception as e:
        console.print(f"[red]Error downloading template[/red]")
        detail = str(e)
        if zip_path.exists():
            zip_path.unlink()
        console.print(Panel(detail, title="Download Error", border_style="red"))
        raise typer.Exit(1)
    if verbose:
        console.print(f"Downloaded: {filename}")
    metadata = {
        "filename": filename,
        "size": file_size,
        "release": release_data["tag_name"],
        "asset_url": download_url
    }
    return zip_path, metadata


def download_and_extract_template(project_path: Path, ai_assistant: str, script_type: str, is_current_dir: bool = False, *, verbose: bool = True, tracker: StepTracker | None = None, client: httpx.Client = None, debug: bool = False, github_token: str = None) -> Path:
    """Download the latest release and extract it to create a new project.
    Returns project_path. Uses tracker if provided (with keys: fetch, download, extract, cleanup)
    """
    current_dir = Path.cwd()
    
    # Step: fetch + download combined
    if tracker:
        tracker.start("fetch", "contacting GitHub API")
    try:
        zip_path, meta = download_template_from_github(
            ai_assistant,
            current_dir,
            script_type=script_type,
            verbose=verbose and tracker is None,
            show_progress=(tracker is None),
            client=client,
            debug=debug,
            github_token=github_token
        )
        if tracker:
            tracker.complete("fetch", f"release {meta['release']} ({meta['size']:,} bytes)")
            tracker.add("download", "Download template")
            tracker.complete("download", meta['filename'])
    except Exception as e:
        if tracker:
            tracker.error("fetch", str(e))
        else:
            if verbose:
                console.print(f"[red]Error downloading template:[/red] {e}")
        raise
    
    if tracker:
        tracker.add("extract", "Extract template")
        tracker.start("extract")
    elif verbose:
        console.print("Extracting template...")
    
    try:
        # Create project directory only if not using current directory
        if not is_current_dir:
            project_path.mkdir(parents=True)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # List all files in the ZIP for debugging
            zip_contents = zip_ref.namelist()
            if tracker:
                tracker.start("zip-list")
                tracker.complete("zip-list", f"{len(zip_contents)} entries")
            elif verbose:
                console.print(f"[cyan]ZIP contains {len(zip_contents)} items[/cyan]")
            
            # For current directory, extract to a temp location first
            if is_current_dir:
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir)
                    zip_ref.extractall(temp_path)
                    
                    # Check what was extracted
                    extracted_items = list(temp_path.iterdir())
                    if tracker:
                        tracker.start("extracted-summary")
                        tracker.complete("extracted-summary", f"temp {len(extracted_items)} items")
                    elif verbose:
                        console.print(f"[cyan]Extracted {len(extracted_items)} items to temp location[/cyan]")
                    
                    # Handle GitHub-style ZIP with a single root directory
                    source_dir = temp_path
                    if len(extracted_items) == 1 and extracted_items[0].is_dir():
                        source_dir = extracted_items[0]
                        if tracker:
                            tracker.add("flatten", "Flatten nested directory")
                            tracker.complete("flatten")
                        elif verbose:
                            console.print(f"[cyan]Found nested directory structure[/cyan]")
                    
                    # Copy contents to current directory
                    for item in source_dir.iterdir():
                        dest_path = project_path / item.name
                        if item.is_dir():
                            if dest_path.exists():
                                if verbose and not tracker:
                                    console.print(f"[yellow]Merging directory:[/yellow] {item.name}")
                                # Recursively copy directory contents
                                for sub_item in item.rglob('*'):
                                    if sub_item.is_file():
                                        rel_path = sub_item.relative_to(item)
                                        dest_file = dest_path / rel_path
                                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                                        shutil.copy2(sub_item, dest_file)
                            else:
                                shutil.copytree(item, dest_path)
                        else:
                            if dest_path.exists() and verbose and not tracker:
                                console.print(f"[yellow]Overwriting file:[/yellow] {item.name}")
                            shutil.copy2(item, dest_path)
                    if verbose and not tracker:
                        console.print(f"[cyan]Template files merged into current directory[/cyan]")
            else:
                # Extract directly to project directory (original behavior)
                zip_ref.extractall(project_path)
                
                # Check what was extracted
                extracted_items = list(project_path.iterdir())
                if tracker:
                    tracker.start("extracted-summary")
                    tracker.complete("extracted-summary", f"{len(extracted_items)} top-level items")
                elif verbose:
                    console.print(f"[cyan]Extracted {len(extracted_items)} items to {project_path}:[/cyan]")
                    for item in extracted_items:
                        console.print(f"  - {item.name} ({'dir' if item.is_dir() else 'file'})")
                
                # Handle GitHub-style ZIP with a single root directory
                if len(extracted_items) == 1 and extracted_items[0].is_dir():
                    # Move contents up one level
                    nested_dir = extracted_items[0]
                    temp_move_dir = project_path.parent / f"{project_path.name}_temp"
                    # Move the nested directory contents to temp location
                    shutil.move(str(nested_dir), str(temp_move_dir))
                    # Remove the now-empty project directory
                    project_path.rmdir()
                    # Rename temp directory to project directory
                    shutil.move(str(temp_move_dir), str(project_path))
                    if tracker:
                        tracker.add("flatten", "Flatten nested directory")
                        tracker.complete("flatten")
                    elif verbose:
                        console.print(f"[cyan]Flattened nested directory structure[/cyan]")
                    
    except Exception as e:
        if tracker:
            tracker.error("extract", str(e))
        else:
            if verbose:
                console.print(f"[red]Error extracting template:[/red] {e}")
                if debug:
                    console.print(Panel(str(e), title="Extraction Error", border_style="red"))
        # Clean up project directory if created and not current directory
        if not is_current_dir and project_path.exists():
            shutil.rmtree(project_path)
        raise typer.Exit(1)
    else:
        if tracker:
            tracker.complete("extract")
    finally:
        if tracker:
            tracker.add("cleanup", "Remove temporary archive")
        # Clean up downloaded ZIP file
        if zip_path.exists():
            zip_path.unlink()
            if tracker:
                tracker.complete("cleanup")
            elif verbose:
                console.print(f"Cleaned up: {zip_path.name}")
    
    return project_path


def ensure_executable_scripts(project_path: Path, tracker: StepTracker | None = None) -> None:
    """Ensure POSIX .sh scripts under .specify/scripts (recursively) have execute bits (no-op on Windows)."""
    if os.name == "nt":
        return  # Windows: skip silently
    scripts_root = project_path / ".specify" / "scripts"
    if not scripts_root.is_dir():
        return
    failures: list[str] = []
    updated = 0
    for script in scripts_root.rglob("*.sh"):
        try:
            if script.is_symlink() or not script.is_file():
                continue
            try:
                with script.open("rb") as f:
                    if f.read(2) != b"#!":
                        continue
            except Exception:
                continue
            st = script.stat(); mode = st.st_mode
            if mode & 0o111:
                continue
            new_mode = mode
            if mode & 0o400: new_mode |= 0o100
            if mode & 0o040: new_mode |= 0o010
            if mode & 0o004: new_mode |= 0o001
            if not (new_mode & 0o100):
                new_mode |= 0o100
            os.chmod(script, new_mode)
            updated += 1
        except Exception as e:
            failures.append(f"{script.relative_to(scripts_root)}: {e}")
    if tracker:
        detail = f"{updated} updated" + (f", {len(failures)} failed" if failures else "")
        tracker.add("chmod", "Set script permissions recursively")
        (tracker.error if failures else tracker.complete)("chmod", detail)
    else:
        if updated:
            console.print(f"[cyan]Updated execute permissions on {updated} script(s) recursively[/cyan]")
        if failures:
            console.print("[yellow]Some scripts could not be updated:[/yellow]")
            for f in failures:
                console.print(f"  - {f}")

@app.command()
def init(
    project_name: str = typer.Argument(None, help="Name for your new project directory (optional if using --here, or use '.' for current directory)"),
    ai_assistant: str = typer.Option(None, "--ai", help="AI assistant to use: claude, gemini, copilot, cursor, qwen, opencode, codex, windsurf, kilocode, auggie or q"),
    script_type: str = typer.Option(None, "--script", help="Script type to use: sh or ps"),
    ignore_agent_tools: bool = typer.Option(False, "--ignore-agent-tools", help="Skip checks for AI agent tools like Claude Code"),
    no_git: bool = typer.Option(False, "--no-git", help="Skip git repository initialization"),
    here: bool = typer.Option(False, "--here", help="Initialize project in the current directory instead of creating a new one"),
    force: bool = typer.Option(False, "--force", help="Force merge/overwrite when using --here (skip confirmation)"),
    skip_tls: bool = typer.Option(False, "--skip-tls", help="Skip SSL/TLS verification (not recommended)"),
    debug: bool = typer.Option(False, "--debug", help="Show verbose diagnostic output for network and extraction failures"),
    github_token: str = typer.Option(None, "--github-token", help="GitHub token to use for API requests (or set GH_TOKEN or GITHUB_TOKEN environment variable)"),
    division: str = typer.Option(None, "--division", help="Project division for AI guidance: SE, DS, Platform (defaults to SE)"),
):
    """
    Initialize a new Specify project from the latest template.
    
    This command will:
    1. Check that required tools are installed (git is optional)
    2. Let you choose your AI assistant (Claude Code, Gemini CLI, GitHub Copilot, Cursor, Qwen Code, opencode, Codex CLI, Windsurf, Kilo Code, Auggie CLI, or Amazon Q Developer CLI)
    3. Download the appropriate template from GitHub
    4. Extract the template to a new project directory or current directory
    5. Initialize a fresh git repository (if not --no-git and no existing repo)
    6. Configure project division for AI guidance (defaults to SE)
    7. Optionally set up AI assistant commands
    
    Examples:
        specify init my-project
        specify init my-project --ai claude
        specify init my-project --ai gemini
        specify init my-project --ai copilot --no-git
        specify init my-project --ai cursor
        specify init my-project --ai qwen
        specify init my-project --ai opencode
        specify init my-project --ai codex
        specify init my-project --ai windsurf
        specify init my-project --ai auggie
        specify init my-project --ai q
        specify init my-project --division DS
        specify init my-project --ai claude --division Platform
        specify init --ignore-agent-tools my-project
        specify init . --ai claude         # Initialize in current directory
        specify init .                     # Initialize in current directory (interactive AI selection)
        specify init --here --ai claude    # Alternative syntax for current directory
        specify init --here --ai codex
        specify init --here
        specify init --here --force  # Skip confirmation when current directory not empty
    """
    # Show banner first
    show_banner()
    
    # Handle '.' as shorthand for current directory (equivalent to --here)
    if project_name == ".":
        here = True
        project_name = None  # Clear project_name to use existing validation logic
    
    # Validate division early if provided
    if division:
        # We can't validate against guides yet since they haven't been cloned
        # But we can do basic format validation
        if not division or not isinstance(division, str):
            console.print("[red]Error:[/red] Division must be a non-empty string")
            raise typer.Exit(1)
        if not division.replace("-", "").replace("_", "").isalnum():
            console.print(f"[red]Error:[/red] Invalid division format: {division}")
            console.print("[dim]Division must contain only letters, numbers, hyphens, and underscores[/dim]")
            raise typer.Exit(1)
    
    # Validate arguments
    if here and project_name:
        console.print("[red]Error:[/red] Cannot specify both project name and --here flag")
        raise typer.Exit(1)
    
    if not here and not project_name:
        console.print("[red]Error:[/red] Must specify either a project name, use '.' for current directory, or use --here flag")
        raise typer.Exit(1)
    
    # Determine project directory
    if here:
        project_name = Path.cwd().name
        project_path = Path.cwd()
        
        # Check if current directory has any files
        existing_items = list(project_path.iterdir())
        if existing_items:
            console.print(f"[yellow]Warning:[/yellow] Current directory is not empty ({len(existing_items)} items)")
            console.print("[yellow]Template files will be merged with existing content and may overwrite existing files[/yellow]")
            if force:
                console.print("[cyan]--force supplied: skipping confirmation and proceeding with merge[/cyan]")
            else:
                # Ask for confirmation
                response = typer.confirm("Do you want to continue?")
                if not response:
                    console.print("[yellow]Operation cancelled[/yellow]")
                    raise typer.Exit(0)
    else:
        project_path = Path(project_name).resolve()
        # Check if project directory already exists
        if project_path.exists():
            error_panel = Panel(
                f"Directory '[cyan]{project_name}[/cyan]' already exists\n"
                "Please choose a different project name or remove the existing directory.",
                title="[red]Directory Conflict[/red]",
                border_style="red",
                padding=(1, 2)
            )
            console.print()
            console.print(error_panel)
            raise typer.Exit(1)
    
    # Create formatted setup info with column alignment
    current_dir = Path.cwd()
    
    setup_lines = [
        "[cyan]Specify Project Setup[/cyan]",
        "",
        f"{'Project':<15} [green]{project_path.name}[/green]",
        f"{'Working Path':<15} [dim]{current_dir}[/dim]",
    ]
    
    # Add target path only if different from working dir
    if not here:
        setup_lines.append(f"{'Target Path':<15} [dim]{project_path}[/dim]")
    
    console.print(Panel("\n".join(setup_lines), border_style="cyan", padding=(1, 2)))
    
    # Check git only if we might need it (not --no-git)
    # Only set to True if the user wants it and the tool is available
    should_init_git = False
    if not no_git:
        should_init_git = check_tool("git", "https://git-scm.com/downloads")
        if not should_init_git:
            console.print("[yellow]Git not found - will skip repository initialization[/yellow]")

    # AI assistant selection
    if ai_assistant:
        if ai_assistant not in AI_CHOICES:
            console.print(f"[red]Error:[/red] Invalid AI assistant '{ai_assistant}'. Choose from: {', '.join(AI_CHOICES.keys())}")
            raise typer.Exit(1)
        selected_ai = ai_assistant
    else:
        # Use arrow-key selection interface
        selected_ai = select_with_arrows(
            AI_CHOICES, 
            "Choose your AI assistant:", 
            "copilot"
        )
    
    # Check agent tools unless ignored
    if not ignore_agent_tools:
        agent_tool_missing = False
        install_url = ""
        if selected_ai == "claude":
            if not check_tool("claude", "https://docs.anthropic.com/en/docs/claude-code/setup"):
                install_url = "https://docs.anthropic.com/en/docs/claude-code/setup"
                agent_tool_missing = True
        elif selected_ai == "gemini":
            if not check_tool("gemini", "https://github.com/google-gemini/gemini-cli"):
                install_url = "https://github.com/google-gemini/gemini-cli"
                agent_tool_missing = True
        elif selected_ai == "qwen":
            if not check_tool("qwen", "https://github.com/QwenLM/qwen-code"):
                install_url = "https://github.com/QwenLM/qwen-code"
                agent_tool_missing = True
        elif selected_ai == "opencode":
            if not check_tool("opencode", "https://opencode.ai"):
                install_url = "https://opencode.ai"
                agent_tool_missing = True
        elif selected_ai == "codex":
            if not check_tool("codex", "https://github.com/openai/codex"):
                install_url = "https://github.com/openai/codex"
                agent_tool_missing = True
        elif selected_ai == "auggie":
            if not check_tool("auggie", "https://docs.augmentcode.com/cli/setup-auggie/install-auggie-cli"):
                install_url = "https://docs.augmentcode.com/cli/setup-auggie/install-auggie-cli"
                agent_tool_missing = True
        elif selected_ai == "q":
            if not check_tool("q", "https://github.com/aws/amazon-q-developer-cli"):
                install_url = "https://aws.amazon.com/developer/learning/q-developer-cli/"
                agent_tool_missing = True
        # GitHub Copilot and Cursor checks are not needed as they're typically available in supported IDEs

        if agent_tool_missing:
            error_panel = Panel(
                f"[cyan]{selected_ai}[/cyan] not found\n"
                f"Install with: [cyan]{install_url}[/cyan]\n"
                f"{AI_CHOICES[selected_ai]} is required to continue with this project type.\n\n"
                "Tip: Use [cyan]--ignore-agent-tools[/cyan] to skip this check",
                title="[red]Agent Detection Error[/red]",
                border_style="red",
                padding=(1, 2)
            )
            console.print()
            console.print(error_panel)
            raise typer.Exit(1)
    
    # Determine script type (explicit, interactive, or OS default)
    if script_type:
        if script_type not in SCRIPT_TYPE_CHOICES:
            console.print(f"[red]Error:[/red] Invalid script type '{script_type}'. Choose from: {', '.join(SCRIPT_TYPE_CHOICES.keys())}")
            raise typer.Exit(1)
        selected_script = script_type
    else:
        # Auto-detect default
        default_script = "ps" if os.name == "nt" else "sh"
        # Provide interactive selection similar to AI if stdin is a TTY
        if sys.stdin.isatty():
            selected_script = select_with_arrows(SCRIPT_TYPE_CHOICES, "Choose script type (or press Enter)", default_script)
        else:
            selected_script = default_script
    
    console.print(f"[cyan]Selected AI assistant:[/cyan] {selected_ai}")
    console.print(f"[cyan]Selected script type:[/cyan] {selected_script}")
    
    # Download and set up project
    # New tree-based progress (no emojis); include earlier substeps
    tracker = StepTracker("Initialize Specify Project")
    # Flag to allow suppressing legacy headings
    sys._specify_tracker_active = True
    # Pre steps recorded as completed before live rendering
    tracker.add("precheck", "Check required tools")
    tracker.complete("precheck", "ok")
    tracker.add("ai-select", "Select AI assistant")
    tracker.complete("ai-select", f"{selected_ai}")
    tracker.add("script-select", "Select script type")
    tracker.complete("script-select", selected_script)
    for key, label in [
        ("fetch", "Fetch latest release"),
        ("download", "Download template"),
        ("extract", "Extract template"),
        ("zip-list", "Archive contents"),
        ("extracted-summary", "Extraction summary"),
        ("chmod", "Ensure scripts executable"),
        ("cleanup", "Cleanup"),
        ("git", "Initialize git repository"),
        ("guides", "Clone implementation guides"),
        ("division", "Configure project division"),
        ("final", "Finalize")
    ]:
        tracker.add(key, label)

    # Use transient so live tree is replaced by the final static render (avoids duplicate output)
    with Live(tracker.render(), console=console, refresh_per_second=8, transient=True) as live:
        tracker.attach_refresh(lambda: live.update(tracker.render()))
        try:
            # Create a httpx client with verify based on skip_tls
            verify = not skip_tls
            local_ssl_context = ssl_context if verify else False
            local_client = httpx.Client(verify=local_ssl_context)

            download_and_extract_template(project_path, selected_ai, selected_script, here, verbose=False, tracker=tracker, client=local_client, debug=debug, github_token=github_token)

            # Ensure scripts are executable (POSIX)
            ensure_executable_scripts(project_path, tracker=tracker)

            # Git step
            if not no_git:
                tracker.start("git")
                if is_git_repo(project_path):
                    tracker.complete("git", "existing repo detected")
                elif should_init_git:
                    if init_git_repo(project_path, quiet=True):
                        tracker.complete("git", "initialized")
                    else:
                        tracker.error("git", "init failed")
                else:
                    tracker.skip("git", "git not available")
            else:
                tracker.skip("git", "--no-git flag")
            
            # Guides step - always attempt to integrate guides
            # Use environment variable override if set, otherwise use hardcoded URL
            guides_repo_url = os.getenv("SPECIFY_GUIDES_REPO_URL", "").strip() or GUIDES_REPO_URL
            
            if not is_git_repo(project_path):
                tracker.error("guides", "requires git repository")
            else:
                # Always attempt to clone guides (required for all projects)
                if not clone_guides_as_submodule(project_path, guides_repo_url, tracker=tracker):
                    # Clone failed - this is a fatal error since guides are required
                    raise Exception(f"Failed to clone implementation guides from {guides_repo_url}")

            # Division configuration step
            if division:
                tracker.start("division", "Configure project division")
                # Validate division against available guides
                is_valid, error_msg = validate_division(division, project_path)
                if not is_valid:
                    tracker.error("division", error_msg)
                    raise Exception(f"Invalid division '{division}': {error_msg}")
                
                # Write division to project config
                try:
                    write_project_config(project_path, division)
                    tracker.complete("division", f"set to {division}")
                except Exception as e:
                    tracker.error("division", f"failed to write config: {e}")
                    raise Exception(f"Failed to configure division: {e}")
            else:
                # Default to SE division
                tracker.start("division", "Configure project division")
                try:
                    write_project_config(project_path, "SE")
                    tracker.complete("division", "set to SE (default)")
                except Exception as e:
                    tracker.error("division", f"failed to write config: {e}")
                    raise Exception(f"Failed to configure default division: {e}")

            tracker.complete("final", "project ready")
        except Exception as e:
            tracker.error("final", str(e))
            console.print(Panel(f"Initialization failed: {e}", title="Failure", border_style="red"))
            if debug:
                _env_pairs = [
                    ("Python", sys.version.split()[0]),
                    ("Platform", sys.platform),
                    ("CWD", str(Path.cwd())),
                ]
                _label_width = max(len(k) for k, _ in _env_pairs)
                env_lines = [f"{k.ljust(_label_width)} → [bright_black]{v}[/bright_black]" for k, v in _env_pairs]
                console.print(Panel("\n".join(env_lines), title="Debug Environment", border_style="magenta"))
            if not here and project_path.exists():
                shutil.rmtree(project_path)
            raise typer.Exit(1)
        finally:
            # Force final render
            pass

    # Final static tree (ensures finished state visible after Live context ends)
    console.print(tracker.render())
    console.print("\n[bold green]Project ready.[/bold green]")
    
    # Agent folder security notice
    agent_folder_map = {
        "claude": ".claude/",
        "gemini": ".gemini/",
        "cursor": ".cursor/",
        "qwen": ".qwen/",
        "opencode": ".opencode/",
        "codex": ".codex/",
        "windsurf": ".windsurf/",
        "kilocode": ".kilocode/",
        "auggie": ".augment/",
        "copilot": ".github/",
        "roo": ".roo/",
        "q": ".amazonq/"
    }
    
    if selected_ai in agent_folder_map:
        agent_folder = agent_folder_map[selected_ai]
        security_notice = Panel(
            f"Some agents may store credentials, auth tokens, or other identifying and private artifacts in the agent folder within your project.\n"
            f"Consider adding [cyan]{agent_folder}[/cyan] (or parts of it) to [cyan].gitignore[/cyan] to prevent accidental credential leakage.",
            title="[yellow]Agent Folder Security[/yellow]",
            border_style="yellow",
            padding=(1, 2)
        )
        console.print()
        console.print(security_notice)
    
    # Boxed "Next steps" section
    steps_lines = []
    if not here:
        steps_lines.append(f"1. Go to the project folder: [cyan]cd {project_name}[/cyan]")
        step_num = 2
    else:
        steps_lines.append("1. You're already in the project directory!")
        step_num = 2

    # Add Codex-specific setup step if needed
    if selected_ai == "codex":
        codex_path = project_path / ".codex"
        quoted_path = shlex.quote(str(codex_path))
        if os.name == "nt":  # Windows
            cmd = f"setx CODEX_HOME {quoted_path}"
        else:  # Unix-like systems
            cmd = f"export CODEX_HOME={quoted_path}"
        
        steps_lines.append(f"{step_num}. Set [cyan]CODEX_HOME[/cyan] environment variable before running Codex: [cyan]{cmd}[/cyan]")
        step_num += 1

    steps_lines.append(f"{step_num}. Start using slash commands with your AI agent:")

    steps_lines.append("   2.1 [cyan]/constitution[/] - Establish project principles")
    steps_lines.append("   2.2 [cyan]/specify[/] - Create baseline specification")
    steps_lines.append("   2.3 [cyan]/plan[/] - Create implementation plan")
    steps_lines.append("   2.4 [cyan]/tasks[/] - Generate actionable tasks")
    steps_lines.append("   2.5 [cyan]/implement[/] - Execute implementation")

    steps_panel = Panel("\n".join(steps_lines), title="Next Steps", border_style="cyan", padding=(1,2))
    console.print()
    console.print(steps_panel)

    enhancement_lines = [
        "Optional commands that you can use for your specs [bright_black](improve quality & confidence)[/bright_black]",
        "",
        f"○ [cyan]/clarify[/] [bright_black](optional)[/bright_black] - Ask structured questions to de-risk ambiguous areas before planning (run before [cyan]/plan[/] if used)",
        f"○ [cyan]/analyze[/] [bright_black](optional)[/bright_black] - Cross-artifact consistency & alignment report (after [cyan]/tasks[/], before [cyan]/implement[/])"
    ]
    enhancements_panel = Panel("\n".join(enhancement_lines), title="Enhancement Commands", border_style="cyan", padding=(1,2))
    console.print()
    console.print(enhancements_panel)

    if selected_ai == "codex":
        warning_text = """[bold yellow]Important Note:[/bold yellow]

Custom prompts do not yet support arguments in Codex. You may need to manually specify additional project instructions directly in prompt files located in [cyan].codex/prompts/[/cyan].

For more information, see: [cyan]https://github.com/openai/codex/issues/2890[/cyan]"""
        
        warning_panel = Panel(warning_text, title="Slash Commands in Codex", border_style="yellow", padding=(1,2))
        console.print()
        console.print(warning_panel)

@app.command()
def logout():
    """
    Clear GitHub OAuth authentication.
    
    Removes the saved OAuth token from ~/.specify/oauth_token.json
    
    Examples:
        specify logout
    """
    import subprocess
    
    console.print("[cyan]Logging out...[/cyan]")
    
    # Try to call Node.js OAuth logout
    try:
        result = subprocess.run(
            ["node", "-e", "require('./src/auth/github-oauth').logout()"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            console.print("[green]✅ Logged out successfully[/green]")
        else:
            # Fallback: remove token file directly
            import os
            token_file = Path.home() / ".specify" / "oauth_token.json"
            if token_file.exists():
                token_file.unlink()
                console.print("[green]✅ Logged out successfully[/green]")
            else:
                console.print("[yellow]No active session found[/yellow]")
    except Exception as e:
        # Fallback: remove token file directly
        import os
        token_file = Path.home() / ".specify" / "oauth_token.json"
        try:
            if token_file.exists():
                token_file.unlink()
                console.print("[green]✅ Logged out successfully[/green]")
            else:
                console.print("[yellow]No active session found[/yellow]")
        except Exception as inner_e:
            console.print(f"[red]Error during logout: {inner_e}[/red]")

@app.command()
def check():
    """Check that all required tools are installed."""
    show_banner()
    console.print("[bold]Checking for installed tools...[/bold]\n")

    tracker = StepTracker("Check Available Tools")
    
    tracker.add("git", "Git version control")
    tracker.add("claude", "Claude Code CLI")
    tracker.add("gemini", "Gemini CLI")
    tracker.add("qwen", "Qwen Code CLI")
    tracker.add("code", "Visual Studio Code")
    tracker.add("code-insiders", "Visual Studio Code Insiders")
    tracker.add("cursor-agent", "Cursor IDE agent")
    tracker.add("windsurf", "Windsurf IDE")
    tracker.add("kilocode", "Kilo Code IDE")
    tracker.add("opencode", "opencode")
    tracker.add("codex", "Codex CLI")
    tracker.add("auggie", "Auggie CLI")
    tracker.add("q", "Amazon Q Developer CLI")
    
    git_ok = check_tool_for_tracker("git", tracker)
    claude_ok = check_tool_for_tracker("claude", tracker)  
    gemini_ok = check_tool_for_tracker("gemini", tracker)
    qwen_ok = check_tool_for_tracker("qwen", tracker)
    code_ok = check_tool_for_tracker("code", tracker)
    code_insiders_ok = check_tool_for_tracker("code-insiders", tracker)
    cursor_ok = check_tool_for_tracker("cursor-agent", tracker)
    windsurf_ok = check_tool_for_tracker("windsurf", tracker)
    kilocode_ok = check_tool_for_tracker("kilocode", tracker)
    opencode_ok = check_tool_for_tracker("opencode", tracker)
    codex_ok = check_tool_for_tracker("codex", tracker)
    auggie_ok = check_tool_for_tracker("auggie", tracker)
    q_ok = check_tool_for_tracker("q", tracker)

    console.print(tracker.render())

    console.print("\n[bold green]Specify CLI is ready to use![/bold green]")

    if not git_ok:
        console.print("[dim]Tip: Install git for repository management[/dim]")
    if not (claude_ok or gemini_ok or cursor_ok or qwen_ok or windsurf_ok or kilocode_ok or opencode_ok or codex_ok or auggie_ok or q_ok):
        console.print("[dim]Tip: Install an AI assistant for the best experience[/dim]")


@app.command()
def guides(
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


@app.command()
def waive_requirement(
    reason: str = typer.Argument(..., help="Reason for the waiver (max 500 characters)")
):
    """
    Record a formal compliance waiver.
    
    Creates or appends to .specify/waivers.md with structured waiver entry including
    reason, timestamp, and unique identifier.
    
    Example:
        specify waive-requirement "Disabling MFA for service account per ticket #1234"
    """
    console = Console()
    
    try:
        # Validate reason
        if not reason or not reason.strip():
            console.print("[red]Error:[/red] Waiver reason cannot be empty")
            raise typer.Exit(1)
        
        if len(reason) > 500:
            console.print("[red]Error:[/red] Waiver reason exceeds 500 character limit")
            console.print(f"[dim]Current length: {len(reason)} characters[/dim]")
            raise typer.Exit(1)
        
        # Create waiver
        manager = WaiverManager()
        waiver = manager.create_waiver(reason.strip())
        
        # Display success message
        console.print()
        console.print(
            Panel(
                f"[green]✓ Waiver recorded[/green]\n\n"
                f"[bright_blue]ID:[/bright_blue] {waiver.waiver_id}\n"
                f"[bright_blue]Reason:[/bright_blue] {waiver.reason}\n"
                f"[bright_blue]Timestamp:[/bright_blue] {waiver.timestamp}",
                title="Compliance Waiver",
                border_style="green"
            )
        )
        console.print()
        console.print("[dim]Waiver stored in: .specify/waivers.md[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error creating waiver:[/red] {str(e)}")
        raise typer.Exit(1)


@app.command()
def check_compliance():
    """
    Check code compliance against implementation guides.
    
    Evaluates all rules defined in implementation guides, generates a compliance
    report with pass/fail/waived status, and cross-references waivers.
    
    Creates: compliance-report.md
    
    Example:
        specify check-compliance
    """
    console = Console()
    
    try:
        with console.status("[bold cyan]Discovering guides...") as status:
            checker = ComplianceChecker()
            guides = checker._discover_guides()
        
        if not guides:
            console.print("[yellow]⚠[/yellow]  No implementation guides found")
            console.print("[dim]Looking in: context/references/, specs/[/dim]")
            raise typer.Exit(1)
        
        console.print(f"[dim]Found {len(guides)} guide(s)[/dim]")
        
        # Run compliance check
        with console.status("[bold cyan]Checking compliance...") as status:
            results = checker.run_compliance_check(guides)
        
        # Count statuses
        from .governance.compliance import RuleStatus
        pass_count = sum(1 for r in results if r.status == RuleStatus.PASS)
        fail_count = sum(1 for r in results if r.status == RuleStatus.FAIL)
        waived_count = sum(1 for r in results if r.status == RuleStatus.WAIVED)
        error_count = sum(1 for r in results if r.status == RuleStatus.ERROR)
        
        # Display results
        console.print()
        console.print("[bold]Compliance Check Results[/bold]")
        console.print(f"  ✅ Passed: {pass_count}")
        console.print(f"  ❌ Failed: {fail_count}")
        console.print(f"  🚫 Waived: {waived_count}")
        console.print(f"  ⚠️ Errors: {error_count}")
        
        # Generate and write report
        with console.status("[bold cyan]Generating report...") as status:
            generator = ComplianceReportGenerator()
            report_path = generator.generate_and_write_report(
                results,
                project_name=Path.cwd().name
            )
        
        console.print()
        console.print(
            Panel(
                f"[green]✓ Report generated[/green]\n\n"
                f"[bright_blue]Location:[/bright_blue] {report_path.relative_to(Path.cwd())}\n"
                f"[bright_blue]Rules Checked:[/bright_blue] {len(results)}\n"
                f"[bright_blue]Status:[/bright_blue] ",
                title="Compliance Check Complete",
                border_style="green" if fail_count == 0 else "yellow"
            )
        )
        
        # Determine exit code based on failures
        if fail_count > 0:
            console.print("[yellow]⚠ Some rules failed - see report for details[/yellow]")
            raise typer.Exit(1)
        elif error_count > 0:
            console.print("[yellow]⚠ Some errors occurred during evaluation[/yellow]")
            raise typer.Exit(1)
        else:
            console.print("[green]✓ All rules passed![/green]")
    
    except Exception as e:
        console.print(f"[red]Error during compliance check:[/red] {str(e)}")
        raise typer.Exit(1)


def main():
    app()


if __name__ == "__main__":
    main()
