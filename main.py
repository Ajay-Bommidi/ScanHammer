import random
import os
import subprocess
from art import text2art
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Motivational hacking quotes
quotes = [
    "The quieter you become, the more you can hear. — Anonymous",
    "Hacking is not about breaking things; it's about understanding them. — Unknown",
    "The best way to learn is to break something and fix it. — Hackers' Creed",
    "In a world full of locks, be a key. — Anonymous",
    "Code is poetry, and hacking is art. — Unknown"
]

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    """Display the ASCII art banner and tool information."""
    banner = text2art("ScanHammer", font="block")
    print(Fore.CYAN + Style.BRIGHT + banner)
    print(Fore.GREEN + Style.BRIGHT + "          ScanHammer: A Network Recon and Testing Tool")
    print(Fore.YELLOW + "          Created by Ajay Bommidi")
    print(Fore.YELLOW + "          GitHub: https://github.com/Ajay-Bommidi/ScanHammer.git")
    print(Style.RESET_ALL + "-" * 70)

def display_disclaimer():
    """Display legal and ethical disclaimer."""
    print(Fore.RED + Style.BRIGHT + "\n[!] DISCLAIMER:")
    print(Fore.RED + "This tool is for EDUCATIONAL PURPOSES ONLY. Unauthorized use of network scanning or DoS tools")
    print(Fore.RED + "against systems without explicit permission is ILLEGAL and UNETHICAL.")
    print(Fore.RED + "Use responsibly and only on systems you own or have permission to test.")
    print(Style.RESET_ALL + "-" * 70)

def display_quote():
    """Display a random motivational hacking quote."""
    print(Fore.MAGENTA + Style.BRIGHT + "\nQuote of the Day:")
    print(Fore.MAGENTA + random.choice(quotes))
    print(Style.RESET_ALL + "-" * 70)

def display_menu():
    """Display the main menu options."""
    print(Fore.GREEN + Style.BRIGHT + "\nMain Menu:")
    print(Fore.GREEN + "1. Network Scanning (Nmap-inspired)")
    print(Fore.GREEN + "2. Perform DoS Attack (Humangous)")
    print(Fore.GREEN + "3. Exit")
    print(Style.RESET_ALL + "-" * 70)

def main():
    """Main function to run the ScanHammer CLI interface."""
    clear_screen()
    display_banner()
    display_disclaimer()
    display_quote()
    
    while True:
        display_menu()
        choice = input(Fore.YELLOW + Style.BRIGHT + "Enter your choice (1-3): " + Style.RESET_ALL)
        
        if choice == "1":
            print(Fore.CYAN + "\nStarting Network Scanner...")
            try:
                subprocess.run(["sudo", "bash", "NetScanner.sh"], check=True)
            except subprocess.CalledProcessError as e:
                print(Fore.RED + f"Error running Network Scanner: {e}")
            input(Fore.YELLOW + "\nPress Enter to return to the menu...")
            clear_screen()
            display_banner()
            display_disclaimer()
            display_quote()
        
        elif choice == "2":
            print(Fore.CYAN + "\nStarting DoS Attack Tool...")
            try:
                subprocess.run(["bash", "humangous.sh"], check=True)
            except subprocess.CalledProcessError as e:
                print(Fore.RED + f"Error running DoS Tool: {e}")
            input(Fore.YELLOW + "\nPress Enter to return to the menu...")
            clear_screen()
            display_banner()
            display_disclaimer()
            display_quote()
        
        elif choice == "3":
            print(Fore.GREEN + "\nExiting ScanHammer. Stay ethical!")
            break
        else:
            print(Fore.RED + "\nInvalid choice! Please select 1, 2, or 3.")
            input(Fore.YELLOW + "Press Enter to continue...")
            clear_screen()
            display_banner()
            display_disclaimer()
            display_quote()

if __name__ == "__main__":
    main()
