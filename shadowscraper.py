import re
import os
import sys
import json
import csv
from pathlib import Path
from docx import Document
from PyPDF2 import PdfReader
from tqdm import tqdm
from colorama import Fore, Style, init

init(autoreset=True)

# ------------------ CONFIG ------------------ #
TOOL_NAME = "ShadowScraper CLI"
AUTHOR = "Made by g33l0 | Telegram: @x0x0h33l0"

BANNER = f"""
{Fore.GREEN}
███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗
██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║
███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║
╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║
███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝

{TOOL_NAME}
{AUTHOR}
{Style.RESET_ALL}
"""

# ------------------ REGEX ------------------ #
EMAIL_REGEX = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b")

DOMAIN_REGEX = re.compile(
    r"\b(?:https?://)?(?:www\.)?([a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+)\b"
)

URL_PATH_REGEX = re.compile(
    r"\bhttps?://[^\s\"'<>]+"
)

IPV4_REGEX = re.compile(
    r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"
)

IPV6_REGEX = re.compile(
    r"\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b|\b(?:[0-9a-fA-F]{1,4}:){1,7}:"
)

# ------------------ UTILS ------------------ #
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def exit_tool():
    print(Fore.RED + "\n[!] Exiting ShadowScraper CLI. Stay stealthy.")
    sys.exit(0)

def read_file_auto(filename):
    ext = Path(filename).suffix.lower()

    try:
        if ext in [".txt", ".log", ".csv", ".json", ".html", ".xml"]:
            with open(filename, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()

        elif ext == ".docx":
            doc = Document(filename)
            return "\n".join(p.text for p in doc.paragraphs)

        elif ext == ".pdf":
            reader = PdfReader(filename)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text

        else:
            with open(filename, "rb") as f:
                return f.read().decode(errors="ignore")

    except Exception as e:
        print(Fore.RED + f"[X] Error reading file: {e}")
        return None

def live_print(item):
    print(Fore.CYAN + "[+] Extracted:", Fore.YELLOW + item)

def save_output(data, fmt):
    output_file = f"extracted_output.{fmt}"

    if fmt == "txt":
        with open(output_file, "w", encoding="utf-8") as f:
            for item in sorted(data):
                f.write(item + "\n")

    elif fmt == "csv":
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for item in sorted(data):
                writer.writerow([item])

    elif fmt == "json":
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(sorted(data), f, indent=4)

    print(Fore.GREEN + f"\n[✔] Output saved to: {output_file}")

# ------------------ EXTRACTORS ------------------ #
def extract_emails(text):
    found = set()
    for email in EMAIL_REGEX.findall(text):
        if email not in found:
            live_print(email)
            found.add(email)
    return found

def extract_domains(text):
    found = set()
    for match in DOMAIN_REGEX.findall(text):
        domain = match.lower()
        if domain not in found:
            live_print(domain)
            found.add(domain)
    return found

def extract_urls(text):
    found = set()
    for url in URL_PATH_REGEX.findall(text):
        clean_url = url.rstrip('.,);]')
        if clean_url not in found:
            live_print(clean_url)
            found.add(clean_url)
    return found

def extract_ips(text):
    found = set()
    for ip in IPV4_REGEX.findall(text):
        if ip not in found:
            live_print(ip)
            found.add(ip)

    for ip in IPV6_REGEX.findall(text):
        if ip not in found:
            live_print(ip)
            found.add(ip)

    return found

# ------------------ MENU ------------------ #
def choose_output(data):
    while True:
        print("\n[?] Select output format:")
        print("1) TXT")
        print("2) CSV")
        print("3) JSON")
        print("0) Back")

        choice = input("> ").strip()

        if choice == "1":
            save_output(data, "txt")
            return
        elif choice == "2":
            save_output(data, "csv")
            return
        elif choice == "3":
            save_output(data, "json")
            return
        elif choice == "0":
            return
        elif choice.upper() == "ESC":
            exit_tool()

def main_menu():
    while True:
        clear()
        print(BANNER)
        print("1) Email Extractor")
        print("2) Website (Domain) Extractor")
        print("3) IP Address Extractor")
        print("4) Full URL Path Extractor")
        print("ESC) Exit\n")

        choice = input("> ").strip()

        if choice.upper() == "ESC":
            exit_tool()

        if choice not in ["1", "2", "3", "4"]:
            continue

        filename = input("\n[?] Enter filename in current directory: ").strip()
        if filename.upper() == "ESC":
            exit_tool()

        if not Path(filename).exists():
            print(Fore.RED + "[X] File not found.")
            input("Press Enter to continue...")
            continue

        print(Fore.MAGENTA + "\n[~] Reading file...")
        content = read_file_auto(filename)
        if not content:
            input("Press Enter to continue...")
            continue

        print(Fore.MAGENTA + "[~] Extracting data...\n")

        with tqdm(total=len(content), desc="Progress", bar_format=f"{Fore.GREEN}{{l_bar}}{{bar}}{Style.RESET_ALL}{{r_bar}}") as pbar:
            if choice == "1":
                data = extract_emails(content)
            elif choice == "2":
                data = extract_domains(content)
            elif choice == "3":
                data = extract_ips(content)
            elif choice == "4":
                data = extract_urls(content)
            pbar.update(len(content))

        print(Fore.GREEN + f"\n[✔] Done. Unique results: {len(data)}")
        choose_output(data)
        input("\nPress Enter to return to main menu...")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        exit_tool()