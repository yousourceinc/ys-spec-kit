# Check compliance command implementation
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

from ..governance.compliance import ComplianceChecker, RuleStatus
from ..governance.report import ComplianceReportGenerator

console = Console()


def check_compliance_command():
    """
    Check code compliance against implementation guides.

    Evaluates all rules defined in implementation guides, generates a compliance
    report with pass/fail/waived status, and cross-references waivers.

    Creates: compliance-report.md

    Example:
        specify check-compliance
    """
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