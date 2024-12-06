from typing import Dict, Optional
from bs4 import BeautifulSoup
import socket
import requests

def get_ip_info(domain: str) -> Optional[str]:
    """
    Get the IP address for the provided domain.
    
    Args:
        domain (str): The domain to resolve to an IP address.

    Returns:
        str|None: The resolved IP address or None if unable to resolve.
    """
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None
    
def get_ip_geolocation(ip: str) -> Dict[str, str]:    
    """
    Get geolocation information for a given IP address.
    
    Args:
        ip (str): The IP address to retrieve geolocation data for.

    Returns:
        dict: A dictionary containing geolocation details such as city, region, and country.
    """
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
        return response.json()
    except requests.RequestException:
        return {"Error": "Unable to retrieve geolocation"}
    
def reverse_dns_lookup(ip: str) -> str:
    """
    Perform a reverse DNS lookup to find the associated domain for an IP address.
    
    Args:
        ip (str): The IP address to perform reverse lookup on.

    Returns:
        str: The domain associated with the IP, or a message if lookup fails.
    """
    try:
        host = socket.gethostbyaddr(ip)
        return host[0]
    except socket.herror:
        return "No reverse DNS record found"   

def scrape_reverse_ip(ip: str) -> list:
    """
    Perform a reverse IP lookup by scraping data from viewdns.info.

    Args:
        ip (str): The IP address to check.

    Returns:
        list: Domains hosted on the same IP.
    """
    try:
        url = f'https://viewdns.info/reverseip/?host={ip}'
        response = requests.get(url)
        response.raise_for_status()  # Ensure we get a valid response
        
        soup = BeautifulSoup(response.text, 'html.parser')
        domains = soup.find_all('td', {'class': 'list'})
        return [domain.text for domain in domains]
    except Exception as e:
        return [f"Error: {e}"]

