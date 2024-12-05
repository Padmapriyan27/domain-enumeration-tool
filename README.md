# 0xD4rkEYe Domain Enumeration Tool

## Beta v0.2

### Overview

The **Domain Enumeration Tool** is a Unix-only, Python-based tool designed for comprehensive domain analysis. It gathers extensive information about a target domain, including DNS records, WHOIS data, IP information, SSL certificate details, HTTP headers, Nmap scan results, subdomains, and certificate transparency logs (via crt.sh).

### Features

- **DNS Records**: Retrieves various DNS records, including A, MX, TXT, CNAME, SRV, and more.
- **WHOIS Information**: Fetches detailed WHOIS data for the domain.
- **IP Information**: Resolves the domain's IP address, performs reverse DNS lookups, and retrieves IP geolocation data.
- **Geolocation**: Provides the physical location of the domain's IP address.
- **SSL Certificate**: Extracts SSL certificate details for domains with HTTPS.
- **HTTP Headers**: Retrieves HTTP headers for the domain.
- **Nmap Scan**: Identifies open ports and services running on the domain.
- **Subdomain Discovery**: Uses crt.sh to find and list subdomains.
- **Certificate Transparency Logs**: Fetches detailed certificate information, including crt.sh ID, validity dates, and issuers.

---

## Requirements

- Python 3.8 or higher
- External Python Libraries:
  - `requests`
  - `dnspython`
  - `rich`
  - `pyfiglet`

Install the required libraries by running:

```bash
pip install -r requirements.txt
```

---

## Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/Padmapriyan27/domain-enumeration-tool
```

2. Navigate to the project directory:

```bash
cd domain-enumeration-tool
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

### Running the Tool

To use the tool, run the script with a domain as the argument:

```bash
python 0xD4rkEYe.py example.com
```

### Example Output

When executed, the tool gathers and displays detailed information about the domain:

```bash
Domain: example.com

- WHOIS Information:
  [WHOIS data]

- DNS Records:
  - A Record: 93.184.216.34
  - MX Record: mail.example.com

- Subdomains:
  - sub1.example.com
  - sub2.example.com

- Certificate Transparency Logs:
  - crt.sh ID: 123456789
    Logged At: 2024-12-01
    Not Before: 2024-01-01
    Not After: 2025-01-01
    Common Name: example.com
    Issuer Name: CN=Let's Encrypt Authority X3

- HTTP Headers:
  - Content-Type: text/html
  - Server: Apache

- SSL Certificate Info:
  - Subject: CN=example.com
  - Issuer: CN=Let's Encrypt Authority X3
  - Valid From: 2024-01-01
  - Valid To: 2025-01-01

- Nmap Results:
  - Ports: 80, 443
  - Services: HTTP, HTTPS
```

---

## Modules

### 1. **`0xD4rkEYe.py`**
The main script that orchestrates all domain enumeration tasks.

### 2. **`modules/dns_utils.py`**
Contains functions for querying DNS records, checking DNSSEC status, finding subdomains, and retrieving certificate transparency logs via crt.sh.

### 3. **`modules/ip_utils.py`**
Provides functions to resolve domains to IPs, get IP geolocation, and perform reverse DNS lookups.

### 4. **`modules/network_utils.py`**
Includes WHOIS lookups, HTTP header retrieval, SSL certificate information fetching, and Nmap scans.

### 5. **`modules/ui_utils.py`**
Formats and displays results to the console using the `rich` library for enhanced visuals.

---

## Updates in Beta v0.2

- Added **Certificate Transparency Logs** retrieval using crt.sh to fetch domain certificates, including issuer details and validity periods.
- Improved error handling and logging for all modules.
- Enhanced subdomain discovery with crt.sh results.
- Minor UI improvements for better readability.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---