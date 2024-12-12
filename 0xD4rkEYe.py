from modules.dns_utils import *
from modules.ip_utils import *
from modules.network_utils import *
from modules.dir_utils import *
from modules.ui_utils import print_banner, display_table
from argparse import ArgumentParser
from rich.console import Console
from rich.panel import Panel

console = Console()

def main() -> None:

    print_banner()

    parser = ArgumentParser(description="Domain Enumeration Tool")
    parser.add_argument("domain", help="Domain to enumerate information about")
    args = parser.parse_args()
    domain: str = args.domain

    response_time = check_response_time(domain)
    console.print(Panel(f"Response Time: {response_time} seconds", style="bold yellow"))

    ip_info = get_ip_info(domain)
    if ip_info:
        console.print(Panel(f"IP Address: {ip_info}", style="bold green"))
        geo_info = get_ip_geolocation(ip_info)
        display_table(geo_info, "IP Geolocation")
        reverse_dns = reverse_dns_lookup(ip_info)
        console.print(Panel(f"Reverse DNS: {reverse_dns}", style="bold cyan"))
    else:
        console.print(Panel("Could not resolve IP address.", style="bold red"))

    whois_info = get_whois_info(domain)
    console.print(Panel(whois_info, title="WHOIS Information", expand=True, border_style="green"))

    dns_info = get_dns_records(domain)
    display_table(dns_info, "DNS Records")

    zone_transfer = test_zone_transfer(domain)
    console.print(Panel(f"Zone Transfer Test:\n{zone_transfer}", style="bold red"))

    dnssec_status = check_dnssec(domain)
    console.print(Panel(f"DNSSEC Status: {dnssec_status}", style="bold green"))

    http_methods = get_http_methods(domain)
    console.print(Panel(f"Supported HTTP Methods: {', '.join(http_methods)}", style="bold yellow"))

    robots_txt = scrape_robots_txt(domain)
    console.print(Panel(f"Robots.txt Content:\n{robots_txt}", style="bold magenta"))

    reverse_domains = scrape_reverse_ip(ip_info)
    console.print(Panel(f"Domains hosted on same IP:\n{', '.join(reverse_domains)}", style="bold cyan"))

    subdomains = find_subdomains(domain)
    console.print(Panel(f"Subdomains found: {', '.join(subdomains) if subdomains else 'No subdomains found.'}", style="bold green"))

    wordlist_path = "/usr/share/wordlists/dirb/common.txt"
    console.print("[bold blue]Enumerating directories and files...[/bold blue]")
    directories = enumerate_directories_files(domain, wordlist_path)
    if directories:
        console.print(Panel("\n".join(directories), title="Directories and Files Found", border_style="green"))
    else:
        console.print(Panel("No directories or files found.", style="bold red"))

    cert_info = get_domain_certificate_info(domain)
    if cert_info:
        for cert in cert_info:
            display_table(cert, "Certificate Information")
    else:
        console.print(Panel("No certificate information found.", style="bold red"))

    http_headers = get_http_headers(domain)
    display_table(http_headers, "HTTP Headers")

    ssl_info = get_ssl_certificate_info(domain)
    display_table(ssl_info, "SSL Certificate Info")

    nmap_results = run_nmap(domain)
    console.print(Panel(nmap_results, title="Nmap Scan", expand=True))

if __name__ == "__main__":
    main()
