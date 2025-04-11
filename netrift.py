import socket
import os
import sys
import time
import random
import hashlib
import threading
import requests
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Auto-version check via GitHub raw file (if hosted)
def check_latest_version(local_version):
    try:
        response = requests.get("https://raw.githubusercontent.com/ZeeshanHQ/netrift/main/version.txt", timeout=5)
        if response.status_code == 200:
            latest_version = response.text.strip()
            if latest_version != local_version:
                print(Fore.RED + f"[!] Update available: {latest_version} (You are using {local_version})")
                print(Fore.YELLOW + "Visit https://github.com/YOUR_GITHUB_USERNAME/netrift to update.")
        else:
            print(Fore.RED + "[!] Failed to check latest version.")
    except Exception:
        print(Fore.RED + "[!] Could not connect to check for updates.")

def display_logo_and_version():
    try:
        with open("version.txt", "r") as f:
            version = f.read().strip()
    except FileNotFoundError:
        version = "Unknown"
    check_latest_version(version)
    logo = r"""
   _____  ___    _______  ___________  _______    __     _______  ___________
  ("   \|"  \  /"     "|("     _   ")/"      \  |" \   /"     "|("     _   ")
  |.\\   \    |(: ______) )__/  \\__/|:        | ||  | (: ______) )__/  \\__/
  |: \.   \\  | \/    |      \\_ /   |_____/   ) |:  |  \/    |      \\_ /
  |.  \    \. | // ___)_     |.  |    //      /  |.  |  // ___)      |.  |
  |    \    \ |(:      "|    \:  |   |:  __   \  /\  |\(:  (         \:  |
   \___|\____\) \_______)     \__|   |__|  \___)(__\_|_)\__/          \__|
    """
    print(Fore.CYAN + logo)
    print(Fore.YELLOW + f"NETRIFT Version: {version}")
    print(Fore.GREEN + "-" * 80)

# Port scanner function
def port_scan(ip):
    print(Fore.YELLOW + f"[+] Scanning ports on {ip}...")
    ports = [445, 3389]
    open_ports = []
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((ip, port))
        if result == 0:
            print(Fore.GREEN + f"[OPEN] Port {port}")
            open_ports.append(port)
        else:
            print(Fore.RED + f"[CLOSED] Port {port}")
        s.close()
    return open_ports

# Brute-force (with threading)
def brute_worker(ip, creds, lock):
    for line in creds:
        try:
            user, pwd = line.strip().split(":")
            print(Fore.MAGENTA + f"[*] Trying {user}:{pwd}")
            time.sleep(0.5)
            if user == "admin" and pwd == "admin":
                with lock:
                    print(Fore.GREEN + f"[SUCCESS] Credentials found: {user}:{pwd}")
                    return
        except:
            continue

def brute_force(ip, wordlist_path):
    print(Fore.YELLOW + f"[+] Starting brute-force on {ip}")
    try:
        with open(wordlist_path, "r") as f:
            creds = f.readlines()
        lock = threading.Lock()
        thread = threading.Thread(target=brute_worker, args=(ip, creds, lock))
        thread.start()
        thread.join()
    except FileNotFoundError:
        print(Fore.RED + f"[!] Wordlist not found: {wordlist_path}")

# Hash cracking (optional future)
def crack_md5(hash_value, wordlist_path):
    try:
        with open(wordlist_path, "r") as f:
            for line in f:
                line = line.strip()
                if hashlib.md5(line.encode()).hexdigest() == hash_value:
                    print(Fore.GREEN + f"[+] Match found: {line}")
                    return
        print(Fore.RED + "[!] No match found.")
    except:
        print(Fore.RED + "[!] Error reading wordlist.")

# Get user inputs
def get_target():
    return input(Fore.YELLOW + "Enter target IP or hostname: ")

def get_wordlist():
    print(Fore.YELLOW + "1. Use your own wordlist\n2. Use default rockyou.txt")
    choice = input("Choice (1/2): ")
    if choice == "1":
        return input("Enter full path to wordlist: ")
    return "rockyou.txt"

# Main logic
def main():
    display_logo_and_version()
    target = get_target()
    try:
        socket.gethostbyname(target)
    except:
        print(Fore.RED + "[!] Invalid IP or hostname.")
        return
    wordlist = get_wordlist()
    print(Fore.YELLOW + "1. Port Scan\n2. Brute-Force Attack\n3. Crack MD5 Hash")
    choice = input("Select attack type: ")
    if choice == "1":
        port_scan(target)
    elif choice == "2":
        brute_force(target, wordlist)
    elif choice == "3":
        hash_val = input("Enter MD5 hash: ")
        crack_md5(hash_val, wordlist)
    else:
        print(Fore.RED + "[!] Invalid choice.")

if __name__ == "__main__":
    main()
