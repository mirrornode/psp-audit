import click
from rich.console import Console
from rich.table import Table
from psp import __version__
from psp.cli.audit import run_audit, save_audit
from psp.cli.report import render_report
from psp.github_client import GitHubClient, RateLimitError, AuthError, NotFoundError

console = Console()


@click.group()
@click.version_option(__version__, prog_name="psp")
def main():
    """Repo-Snap Pistol Shrimp — one scan, one report, one recovery plan."""
    pass


@main.command()
@click.argument("owner_repo")
@click.option("--snapshot", is_flag=True, default=False)
@click.option("--out", default="audit.json", show_default=True)
@click.option("--token", default=None, envvar="GITHUB_TOKEN")
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
                color = "red" if f["severity"] == "High" else "yellow"
                console.print(f"  [[{color}]{f['severity']}[/]] {f['id']}: {f['description']}")

        if payload["NextSteps"]:
            console.print("\n[bold yellow]Next steps:[/]")
            for s in payload["NextSteps"]:
                console.print(f"  -> {s}")

        console.print(f"\n[green]Saved -> {path}[/]")
        console.print(f"[dim]Run: psp report {out} --format txt[/]")

    except RateLimitError as e:
        console.print(f"[bold red]Rate limit hit:[/] {e}")
        raise SystemExit(1)
    except AuthError as e:
        console.print(f"[bold red]Auth error:[/] {e}")
        raise SystemExit(1)
    except NotFoundError as e:
        console.print(f"[bold red]Not found:[/] {e}")
        raise SystemExit(1)
    except Exception as e:
        console.print(f"[red]Error:[/] {e}")
        raise SystemExit(1)


@main.command()
@click.argument("audit_file", default="audit.json")
@click.option("--format", "fmt", type=click.Choice(["json", "txt", "md"]), default="txt", show_default=True)
@click.option("--out", default=None, help="Write to file instead of stdout.")
def report(audit_file, fmt, out):
    """Render a report from AUDIT_FILE."""
    try:
        output = render_report(audit_file, fmt)
        if out:
            from pathlib import Path
            Path(out).write_text(output + "\n")
            console.print(f"[green]Report saved -> {out}[/]")
        else:
            console.print(output)
    except Exception as e:
        console.print(f"[red]Error:[/] {e}")
        raise SystemExit(1)


@main.command("rate-limit")
@click.option("--token", default=None, envvar="GITHUB_TOKEN")
def rate_limit(token):
    """Check GitHub API rate limit status."""
    try:
        client = GitHubClient(token=token)
        status = client.rate_limit_status()

        table = Table(title="GitHub Rate Limit")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="white")
        table.add_row("Authenticated", "Yes" if status["authenticated"] else "No (set GITHUB_TOKEN)")
        table.add_row("Limit", str(status["limit"]))
        table.add_row("Remaining", str(status["remaining"]))
        table.add_row("Resets in", f"{status['reset_in']}s")
        console.print(table)

        if not status["authenticated"]:
            console.print("\n[yellow]Tip:[/] Unauthenticated: 60 req/hr. Set GITHUB_TOKEN for 5,000/hr.")
        if status["remaining"] < 10:
            console.print(f"\n[bold red]Warning:[/] Only {status['remaining']} requests left.")
    except Exception as e:
        console.print(f"[red]Error:[/] {e}")
        raise SystemExit(1)
