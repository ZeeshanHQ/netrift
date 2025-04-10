import socket
import time
import os
import colorama
from colorama import Fore, Style

# Initialize colorama for colored output
colorama.init(autoreset=True)

# Display NETRIFT logo and version info
def display_logo_and_version():
    version = ""
    try:
        with open("version.txt", "r") as file:
            version = file.read().strip()
    except FileNotFoundError:
        version = "Unknown"
        
    logo = """
    _____  ___    _______  ___________  _______    __     _______  ___________  
    ("   \|"  \  /"     "|("     _   ")/"      \  |" \   /"     "|("     _   ") 
    |.\\   \    |(: ______) )__/  \\__/|:        | ||  | (: ______) )__/  \\__/  
    |: \.   \\  | \/    |      \\_ /   |_____/   ) |:  |  \/    |      \\_ /     
    |.  \    \. | // ___)_     |.  |    //      /  |.  |  // ___)      |.  |     
    |    \    \ |(:      "|    \:  |   |:  __   \  /\  |\(:  (         \:  |     
     \___|\____\) \_______)     \__|   |__|  \___)(__\_|_)\__/          \__|     
    """
    
    print(Fore.BLUE + logo)
    print(Fore.CYAN + f"NETRIFT Version: {version}")
    print(Fore.YELLOW + "-"*80)

# Function to perform port scanning
def port_scan(target_ip):
    print(Fore.YELLOW + f"Scanning ports on {target_ip}...")
    open_ports = []
    try:
        smb_port = 445
        rdp_port = 3389
        print(Fore.YELLOW + f"Checking SMB port ({smb_port})...")
        smb = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        smb.settimeout(1)
        if smb.connect_ex((target_ip, smb_port)) == 0:
            open_ports.append(smb_port)
            print(Fore.GREEN + f"SMB port ({smb_port}) is open")
        else:
            print(Fore.RED + f"SMB port ({smb_port}) is closed")

        print(Fore.YELLOW + f"Checking RDP port ({rdp_port})...")
        rdp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rdp.settimeout(1)
        if rdp.connect_ex((target_ip, rdp_port)) == 0:
            open_ports.append(rdp_port)
            print(Fore.GREEN + f"RDP port ({rdp_port}) is open")
        else:
            print(Fore.RED + f"RDP port ({rdp_port}) is closed")
    except Exception as e:
        print(Fore.RED + f"Error during port scan: {e}")
    return open_ports

# Function to perform brute-force attack
def brute_force(target_ip, wordlist_path):
    print(Fore.YELLOW + f"Starting brute-force attack on {target_ip} using wordlist {wordlist_path}...")
    try:
        with open(wordlist_path, 'r') as file:
            wordlist = file.readlines()

        for attempt in wordlist:
            username, password = attempt.strip().split(':')
            print(Fore.CYAN + f"Trying: {username} / {password}")
            # Simulating attack, here you can add logic to test the credentials.
            time.sleep(1)  # Simulate delay between attempts
            # Here you would add your attack logic like trying SMB, RDP, etc.
            # For demo purposes, we're assuming that "admin:admin" is the correct combo
            if username == "admin" and password == "admin":
                print(Fore.GREEN + f"Success: Found valid credentials -> {username}:{password}")
                return
        print(Fore.RED + "Brute-force attack failed. No valid credentials found.")
    except FileNotFoundError:
        print(Fore.RED + f"Error: Wordlist file '{wordlist_path}' not found.")
    except Exception as e:
        print(Fore.RED + f"Error during brute-force attack: {e}")

# Function to get user input for the target (hostname or IP)
def get_target():
    print(Fore.YELLOW + "Enter the target's IP address or hostname:")
    target = input(Fore.MAGENTA + "Target (hostname/IP): ")
    return target

# Function to get the wordlist option
def get_wordlist_option():
    print(Fore.YELLOW + "Do you want to use your own wordlist or the default 'rockyou.txt'?")
    print(Fore.MAGENTA + "1. Use my own wordlist")
    print(Fore.MAGENTA + "2. Use default 'rockyou.txt' wordlist")
    choice = input(Fore.YELLOW + "Enter your choice (1/2): ")
    if choice == "1":
        print(Fore.YELLOW + "Please provide the full path to your wordlist file:")
        wordlist_path = input(Fore.MAGENTA + "Path to wordlist: ")
    elif choice == "2":
        wordlist_path = "rockyou.txt"  # Default wordlist
    else:
        print(Fore.RED + "Invalid choice, using default 'rockyou.txt'")
        wordlist_path = "rockyou.txt"
    return wordlist_path

# Main program flow
def main():
    display_logo_and_version()

    # Get target (IP or hostname)
    target = get_target()

    # Get wordlist choice
    wordlist_path = get_wordlist_option()

    # Select attack type
    print(Fore.YELLOW + "Choose the attack type:")
    print(Fore.MAGENTA + "1. Port Scanning (SMB, RDP)")
    print(Fore.MAGENTA + "2. Brute-Force Attack")
    attack_choice = input(Fore.YELLOW + "Enter your choice (1/2): ")

    if attack_choice == "1":
        # Perform port scan
        open_ports = port_scan(target)
        if not open_ports:
            print(Fore.RED + "No open ports found.")
        else:
            print(Fore.GREEN + f"Open ports: {', '.join(map(str, open_ports))}")
    elif attack_choice == "2":
        # Perform brute-force attack
        brute_force(target, wordlist_path)
    else:
        print(Fore.RED + "Invalid choice.")

if __name__ == "__main__":
    main()
