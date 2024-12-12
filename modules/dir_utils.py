import requests
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich.progress import Progress

console = Console()

def enumerate_directories_files(domain: str, wordlist_path: str, threads: int = 20) -> list:
    """
    Enumerates directories and files on the given domain using a wordlist.
    This version includes a progress bar for better visualization.
    
    Args:
        domain (str): The target domain or base URL.
        wordlist_path (str): Path to the wordlist file containing potential directories/files.
        threads (int): Number of threads for concurrent requests.

    Returns:
        list: A list of found directories/files.
    """
    found = []

    # Ensure the URL has the correct format
    if not domain.startswith("http://") and not domain.startswith("https://"):
        domain = f"http://{domain}"
    if not domain.endswith("/"):
        domain += "/"

    try:
        with open(wordlist_path, "r") as f:
            paths = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        console.print(f"[bold red]Error: Wordlist file not found: {wordlist_path}[/bold red]")
        return []

    def test_path(path: str, progress: Progress, task_id: str) -> None:
        url = f"{domain}{path}"
        try:
            response = requests.head(url, timeout=5)
            if response.status_code == 200:
                console.print(f"[bold green]Found: {url}[/bold green]")
                found.append(url)
            elif response.status_code == 403:
                console.print(f"[bold yellow]Forbidden: {url}[/bold yellow]")
                found.append(f"{url} [Forbidden]")
        except requests.RequestException:
            pass
        finally:
            progress.update(task_id, advance=1)

    console.print("[bold blue]Starting enumeration with progress...[/bold blue]")

    # Initialize Progress bar
    with Progress() as progress:
        task_id = progress.add_task("[cyan]Enumerating directories and files...", total=len(paths))
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for path in paths:
                executor.submit(test_path, path, progress, task_id)

    console.print("[bold green]Enumeration complete![/bold green]")
    return found
