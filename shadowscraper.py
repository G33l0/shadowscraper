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
TOOL_NAME  = "ShadowScraper CLI"
VERSION    = "1.1.0"
AUTHOR     = "Made by g33l0 | Telegram: @x0x0h33l0"

BANNER = f"""
{Fore.GREEN}
███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗
██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║
███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║
╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║
███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝

  {TOOL_NAME}  v{VERSION}
  {AUTHOR}
{Style.RESET_ALL}
"""

# ------------------ REGEX ------------------ #

EMAIL_REGEX = re.compile(
    r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"
)

# FIX: Require TLD to be alpha-only so pure IP addresses (e.g. 192.168.1.1)
# are NOT matched as domains.  The original pattern used [a-zA-Z0-9-]+ for
# the last label which caused every IPv4 address to be captured as a domain.
DOMAIN_REGEX = re.compile(
    r"\b(?:https?://)?(?:www\.)?([a-zA-Z0-9-]+(?:\.[a-zA-Z]{2,})+)\b"
)

URL_PATH_REGEX = re.compile(
    r"\bhttps?://[^\s\"'<>]+"
)

IPV4_REGEX = re.compile(
    r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"
)

# FIX: The original IPv6 regex only matched fully-expanded addresses and one
# degenerate compressed form, silently missing fe80::1, ::1, 2001:db8::1000,
# and every other shortened notation.  The new pattern covers all RFC-4291
# compressed representations by listing alternatives longest-first so the
# regex engine commits to the correct branch before backtracking.
IPV6_REGEX = re.compile(
    r"(?:"
    r"(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}"               # 1:2:3:4:5:6:7:8
    r"|(?:[0-9a-fA-F]{1,4}:){6}:[0-9a-fA-F]{1,4}"              # 1:2:3:4:5:6::8
    r"|(?:[0-9a-fA-F]{1,4}:){5}(?::[0-9a-fA-F]{1,4}){1,2}"    # 1:2:3:4:5::7:8
    r"|(?:[0-9a-fA-F]{1,4}:){4}(?::[0-9a-fA-F]{1,4}){1,3}"    # 1:2:3:4::6:7:8
    r"|(?:[0-9a-fA-F]{1,4}:){3}(?::[0-9a-fA-F]{1,4}){1,4}"    # 1:2:3::5:6:7:8
    r"|(?:[0-9a-fA-F]{1,4}:){2}(?::[0-9a-fA-F]{1,4}){1,5}"    # 1:2::4:5:6:7:8
    r"|[0-9a-fA-F]{1,4}:(?::[0-9a-fA-F]{1,4}){1,6}"           # 1::3:4:5:6:7:8
    r"|(?:[0-9a-fA-F]{1,4}:){1,7}:"                            # 1:2:3:4:5:6:7::
    r"|::(?:[0-9a-fA-F]{1,4}:){0,6}[0-9a-fA-F]{1,4}"          # ::2:3:4:5:6:7:8
    r"|::"                                                       # :: (all-zeros)
    r")"
)

# Chunk size used to drive the real-time tqdm progress bar
_CHUNK = 4096

# ------------------ UTILS ------------------ #

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def exit_tool():
    print(Fore.RED + "\n[!] Exiting ShadowScraper CLI. Stay stealthy.")
    sys.exit(0)


def read_file_auto(filename: str) -> str | None:
    """Return the text content of *filename*, auto-detecting the format."""
    ext = Path(filename).suffix.lower()
    try:
        if ext in {".txt", ".log", ".csv", ".json", ".html", ".xml"}:
            with open(filename, "r", encoding="utf-8", errors="ignore") as fh:
                return fh.read()

        elif ext == ".docx":
            doc = Document(filename)
            return "\n".join(p.text for p in doc.paragraphs)

        elif ext == ".pdf":
            reader = PdfReader(filename)
            return "".join(page.extract_text() or "" for page in reader.pages)

        else:
            # Binary / unknown — decode best-effort
            with open(filename, "rb") as fh:
                return fh.read().decode(errors="ignore")

    except Exception as exc:
        print(Fore.RED + f"[X] Error reading file: {exc}")
        return None


def live_print(item: str) -> None:
    print(Fore.CYAN + "[+] Extracted: " + Fore.YELLOW + item)


