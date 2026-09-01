import typer
import subprocess
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

app = typer.Typer(help="Lites - The lightning-fast AI proxy CLI")
console = Console()

@app.command()
def up(
    port: int = typer.Option(8000, help="Port to run the proxy on"),
    host: str = typer.Option("127.0.0.1", help="Host to bind the proxy to")
):
    """
    Start the Lites proxy server
    """
    title = Text("Lites AI Proxy", style="bold bright_cyan")
    subtitle = Text(f"\nStarting on http://{host}:{port}/v1\nWaiting for requests...", style="green")
    
    panel = Panel.fit(
        title + subtitle,
        border_style="bright_cyan",
        padding=(1, 4)
    )
    console.print(panel)
    console.print("\n[dim]Press Ctrl+C to stop[/dim]\n")

    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "app.api.server:app",
        "--host",
        host,
        "--port",
        str(port)
    ]
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        console.print("\n[bold red]Shutting down Lites proxy...[/bold red]")
        sys.exit(0)

@app.command()
def version():
    """Print the Lites CLI version"""
    console.print("Lites CLI v0.1.0")

if __name__ == "__main__":
    app()
