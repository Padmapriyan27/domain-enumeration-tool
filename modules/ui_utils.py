from typing import Dict, Union
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.color import Color
import pyfiglet

console = Console()

def print_banner() -> None:
    """
    Print a banner with the tool's name and description.
    """
    banner = pyfiglet.figlet_format("0xD4rkEYe", font='slant')
    console.print(banner, style="bold green")
    console.print("[bold green]0xD4rkEYe - Domain Enumeration Tool[/bold green]\n")

def display_table(data: Dict[str, Union[str, Dict, list]], title: str) -> None:
    """
    Display the given data as a formatted table in the console.
    
    Args:
        data (dict): Data to display in table format.
        title (str): Title for the table.
    """
    table = Table(title=title, title_style="bold blue")
    table.add_column("Key", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")

    for key, value in data.items():
        table.add_row(key, str(value))
    console.print(table)
