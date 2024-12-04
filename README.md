# 0xD4rkEYe Domain Enumeration Tool

## Beta v0.1

## Overview

The **Domain Enumeration Tool** is a comprehensive unix only Python-based tool designed for gathering a wide range of information about a domain. It retrieves details such as DNS records, WHOIS data, IP information, SSL certificate details, HTTP headers, Nmap scan results, and more.

### Features:
- **DNS Records**: Retrieves various DNS records including A, MX, TXT, CNAME, etc.
- **WHOIS Information**: Fetches WHOIS data for the domain.
- **IP Information**: Resolves the IP address for the domain and performs reverse DNS lookup.
- **Geolocation**: Fetches the geographical location of the domain's IP address.
- **SSL Certificate**: Retrieves SSL certificate details for secure HTTPS communication.
- **HTTP Headers**: Retrieves HTTP headers for the domain.
- **Nmap Scan**: Performs an Nmap scan to identify open ports and services running on the domain.
- **Subdomain Discovery**: Finds subdomains using the crt.sh API.

---

## Requirements

- Python 3.8 or higher
- External Python Libraries:
  - `requests`
  - `dnspython`
  - `rich`
  - `pyfiglet`

You can install the required libraries by running:

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

To use the tool, simply run the script with a domain as the argument:

```bash
    python 0xD4rkEYe.py example.com
```

### Example Output

When you run the tool, it will gather and display information about the domain in a structured format:

```bash
Domain: example.com
- WHOIS Information: [WHOIS data]
- DNS Records:
  - A Record: 93.184.216.34
  - MX Record: mail.example.com
- Subdomains:
  - sub1.example.com
  - sub2.example.com
- HTTP Headers:
  - Content-Type: text/html
  - Server: Apache
- SSL Certificate Info:
  - Subject: CN=example.com
  - Issuer: CN=Let's Encrypt
  - Valid From: 2023-01-01
  - Valid To: 2024-01-01
- Nmap Results:
  - Ports: 80, 443
  - Services: HTTP, HTTPS
```

---

## Modules

### 1. **`0xD4rkEYe.py`**  
The main script that ties all the functions together and runs the domain enumeration process.

### 2. **`modules/dns_utils.py`**  
Contains functions for querying DNS records, checking DNSSEC status, and finding subdomains.

### 3. **`modules/ip_utils.py`**  
Provides functions to resolve domain to IP, get IP geolocation, and perform reverse DNS lookup.

### 4. **`modules/network_utils.py`**  
Contains functions for WHOIS lookups, getting HTTP headers, retrieving SSL certificate info, and performing Nmap scans.

### 5. **`modules/ui_utils.py`**  
Functions for displaying results to the console using the `rich` library to create beautiful and formatted output.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

