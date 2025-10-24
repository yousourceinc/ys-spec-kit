# Waivers subcommands implementation
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ..governance.waiver import WaiverManager

console = Console()


def create_waivers_app():
    """Create the waivers subcommand group."""
    waivers_app = typer.Typer(
        name="waivers",
        help="Manage compliance waivers",
        add_completion=False,
    )

    @waivers_app.command()
    def list(
        verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed information"),
    ):
        """
        List all active compliance waivers.

        Displays all waivers in chronological order with ID, reason, and timestamp.
        Use --verbose for full details including related rules.

        Example:
            specify waivers list
            specify waivers list --verbose
        """
        try:
            manager = WaiverManager()
            waivers = manager.list_waivers()

            if not waivers:
                console.print("[yellow]⚠[/yellow]  No waivers found")
                console.print("[dim]Run 'specify waive-requirement' to create a waiver[/dim]")
                return

            console.print(f"\n[bold]Compliance Waivers[/bold] ({len(waivers)} total)\n")

            if verbose:
                # Show detailed view with all waiver information
                for waiver in waivers:
                    panel_content = (
                        f"[bright_blue]ID:[/bright_blue] {waiver.waiver_id}\n"
                        f"[bright_blue]Reason:[/bright_blue] {waiver.reason}\n"
                        f"[bright_blue]Timestamp:[/bright_blue] {waiver.timestamp}"
                    )

                    if waiver.created_by:
                        panel_content += f"\n[bright_blue]Created By:[/bright_blue] {waiver.created_by}"

                    if waiver.related_rules:
                        rules_str = ", ".join(waiver.related_rules)
                        panel_content += f"\n[bright_blue]Related Rules:[/bright_blue] {rules_str}"

                    console.print(
                        Panel(
                            panel_content,
                            title=f"Waiver {waiver.waiver_id}",
                            border_style="bright_blue",
                        )
                    )
                    console.print()
            else:
                # Show table view for quick overview
                table = Table(title="Active Waivers", show_header=True, header_style="bold bright_blue")
                table.add_column("ID", style="cyan")
                table.add_column("Reason", style="white", max_width=60)
                table.add_column("Timestamp", style="dim")

                for waiver in waivers:
                    # Truncate reason if too long
                    reason = waiver.reason[:57] + "..." if len(waiver.reason) > 60 else waiver.reason
                    table.add_row(waiver.waiver_id, reason, waiver.timestamp)

                console.print(table)
                console.print()
                console.print("[dim]Use 'specify waivers show <id>' for detailed information[/dim]")
                console.print("[dim]Use 'specify waivers list --verbose' to see all details[/dim]")

        except Exception as e:
            console.print(f"[red]Error listing waivers:[/red] {str(e)}")
            raise typer.Exit(1)

    @waivers_app.command()
    def show(
        waiver_id: str = typer.Argument(..., help="Waiver ID to display (e.g., W-001)"),
    ):
        """
        Display detailed information about a specific waiver.

        Shows the waiver reason, timestamp, related rules, and creation metadata.

        Example:
            specify waivers show W-001
        """
        try:
            # Validate waiver ID format
            if not waiver_id.startswith("W-"):
                console.print("[red]Error:[/red] Waiver ID must start with 'W-' (e.g., W-001)")
                raise typer.Exit(1)

            manager = WaiverManager()
            waiver = manager.get_waiver_by_id(waiver_id)

            if not waiver:
                console.print(f"[red]Error:[/red] Waiver {waiver_id} not found")
                console.print("[dim]Run 'specify waivers list' to see all waivers[/dim]")
                raise typer.Exit(1)

            # Display waiver details
            console.print()
            panel_content = (
                f"[bright_blue]ID:[/bright_blue] {waiver.waiver_id}\n\n"
                f"[bright_blue]Reason:[/bright_blue]\n{waiver.reason}\n\n"
                f"[bright_blue]Timestamp:[/bright_blue] {waiver.timestamp}"
            )

            if waiver.created_by:
                panel_content += f"\n\n[bright_blue]Created By:[/bright_blue] {waiver.created_by}"

            if waiver.related_rules:
                rules_str = ", ".join(waiver.related_rules)
                panel_content += f"\n\n[bright_blue]Related Rules:[/bright_blue]\n{rules_str}"

            console.print(
                Panel(
                    panel_content,
                    title=f"Waiver Details: {waiver.waiver_id}",
                    border_style="bright_blue",
                    expand=False,
                )
            )
            console.print()

        except typer.Exit:
            raise
        except Exception as e:
            console.print(f"[red]Error retrieving waiver:[/red] {str(e)}")
            raise typer.Exit(1)

    return waivers_app