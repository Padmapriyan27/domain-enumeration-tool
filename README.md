# 0xD4rkEYe Domain Enumeration Tool

## Beta v.0.4

### Overview

The **Domain Enumeration Tool** is a unix-only  Python-based utility designed to perform an in-depth analysis of a target domain. This tool gathers a variety of information including DNS records, WHOIS data, IP information, geolocation data, SSL certificate details, HTTP headers, Nmap scan results, subdomains, and much more. It is an essential resource for security researchers, penetration testers, and anyone looking to perform a comprehensive analysis of domain OSINT.

### Features

- **DNS Records**: Retrieves multiple DNS record types, such as A, MX, TXT, CNAME, SRV, etc.
- **WHOIS Information**: Fetches detailed WHOIS data for the domain, including registrar and contact information.
- **IP Information**: Resolves the domain to its IP address, conducts reverse DNS lookups, and provides geolocation data.
- **Geolocation**: Identifies the physical location of the domain’s IP address
- **SSL Certificate**: Extracts detailed SSL certificate information for domains with HTTPS, including issuer, validity dates, and more.
- **HTTP Headers**: Retrieves and displays HTTP headers from the domain.
- **Nmap Scan**: Performs an Nmap scan to detect open ports and services associated with the domain.
- **Subdomain Discovery**: Finds subdomains using domain-based queries and certificate transparency logs.
- **Directory & File Enumeration**: Performs directory and file enumeration to find hidden directories and files associated with the domain.
- **Zone Transfer Test**: Verifies if a DNS zone transfer is allowed.
- **DNSSEC Check**: Checks the status of DNSSEC for the domain.
- **Robots.txt Scraping**: Fetches the robots.txt file to determine any rules regarding search engine crawling.

---

## Requirements

- Python 3.8 or higher
- External Python Libraries:
  - `requests`
  - `dnspython`
  - `rich`
  - `pyfiglet`
  - `beautifulsoup4`

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

To use the tool, simply run the script with the domain as the argument:

```bash
python 0xD4rkEYe.py example.com
```

### Example Output

The tool will gather and display detailed information about the domain:

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

- Directory & File Enumeration:
  - /hidden-directory
  - /secret-file.txt

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

- DNSSEC Status:
  - Enabled
```

---

## Modules

### 1. **`0xD4rkEYe.py`**
The main script that orchestrates all domain enumeration tasks.

### 2. **`modules/dns_utils.py`**
- Querying DNS records (A, MX, TXT, etc.)
- Checking DNSSEC status
- Finding subdomains
- Performing zone transfers

### 3. **`modules/ip_utils.py`**
- Resolve domains to IP addresses
- Get IP geolocation information
- Perform reverse DNS lookups

### 4. **`modules/network_utils.py`**
- Perform WHOIS lookups
- Retrieve HTTP headers
- Extract SSL certificate details
- Run Nmap scans
- Check domain response time
- Scrape robots.txt
- Identify HTTP methods

### 5. **`modules/dir_utils.py`**
- enumerate directories and files

### 6. **`modules/ui_utils.py`**
Formats and displays results to the console using the `rich` library for enhanced visuals, such as colorful panels and tables.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---