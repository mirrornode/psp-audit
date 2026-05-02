import click
from rich.console import Console
from rich.table import Table
from psp import __version__
from psp.cli.audit import run_audit, save_audit
from psp.cli.report import render_report

console = Console()


@click.group()
@click.version_option(__version__, prog_name="psp")
def main():
    """Repo-Snap Pistol Shrimp — one scan, one report, one recovery plan."""
    pass


@main.command()
@click.argument("owner_repo")
@click.option("--snapshot", is_flag=True, default=False, help="Capture settings snapshot.")
@click.option("--out", default="audit.json", show_default=True, help="Output file.")
@click.option("--token", default=None, envvar="GITHUB_TOKEN", help="GitHub token.")
def audit(owner_repo, snapshot, out, token):
    """Audit OWNER/REPO and write audit.json."""
    console.print(f"[bold cyan]PSP[/] auditing [bold]{owner_repo}[/]...")
    try:
        payload = run_audit(owner_repo, snapshot=snapshot, token=token)
        path = save_audit(payload, out)

        table = Table(title=f"Audit: {owner_repo}")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="white")
        table.add_row("Branches", str(len(payload["refs"])))
        table.add_row("Tags", str(len(payload["tags"])))
        table.add_row("Workflows", str(len(payload["workflows"])))
        table.add_row("Risk findings", str(len(payload["Risky"])))
        table.add_row("Recent commits", str(len(payload["Changed"])))
        console.print(table)

        if payload["Risky"]:
            console.print("\n[bold red]Risk findings:[/]")
            for f in payload["Risky"]:
                console.print(f"  [{f['severity']}] {f['id']}: {f['description']}")

        if payload["NextSteps"]:
            console.print("\n[bold yellow]Next steps:[/]")
            for s in payload["NextSteps"]:
                console.print(f"  → {s}")

        console.print(f"\n[green]Saved → {path}[/]")

    except Exception as e:
        console.print(f"[red]Error:[/] {e}")
        raise SystemExit(1)


@main.command()
@click.argument("audit_file", default="audit.json")
@click.option("--format", "fmt", type=click.Choice(["json", "txt"]), default="txt", show_default=True)
def report(audit_file, fmt):
    """Render a report from AUDIT_FILE."""
    try:
        console.print(render_report(audit_file, fmt))
    except Exception as e:
        console.print(f"[red]Error:[/] {e}")
        raise SystemExit(1)
