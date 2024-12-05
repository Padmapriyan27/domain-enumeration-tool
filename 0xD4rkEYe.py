from modules.dns_utils import get_dns_records, check_dnssec, find_subdomains, get_domain_certificate_info
from modules.ip_utils import get_ip_info, get_ip_geolocation, reverse_dns_lookup
from modules.network_utils import get_whois_info, get_http_headers, get_ssl_certificate_info, run_nmap
from modules.ui_utils import print_banner, display_table
from argparse import ArgumentParser
from rich.console import Console
from rich.panel import Panel
import logging

# Setup logging for better error tracking
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

console = Console()

def main() -> None:
    """
    Main function to run the domain enumeration tool.
    
    Gathers various information about the domain, such as WHOIS data, DNS records, 
    IP geolocation, and SSL certificate details, and displays the results in a user-friendly format.
    """
    print_banner()

    parser = ArgumentParser(description="Domain Enumeration Tool")
    parser.add_argument("domain", help="Domain to enumerate information about")
    args = parser.parse_args()
    domain: str = args.domain

    # Get and display IP information
    ip_info = get_ip_info(domain)
    if ip_info:
        console.print(Panel(f"IP Address: {ip_info}", style="bold green"))
        geo_info = get_ip_geolocation(ip_info)
        display_table(geo_info, "IP Geolocation")
        reverse_dns = reverse_dns_lookup(ip_info)
        console.print(Panel(f"Reverse DNS: {reverse_dns}", style="bold cyan"))
    else:
        console.print(Panel("Could not resolve IP address.", style="bold red"))

    # Get and display WHOIS information
    whois_info = get_whois_info(domain)
    console.print(Panel(whois_info, title="WHOIS Information", expand=True, border_style="green"))

    # Get and display DNS records
    dns_info = get_dns_records(domain)
    display_table(dns_info, "DNS Records")

    # Check and display DNSSEC status
    dnssec_status = check_dnssec(domain)
    console.print(Panel(f"DNSSEC Status: {dnssec_status}", style="bold green"))

    # Find and display subdomains
    subdomains = find_subdomains(domain)
    console.print(Panel(f"Subdomains found: {', '.join(subdomains) if subdomains else 'No subdomains found.'}", style="bold green"))

    # Fetch and display detailed certificate information
    cert_info = get_domain_certificate_info(domain)
    if cert_info:
        for cert in cert_info:
            display_table(cert, "Certificate Information")
    else:
        console.print(Panel("No certificate information found.", style="bold red"))

    # Get and display HTTP headers
    http_headers = get_http_headers(domain)
    display_table(http_headers, "HTTP Headers")

    # Get and display SSL certificate information
    ssl_info = get_ssl_certificate_info(domain)
    display_table(ssl_info, "SSL Certificate Info")

    # Run and display Nmap scan results
    nmap_results = run_nmap(domain)
    console.print(Panel(nmap_results, title="Nmap Scan", expand=True))

if __name__ == "__main__":
    main()
