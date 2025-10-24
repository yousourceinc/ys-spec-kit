# Logout command implementation
import subprocess
from pathlib import Path

import typer
from rich.console import Console

console = Console()


def logout_command():
    """
    Clear GitHub OAuth authentication.

    Removes the saved OAuth token from ~/.specify/oauth_token.json

    Examples:
        specify logout
    """
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
            token_file = Path.home() / ".specify" / "oauth_token.json"
            if token_file.exists():
                token_file.unlink()
                console.print("[green]✅ Logged out successfully[/green]")
            else:
                console.print("[yellow]No active session found[/yellow]")
    except Exception as e:
        # Fallback: remove token file directly
        token_file = Path.home() / ".specify" / "oauth_token.json"
        try:
            if token_file.exists():
                token_file.unlink()
                console.print("[green]✅ Logged out successfully[/green]")
            else:
                console.print("[yellow]No active session found[/yellow]")
        except Exception as inner_e:
            console.print(f"[red]Error during logout: {inner_e}[/red]")