from typing import Dict
import subprocess
import requests
import socket
import ssl

def get_whois_info(domain: str) -> str:
    """
    Retrieve WHOIS information for the provided domain.
    
    Args:
        domain (str): The domain to fetch WHOIS data for.

    Returns:
        str: WHOIS data for the domain or an error message.
    """
    try:
        result = subprocess.run(
            ["whois", domain],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

def get_http_headers(domain: str) -> Dict[str, str]:
    """
    Retrieve HTTP headers for the domain.
    
    Args:
        domain (str): The domain to get HTTP headers for.

    Returns:
        dict: HTTP headers or an error message.
    """
    try:
        response = requests.get(f"http://{domain}", timeout=5)
        return dict(response.headers)
    except requests.RequestException:
        return {"Error": "Unable to fetch headers"}

def get_ssl_certificate_info(domain: str) -> Dict[str, str]:
    """
    Retrieve SSL certificate information for the provided domain.
    
    Args:
        domain (str): The domain to retrieve SSL certificate data for.

    Returns:
        dict: SSL certificate details such as issuer and validity dates.
    """
    port = 443
    context = ssl.create_default_context()
    try:
        with socket.create_connection((domain, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                return {
                    "subject": dict(x[0] for x in cert["subject"]),
                    "issuer": dict(x[0] for x in cert["issuer"]),
                    "valid_from": cert["notBefore"],
                    "valid_to": cert["notAfter"],
                }
    except (ssl.SSLError, socket.error, requests.RequestException) as e:
        return {"Error": f"Unable to fetch certificate: {str(e)}"}

def run_nmap(domain: str) -> str:
    """
    Run an Nmap scan against the given domain to find open ports and services.
    
    Args:
        domain (str): The domain to scan.

    Returns:
        str: The output from the Nmap scan.
    """
    try:
        result = subprocess.run(["nmap", "-sV", "-A", domain], stdout=subprocess.PIPE, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"
