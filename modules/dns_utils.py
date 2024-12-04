import logging
from typing import Dict, List, Union
import dns.resolver
import requests

def get_dns_records(domain: str) -> Dict[str, Union[List[str], str]]:
    """
    Get DNS records for the provided domain.
    
    Args:
        domain (str): The domain to get DNS records for.

    Returns:
        dict: A dictionary with record types as keys and their corresponding values.
              Values could be a list of records or an error message.
    """

    record_types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SRV", "PTR"]
    dns_info: Dict[str, Union[List[str], str]] = {}

    for record in record_types:
        try:
            answers = dns.resolver.resolve(domain, record)
            dns_info[record] = [str(rdata) for rdata in answers]
        except dns.resolver.NoAnswer:
            dns_info[record] = "No Record Found."
        except dns.resolver.NXDOMAIN:
            dns_info[record] = "Domain does not exist."
        except dns.resolver.NoNameservers:
            dns_info[record] = "No nameservers found."
        except Exception as e:
            dns_info[record] = f"Error: {str(e)}"
    return dns_info

def check_dnssec(domain: str) -> str:
    """
    Check if DNSSEC is enabled for the domain.
    
    Args:
        domain (str): The domain to check for DNSSEC.

    Returns:
        str: Status message indicating whether DNSSEC is enabled or not.
    """  
    try:
        dnssec_status = dns.resolver.resolve(domain, "DNSKEY")
        return "DNSSEC is enabled." if dnssec_status else "DNSSEC is not enabled."
    except dns.resolver.NoAnswer:
        return "DNSSEC is not enabled."
    except dns.resolver.NXDOMAIN:
        return "Domain does not exist."
    except Exception as e:
        return f"Error checking DNSSEC: {str(e)}"
    
def find_subdomains(domain: str) -> List[str]:
    """
    Enumerate subdomains using online APIs.

    Args:
        domain (str): The given target domain.

    Returns:
        List[str]: A list of discovered subdomains.
    """    
    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return sorted({entry["name_value"] for entry in data})
        return []
    except Exception as e:
        logging.error(f"Error finding subdomains: {e}")
        return [f"Error: {e}"]

   