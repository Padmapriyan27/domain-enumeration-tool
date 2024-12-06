import logging
from typing import Dict, List, Union
import dns.resolver
import requests
import dns.query
import dns.zone

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
        #logging.error(f"Error finding subdomains: {e}")
        return logging.error([f"Error: {e}"])

def get_domain_certificate_info(domain: str) -> List[Dict[str, str]]:
    """
    Fetch detailed certificate information about the domain from crt.sh.

    Args:
        domain (str): The domain to fetch certificate details for.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing certificate details.
    """
    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            certificates = []
            for entry in data:
                cert_info = {
                    "crt.sh ID": entry.get("id"),
                    "Logged At": entry.get("logged_at"),
                    "Not Before": entry.get("not_before"),
                    "Not After": entry.get("not_after"),
                    "Common Name": entry.get("common_name"),
                    "Matching Identities": entry.get("name_value"),
                    "Issuer Name": entry.get("issuer_name"),
                }
                certificates.append(cert_info)
            return certificates
        else:
            #logging.error(f"Failed to fetch certificate details: {response.status_code}")
            return logging.error([{"Error": f"HTTP {response.status_code}"}])
    except Exception as e:
        #logging.error(f"Error fetching certificate details: {e}")
        return logging.error([{"Error": str(e)}])

def test_zone_transfer(domain: str) -> str:
    """
    Test for DNS zone transfer vulnerability.

    Args:
        domain (str): The domain to test.

    Returns:
        str: Zone transfer result.
    """
    try:
        nameservers = dns.resolver.resolve(domain, "NS")
        for ns in nameservers:
            ns_ip = str(ns.target)
            try:
                zone = dns.zone.from_xfr(dns.query.xfr(ns_ip, domain))
                return f"Zone transfer successful with nameserver: {ns_ip}\nZone Data:\n{zone.to_text()}"
            except Exception as e:
                pass
        return "Zone transfer not allowed."
    except Exception as e:
        return f"Error: {e}"

def get_txt_records(domain: str) -> list:
    """
    Retrieve TXT records for the given domain, which may include SPF, DKIM, and DMARC information.

    Args:
        domain (str): The domain to check for TXT records.

    Returns:
        list: TXT records for the domain.
    """
    try:
        # Query the DNS for TXT records
        records = get_dns_records(domain)  # Assuming get_dns_records only fetches A, AAAA, etc.
        txt_records = [record for record in records if 'TXT' in record['type']]
        return txt_records
    except Exception as e:
        return [f"Error fetching TXT records: {e}"]
