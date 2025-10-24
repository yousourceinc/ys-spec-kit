# Waive requirement command implementation
import typer
from rich.console import Console
from rich.panel import Panel

from ..governance.waiver import WaiverManager

console = Console()


def waive_requirement_command(
    reason: str = typer.Argument(..., help="Reason for the waiver (max 500 characters)")
):
    """
    Record a formal compliance waiver.

    Creates or appends to .specify/waivers.md with structured waiver entry including
    reason, timestamp, and unique identifier.

    Example:
        specify waive-requirement "Disabling MFA for service account per ticket #1234"
    """
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