ScanHammer
 
ScanHammer is a powerful, Python-driven cybersecurity tool inspired by Nmap and Hulk, designed for educational purposes to perform network reconnaissance and simulate Denial of Service (DoS) attacks. It combines intuitive menu-driven options with robust Bash scripts to deliver detailed network scanning and attack simulation capabilities, making it an essential tool for security researchers, penetration testers, and students learning ethical hacking.

🚀 Why ScanHammer?
In today’s cybersecurity landscape, understanding network vulnerabilities and attack vectors is critical. ScanHammer empowers users to:

Discover Network Assets: Identify active devices, services, and open ports with Nmap-inspired scanning, including TCP/IP fingerprinting for vulnerability assessment.
Simulate Real-World Attacks: Test system resilience with Hulk-inspired DoS attacks (HTTP Flood and Slowloris), providing insights into attack impact and mitigation.
Learn Securely: Designed for educational environments, ScanHammer emphasizes ethical use with clear disclaimers and controlled testing scenarios.
Showcase Skills: A portfolio-ready project demonstrating proficiency in Python, Bash, networking, and security testing, perfect for recruiters and GitHub visibility.


Disclaimer: ScanHammer is for EDUCATIONAL PURPOSES ONLY. Unauthorized use of network scanning or DoS tools against systems without explicit permission is ILLEGAL and UNETHICAL. Use responsibly on systems you own or have permission to test.

📸 Showcase: Real-Time Testing
To demonstrate ScanHammer’s power, we’re seeking screenshots or videos of the tool in action! Have you tested ScanHammer on a local network or lab environment? Share your:

Network scanning results (e.g., active hosts, open ports).
DoS attack simulations (e.g., HTTP Flood or Slowloris output, “Successfully Down” message).
CLI interface with menu options.

Example Screenshots :

![Screenshot_2025-05-18_02_43_43](https://github.com/user-attachments/assets/1b37fb48-2863-41f7-b9ef-2b81a6c00a80)

![Screenshot_2025-05-18_02_44_45](https://github.com/user-attachments/assets/23436952-144b-4149-bd9a-e444f104037f)


![Screenshot_2025-05-18_02_52_55](https://github.com/user-attachments/assets/10330ac8-50ae-40a0-b1ef-ab1f099d56ad)

🛠️ Features
Network Scanning (Inspired by Nmap)

Host Discovery: Identifies active devices on a network.
Port Scanning: Detects open ports and services.
TCP/IP Fingerprinting: Analyzes OS and service versions for vulnerability assessment.
Detailed Reporting: Provides clear, actionable output for network analysis.

DoS Attack Simulation (Inspired by Hulk)

HTTP Flood: Overwhelms websites with high-volume requests to simulate bandwidth exhaustion.
Slowloris Attack: Exhausts server sockets with slow connections, mimicking real-world DoS scenarios.
Interactive Feedback: Displays real-time attack progress and “Successfully Down” notifications.
Ethical Design: Includes duration limits and disclaimers to ensure safe testing.

User Experience

Python CLI: Intuitive menu with options (1: Network Scanning, 2: DoS Attack, 3: Exit).
Bash Efficiency: Leverages Bash scripts for high-performance scanning and attacks.
Colored Output: Enhances readability with colorama and ASCII art via art.

📋 Prerequisites

Operating System: Kali Linux (recommended for native nmap, curl, and apache2-utils support).
Python: Version 3.8 or higher.
System Tools:
nmap (for network scanning).
apache2-utils (provides ab for HTTP Flood).
curl (for Slowloris and downtime checks).


Permissions: sudo required for network scanning (NetScanner.sh); DoS attacks (humangous.sh) run without sudo.

🛠️ Installation

Follow these steps to set up ScanHammer on Kali Linux:





Clone the Repository:
#bash
git clone https://github.com/Ajay-Bommidi/ScanHammer.git
cd ScanHammer



Install System Dependencies:

sudo apt update
sudo apt install nmap apache2-utils curl



Set Up Python Virtual Environment:

python3 -m venv venv
source venv/bin/activate



Install Python Dependencies:

pip install -r requirements.txt

Contents of requirements.txt:

colorama==0.4.6
art==6.2



Verify Scripts: Ensure main.py, NETWORK-SCANNER/NetScanner.sh, and DOS-TOOL/humangous.sh are executable:

chmod +x NETWORK-SCANNER/NetScanner.sh DOS-TOOL/humangous.sh

🚀 Usage

Run ScanHammer via the Python CLI interface:

source venv/bin/activate
python3 main.py

Menu Options





Network Scanning:





Runs NETWORK-SCANNER/NetScanner.sh (requires sudo).



Prompts for a target IP or range (e.g., 192.168.1.0/24).



Outputs active hosts, open ports, and service details.



Command (if run separately):

sudo ./NETWORK-SCANNER/NetScanner.sh



DoS Attack:





Runs DOS-TOOL/humangous.sh (no sudo needed).



Prompts for target URL (e.g., http://localhost), attack duration, and type (HTTP Flood or Slowloris).



Displays real-time attack progress and “Successfully Down” if the target becomes unresponsive.



Command (if run separately):

./DOS-TOOL/humangous.sh



Exit:





Closes the CLI.

Example Commands





Network Scanning:

sudo ./NETWORK-SCANNER/NetScanner.sh
Enter target IP or range: 192.168.1.0/24

Output: List of active hosts, ports, and services.



DoS Attack (HTTP Flood):

./DOS-TOOL/humangous.sh
Enter target URL: http://localhost
Enter attack duration: 60
Select attack type: 1

Output: Attack progress, “Successfully Down” if target fails.

🧪 Testing Environment

For safe and ethical testing:





Set Up a Local Server:

sudo apt install apache2
sudo systemctl start apache2

Test DoS attacks against http://localhost.



Use a Virtual Machine:





Run ScanHammer in a Kali Linux VM to isolate network scanning and attacks.



Example: Use VirtualBox with a local network for scanning.



Capture Screenshots:





Take screenshots of:





CLI menu (main.py).



Network scanning output (e.g., nmap results).



DoS attack progress and “Successfully Down” message.



Upload to a GitHub issue or include in a pull request to enhance this README.

🔒 Ethical Considerations

ScanHammer is designed for educational purposes and authorized testing only. Key safeguards:





Disclaimers: Prominent warnings in the CLI and scripts.



Controlled Attacks: Duration limits prevent prolonged impact.



Permission Checks: Prompts for user confirmation before attacks.

Legal Warning: Unauthorized scanning or attacking systems is illegal under laws like the Computer Fraud and Abuse Act (CFAA) in the US or equivalent regulations worldwide. Always obtain explicit permission from system owners.

📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

📬 Contact





Author: Ajay Bommidi



GitHub: Ajay-Bommidi



Email: ajaynaidu641@gmail.com



⭐ Star this repository if you find ScanHammer useful! Your support helps showcase this project to recruiters and the cybersecurity community.
