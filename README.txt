NetScanner is a networkscanning tool
humangous is a Dos(Denial of service) tool

[note: run with sudo perminssions]
---

# README

## Overview

This project contains two educational tools designed for network security research and ethical hacking purposes: a DoS attacking tool and a network scanner.

### Disclaimer
These tools are intended solely for educational and research purposes. Misuse of these tools may result in legal consequences. Always ensure you have explicit permission to test and scan any network or system.

## Tools

### 1. DoS Attack Tool

**Name:** humangous

**Description:**
This tool is designed to simulate Denial of Service (DoS) attacks. It helps users understand the mechanics of DoS attacks and the potential impacts on network infrastructure.

**Features:**
- Interactive interface
- Detailed output reporting
- Number of requests sent
- Automatic updates
- User suggestions on attack impact

**Usage:**
```
python humangous.py [target_url] [options]
```

**Options:**
- `--help` : Show usage information
- `--verbose` : Enable detailed logging
- `--requests` : Number of requests to send (default: 1000)
- `--timeout` : Timeout for each request in seconds (default: 5)

### 2. Network Scanner

**Name:** NetScanner

**Description:**
This tool is designed to scan networks and identify active devices and services. It provides insights into network configurations and potential vulnerabilities.

**Features:**
- TCP/IP fingerprinting (OS scan)
- Port scanning
- Detailed output
- Reporting and logging capabilities

**Usage:**
```
python NetScanner.py [options]
```

**Options:**
- `--help` : Show usage information
- `--target` : Specify target IP address or range
- `--ports` : Specify ports to scan (default: 1-1024)
- `--os-scan` : Enable OS fingerprinting (requires root privileges)

## Installation

1. Clone this repository:
```
git clone https://github.com/[YourGitHubUsername]/[YourRepositoryName].git
```
2. Navigate to the project directory:
```
cd [YourRepositoryName]
```
3. Install required dependencies:
```
pip install -r requirements.txt
```

## Important Notes

- Ensure you run these tools in an environment where you have explicit permission.
- For the network scanner, root privileges are required for TCP/IP fingerprinting.
- Always comply with local laws and regulations when using these tools.

## Contributions

Contributions are welcome! Please fork this repository and submit a pull request for any improvements or new features.

## License

This project is licensed under the CYBER-SPECTOR License - see the LICENSE file for details.

---

Feel free to adjust the template as needed. Once you have filled in the specific details, you can upload this `README.txt` to your GitHub repository.