def save_output(data: set, fmt: str) -> None:
    output_file = f"extracted_output.{fmt}"
    sorted_data = sorted(data)

    if fmt == "txt":
        with open(output_file, "w", encoding="utf-8") as fh:
            fh.writelines(item + "\n" for item in sorted_data)

    elif fmt == "csv":
        with open(output_file, "w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerows([item] for item in sorted_data)

    elif fmt == "json":
        with open(output_file, "w", encoding="utf-8") as fh:
            json.dump(sorted_data, fh, indent=4)

    print(Fore.GREEN + f"\n[✔] Output saved to: {output_file}")


# ------------------ EXTRACTORS ------------------ #
# FIX: All extractors now receive text in chunks so the tqdm bar reflects
# actual scanning progress instead of jumping from 0 % to 100 % instantly.

def _iter_chunks(text: str):
    """Yield (chunk, size) pairs over *text*."""
    for start in range(0, len(text), _CHUNK):
        chunk = text[start : start + _CHUNK]
        yield chunk, len(chunk)


def extract_emails(text: str, pbar: tqdm) -> set:
    found: set[str] = set()
    for chunk, size in _iter_chunks(text):
        for email in EMAIL_REGEX.findall(chunk):
            if email not in found:
                live_print(email)
                found.add(email)
        pbar.update(size)
    return found


def extract_domains(text: str, pbar: tqdm) -> set:
    found: set[str] = set()
    for chunk, size in _iter_chunks(text):
        for match in DOMAIN_REGEX.findall(chunk):
            domain = match.lower()
            if domain not in found:
                live_print(domain)
                found.add(domain)
        pbar.update(size)
    return found


def extract_urls(text: str, pbar: tqdm) -> set:
    found: set[str] = set()
    for chunk, size in _iter_chunks(text):
        for url in URL_PATH_REGEX.findall(chunk):
            clean = url.rstrip(".,);]")
            if clean not in found:
                live_print(clean)
                found.add(clean)
        pbar.update(size)
    return found


def extract_ips(text: str, pbar: tqdm) -> set:
    found: set[str] = set()
    for chunk, size in _iter_chunks(text):
        for ip in IPV4_REGEX.findall(chunk):
            if ip not in found:
                live_print(ip)
                found.add(ip)
        for ip in IPV6_REGEX.findall(chunk):
            if ip not in found:
                live_print(ip)
                found.add(ip)
        pbar.update(size)
    return found


# ------------------ MENU ------------------ #

def choose_output(data: set) -> None:
    while True:
        print("\n[?] Select output format:")
        print("  1) TXT")
        print("  2) CSV")
        print("  3) JSON")
        print("  0) Back")

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


def main_menu() -> None:
    extractors = {
        "1": ("Email Extractor",        extract_emails),
        "2": ("Website/Domain Extractor", extract_domains),
        "3": ("IP Address Extractor",   extract_ips),
        "4": ("Full URL Path Extractor", extract_urls),
    }

    while True:
        clear()
        print(BANNER)
        for key, (label, _) in extractors.items():
            print(f"  {key}) {label}")
        print("  ESC) Exit\n")

        choice = input("> ").strip()

        if choice.upper() == "ESC":
            exit_tool()

        if choice not in extractors:
            continue

        label, extractor_fn = extractors[choice]

        filename = input("\n[?] Enter filename (or path) to scan: ").strip()
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

        print(Fore.MAGENTA + f"[~] Running {label}...\n")

        # FIX: progress bar now advances in real chunks instead of one fake jump
        bar_fmt = f"{Fore.GREEN}{{l_bar}}{{bar}}{Style.RESET_ALL}{{r_bar}}"
        with tqdm(total=len(content), desc="Scanning", unit="B",
                  unit_scale=True, bar_format=bar_fmt) as pbar:
            data = extractor_fn(content, pbar)

        print(Fore.GREEN + f"\n[✔] Done. Unique results found: {len(data)}")

        if data:
            choose_output(data)
        else:
            print(Fore.YELLOW + "[!] No matches found in this file.")

        input("\nPress Enter to return to main menu...")


# ------------------ ENTRY POINT ------------------ #

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("-v", "--version"):
        print(f"ShadowScraper CLI v{VERSION}")
        sys.exit(0)

    try:
        main_menu()
    except KeyboardInterrupt:
        exit_tool()
