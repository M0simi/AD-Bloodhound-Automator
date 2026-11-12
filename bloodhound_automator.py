#!/usr/bin/env python3
"""
AD-Bloodhound-Automator: Active Directory Enumeration & Bloodhound Data Prep Suite
Author: Meshari (M0simi)
Description: Automates the execution of Bloodhound data collection (using Sharphound or Python-based alternatives)
             and structures the output directory for offensive security assessments.
"""

import os
import sys
import argparse
import subprocess
from datetime import datetime

def banner():
    print(r"""
    █████╗ ██████╗       ██████╗ ██╗      ██████╗  ██████╗ ██╗  ██╗███╗   ██╗██████╗ 
   ██╔══██╗██╔══██╗      ██╔══██╗██║     ██╔═══██╗██╔═══██╗██║  ██║████╗  ██║██╔══██╗
   ███████║██║  ██║█████╗██████╔╝██║     ██║   ██║██║   ██║███████║██╔██╗ ██║██║  ██║
   ██╔══██║██║  ██║╚════╝██╔══██╗██║     ██║   ██║██║   ██║██╔══██║██║╚██╗██║██║  ██║
   ██║  ██║██████╔╝      ██████╔╝███████╗╚██████╔╝╚██████╔╝██║  ██║██║ ╚████║██████╔╝
   ╚═╝  ╚═╝╚══════╝       ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝
                 [ AD-Bloodhound-Automator v1.0 - Offensive Security Suite ]
    """)

def check_dependencies():
    """Verify if bloodhound-python or required tooling is available."""
    print("[*] Checking environment dependencies...")
    # Check if bloodhound-python is installed in the path
    try:
        subprocess.run(["bloodhound-python", "--help"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def run_collection(domain, username, password, dc_ip, collection_methods, output_dir):
    """Execute bloodhound-python collection against the target domain."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"[+] Created output directory: {output_dir}")

    cmd = [
        "bloodhound-python",
        "-d", domain,
        "-u", username,
        "-p", password,
        "-dc", dc_ip,
        "-c", collection_methods,
        "--zip",
        "-outputdir", output_dir
    ]

    print(f"\n[+] Launching Bloodhound collection against {domain} (DC: {dc_ip})...")
    print(f"[*] Executing command with methods: {collection_methods}")
    
    try:
        # Mask password in logs
        masked_cmd = cmd.copy()
        masked_cmd[6] = "********"
        print(f"[*] Command: {' '.join(masked_cmd)}\n")

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(f"    {output.strip()}")
                
        rc = process.poll()
        if rc == 0:
            print("\n[+] Bloodhound data collection completed successfully!")
        else:
            print(f"\n[-] Collection process returned non-zero exit code: {rc}")
            
    except Exception as e:
        print(f"[-] Critical error executing collection: {e}")

def main():
    banner()
    parser = argparse.ArgumentParser(description="Automate Active Directory Bloodhound Collection")
    parser.add_argument("-d", "--domain", required=True, help="Target Active Directory Domain (e.g., corp.local)")
    parser.add_argument("-u", "--username", required=True, help="Domain username for authentication")
    parser.add_argument("-p", "--password", required=True, help="Domain password")
    parser.add_argument("--dc-ip", required=True, help="IP address of the Domain Controller")
    parser.add_argument("-c", "--methods", default="All", help="Collection methods (Default: All, options: Group, LocalAdmin, Session, Trust, DCOnly, etc.)")
    parser.add_argument("-o", "--output", default="./bloodhound_output", help="Directory to store collected JSON/ZIP reports")
    
    args = parser.parse_args()

    print(f"[+] Target Domain: {args.domain}")
    print(f"[+] Domain Controller: {args.dc_ip}")
    print(f"[+] User: {args.username}")
    print(f"[+] Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    if not check_dependencies():
        print("[!] Warning: 'bloodhound-python' is not found in your system path.")
        print("[!] Please install it using: pip install bloodhound")
        choice = input("[?] Do you want to proceed anyway? (y/N): ").strip().lower()
        if choice != 'y':
            sys.exit(1)

    run_collection(
        domain=args.domain,
        username=args.username,
        password=args.password,
        dc_ip=args.dc_ip,
        collection_methods=args.methods,
        output_dir=args.output
    )

if __name__ == "__main__":
    main()
