import nmap
import sys
import os

# ASCII art for "CYBER SPECTER"
ascii_art = """

   _____      _                  _____                 _             
  / ____|    | |                / ____|               | |            
 | |    _   _| |__   ___ _ __  | (___  _ __   ___  ___| |_ ___  _ __ 
 | |   | | | | '_ \ / _ \ '__|  \___ \| '_ \ / _ \/ __| __/ _ \| '__|
 | |___| |_| | |_) |  __/ |     ____) | |_) |  __/ (__| || (_) | |   
  \_____\__, |_.__/ \___|_|    |_____/| .__/ \___|\___|\__\___/|_|   
         __/ |                        | |                            
        |___/                         |_|                            

"""

def check_root():
    if os.geteuid() != 0:
        print("Error: This script requires root privileges to perform OS detection.")
        print("Please run the script with elevated permissions (e.g., using 'sudo').")
        sys.exit()

def scan_network(ip_range, port_range, scan_type):
    nm = nmap.PortScanner()
    print(f"Scanning {ip_range} on ports {port_range} with {scan_type} scan...")
    try:
        nm.scan(ip_range, port_range, arguments=scan_type)
    except nmap.PortScannerError as e:
        print(f"Error: {e}")
        sys.exit()
    
    result = []
    for host in nm.all_hosts():
        host_info = {
            'Host': host,
            'Hostname': nm[host].hostname(),
            'State': nm[host].state(),
            'OS': nm[host]['osmatch'][0]['name'] if 'osmatch' in nm[host] and nm[host]['osmatch'] else 'Unknown',
            'Protocols': {}
        }
        for proto in nm[host].all_protocols():
            ports = nm[host][proto].keys()
            host_info['Protocols'][proto] = {
                port: {
                    'state': nm[host][proto][port]['state'],
                    'name': nm[host][proto][port]['name'],
                    'version': nm[host][proto][port]['version'],
                } for port in ports
            }
        result.append(host_info)
    return result

def verbose_output(scan_results):
    for host in scan_results:
        print(f"Host: {host['Host']} ({host['Hostname']})")
        print(f"State: {host['State']}")
        print(f"OS: {host['OS']}")
        for proto, ports in host['Protocols'].items():
            print(f"Protocol: {proto}")
            for port, info in ports.items():
                print(f"Port: {port}\tState: {info['state']}\tService: {info['name']}\tVersion: {info['version']}")
        print("-" * 50)

def main():
    print(ascii_art)
    print("Welcome to Cyber Network scanner!")
    
    check_root()
    
    ip_range = input("Enter the IP range to scan (e.g., 192.168.1.0/24): ")
    print("Select the port range to scan:")
    print("1. First 1000 ports")
    print("2. All ports")
    print("3. Specific ports")

    choice = input("Enter your choice (1/2/3): ")
    if choice == '1':
        port_range = '1-1000'
    elif choice == '2':
        port_range = '1-65535'
    elif choice == '3':
        port_range = input("Enter the specific ports (comma-separated, e.g., 22,80,443): ")
    else:
        print("Invalid choice! Exiting.")
        sys.exit()

    print("Select the type of scan:")
    print("1. SYN Scan")
    print("2. ACK Scan")
    print("3. UDP Scan")
    print("4. Service Version Detection")

    scan_choice = input("Enter your choice (1/2/3/4): ")
    if scan_choice == '1':
        scan_type = '-sS'
    elif scan_choice == '2':
        scan_type = '-sA'
    elif scan_choice == '3':
        scan_type = '-sU'
    elif scan_choice == '4':
        scan_type = '-sV'
    else:
        print("Invalid choice! Exiting.")
        sys.exit()

    if input("Do you want to enable OS detection? (y/n): ").lower() == 'y':
        scan_type += ' -O'

    scan_results = scan_network(ip_range, port_range, scan_type)
    verbose_output(scan_results)

if __name__ == "__main__":
    main()

