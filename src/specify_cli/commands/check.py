# Check command implementation
import typer
from rich.console import Console

from ..core.git import check_tool_for_tracker
from ..ui.tracker import StepTracker, show_banner

console = Console()


def check_command():
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