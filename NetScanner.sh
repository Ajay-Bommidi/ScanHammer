#!/bin/bash

# Colors for output
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
WHITE='\033[1;37m'
NC='\033[0m'

check_nmap() {
    if ! command -v nmap >/dev/null 2>&1; then
        echo -e "${RED}Error: nmap not found. Install it with 'sudo apt install nmap'.${NC}"
        exit 1
    fi
}

check_root() {
    if [ "$EUID" -ne 0 ]; then
        echo -e "${RED}Error: This script requires root privileges for scanning.${NC}"
        echo -e "${RED}Run with 'sudo' (e.g., 'sudo bash NetScanner.sh').${NC}"
        exit 1
    fi
}

validate_ip_range() {
    local ip_range="$1"
    if ! [[ $ip_range =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}(/[0-9]{1,2})?$ ]]; then
        echo -e "${RED}Error: Invalid IP range format (e.g., 192.168.1.0/24).${NC}"
        exit 1
    fi
    echo "$ip_range"
}

validate_port_range() {
    local port_range="$1"
    if ! [[ $port_range =~ ^([0-9]+-[0-9]+|[0-9]+(,[0-9]+)*)$ ]]; then
        echo -e "${RED}Error: Invalid port range format (e.g., 1-1000 or 22,80,443).${NC}"
        exit 1
    fi
    echo "$port_range"
}

scan_network() {
    local ip_range="$1"
    local port_range="$2"
    local scan_type="$3"
    echo -e "${CYAN}Scanning $ip_range on ports $port_range with $scan_type scan...${NC}"
    nmap $scan_type -p "$port_range" "$ip_range" -oG - | awk '
        /^Host:/ {
            host=$2; state=$4; hostname=$5; os=""
        }
        /OS:/ {
            os=$0; sub(/^OS:/, "", os)
        }
        /Ports:/ {
            print "'${GREEN}'Host: " host " (" hostname ")'${NC}'"
            print "'${GREEN}'State: " state "'${NC}'"
            print "'${GREEN}'OS: " (os ? os : "Unknown") "'${NC}'"
            ports=$0; sub(/^Ports:/, "", ports)
            split(ports, port_array, ", ")
            for (i in port_array) {
                if (port_array[i] ~ /^[0-9]+/) {
                    split(port_array[i], fields, "/")
                    port=fields[1]; state=fields[2]; proto=fields[3]; service=fields[5]
                    print "'${WHITE}'Port: " port "\tState: " state "\tService: " service "\tProtocol: " proto "'${NC}'"
                }
            }
            print "'${YELLOW}'----------------------------------------'${NC}'"
        }'
}

main() {
    check_nmap
    check_root
    
    echo -e "${CYAN}Welcome to Cyber Network Scanner!${NC}"
    
    read -p "$(echo -e ${YELLOW}Enter the IP range to scan \(e.g., 192.168.1.0/24\): ${NC})" ip_range
    ip_range=$(validate_ip_range "$ip_range")
    
    echo -e "${YELLOW}Select the port range to scan:${NC}"
    echo -e "${WHITE}1. First 1000 ports${NC}"
    echo -e "${WHITE}2. All ports${NC}"
    echo -e "${WHITE}3. Specific ports${NC}"
    read -p "$(echo -e ${YELLOW}Enter your choice \(1/2/3\): ${NC})" choice
    
    case "$choice" in
        1) port_range="1-1000" ;;
        2) port_range="1-65535" ;;
        3) read -p "$(echo -e ${YELLOW}Enter specific ports \(comma-separated, e.g., 22,80,443\): ${NC})" port_range
           port_range=$(validate_port_range "$port_range") ;;
        *) echo -e "${RED}Invalid choice! Exiting.${NC}"; exit 1 ;;
    esac
    
    echo -e "${YELLOW}Select the type of scan:${NC}"
    echo -e "${WHITE}1. SYN Scan (-sS)${NC}"
    echo -e "${WHITE}2. ACK Scan (-sA)${NC}"
    echo -e "${WHITE}3. UDP Scan (-sU)${NC}"
    echo -e "${WHITE}4. Service Version Detection (-sV)${NC}"
    read -p "$(echo -e ${YELLOW}Enter your choice \(1/2/3/4\): ${NC})" scan_choice
    
    case "$scan_choice" in
        1) scan_type="-sS" ;;
        2) scan_type="-sA" ;;
        3) scan_type="-sU" ;;
        4) scan_type="-sV" ;;
        *) echo -e "${RED}Invalid scan type! Exiting.${NC}"; exit 1 ;;
    esac
    
    read -p "$(echo -e ${YELLOW}Enable OS detection? \(y/n\): ${NC})" os_choice
    if [[ "$os_choice" =~ ^[Yy]$ ]]; then
        scan_type="$scan_type -O"
    fi
    
    scan_network "$ip_range" "$port_range" "$scan_type"
}

main
