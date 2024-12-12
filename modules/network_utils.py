from typing import Dict
import subprocess
import requests
import socket
import ssl
import time
import re

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

def check_response_time(domain: str) -> float:
    """
    Measure the response time of the given domain.

    Args:
        domain (str): The domain to test.

    Returns:
        float: Response time in seconds.
    """
    try:
        start_time = time.time()
        response = requests.get(f"http://{domain}", timeout=5)
        response.raise_for_status()
        return round(time.time() - start_time, 3)
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def get_http_methods(domain: str) -> list:
    """
    Perform HTTP methods enumeration by sending a request with various methods.
    
    Args:
        domain (str): The domain to test for HTTP methods.

    Returns:
        list: Supported HTTP methods.
    """
    methods = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH']
    supported_methods = []
    urls = [f"http://{domain}", f"https://{domain}"]  # Check both HTTP and HTTPS
    
    for url in urls:
        for method in methods:
            try:
                response = requests.request(method, url, timeout=5)  
                if response.status_code not in [405, 501, 400]:
                    supported_methods.append(method)
            except requests.exceptions.RequestException as e:
                # Log the error for visibility
                #print(f"Error testing {method} on {url}: {e}")
                continue

    # Remove duplicates (in case both http and https return the same methods)
    return list(set(supported_methods))

def scrape_robots_txt(domain: str) -> str:
    """
    Scrape the robots.txt file for a domain to find information about restricted paths.

    Args:
        domain (str): The domain to scrape.

    Returns:
        str: The content of the robots.txt file.
    """
    try:
        response = requests.get(f"http://{domain}/robots.txt")
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error fetching robots.txt: {e}"
