# 🕶️ ShadowScraper CLI

<p align="center">
  <img src="https://img.shields.io/badge/version-1.1.0-brightgreen?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=for-the-badge" alt="Platform">
  <img src="https://img.shields.io/badge/license-MIT-orange?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/maintained-yes-success?style=for-the-badge" alt="Maintained">
</p>

<p align="center">
  A fast, cross-platform OSINT and recon data-extraction CLI.<br>
  Extract emails, domains, IP addresses (IPv4 <strong>and</strong> IPv6), and full URLs from almost any file type — with live progress and hacker-style terminal output.
</p>

<p align="center">
  <strong>Made by g33l0</strong> &nbsp;|&nbsp;
  <a href="https://t.me/x0x0h33l0">Telegram: @x0x0h33l0</a>
</p>

---

## 📑 Table of Contents

- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
- [Supported File Types](#-supported-file-types)
- [Example Use Cases](#-example-use-cases)
- [Roadmap](#-roadmap)
- [Changelog](#-changelog)
- [Disclaimer](#️-disclaimer)
- [Author](#-author)

---

## ✨ Features

- **Email extractor** — RFC-compliant pattern, deduplication out of the box
- **Domain / website extractor** — strips scheme and `www.`, alpha-TLD validation (IPv4 addresses are no longer falsely matched as domains)
- **IP address extractor** — full IPv4 *and* all compressed IPv6 forms (`fe80::1`, `::1`, `2001:db8::1000`, etc.)
- **Full URL path extractor** — captures complete paths including query strings
- **Real-time progress bar** — tqdm bar advances as the file is actually scanned, not at the end
- **Live extraction preview** — every hit is printed to the terminal as it is found
- **Clean, deduplicated output** — results are stored in a `set` and sorted before export
- **Export formats** — TXT, CSV, or JSON
- **Cross-platform** — Windows, macOS, Linux
- **Wide file-type support** — see [Supported File Types](#-supported-file-types)
- **Interactive menu** — ESC to exit anywhere, `0` to go back

---

## 📦 Requirements

| Requirement | Detail |
|---|---|
| Python | 3.9 or newer (3.11 recommended) |
| OS | Windows, macOS, Linux |
| Terminal | Any modern terminal with ANSI colour support |

### Python dependencies

| Package | Purpose |
|---|---|
| `python-docx` | Read `.docx` Word documents |
| `PyPDF2` | Read `.pdf` files |
| `colorama` | Cross-platform ANSI colour support |
| `tqdm` | Progress bar |

---

## 🚀 Installation

```bash
# 1. Clone the repository
git clone https://github.com/g33l0/shadowscraper.git
cd shadowscraper

# 2. (Recommended) Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

---

## 🖥️ Usage

```bash
python shadowscraper.py
```

**Step-by-step:**

1. Launch the tool — the interactive menu is displayed.
2. Choose an extractor:
   - `1` — Email addresses
   - `2` — Domains / websites
   - `3` — IP addresses (IPv4 + IPv6)
   - `4` — Full URLs
   - `ESC` — Exit
3. Enter the path to the target file.
4. Watch results stream in real time as the file is scanned.
5. Choose an export format when scanning completes:
   - `1` TXT
   - `2` CSV
   - `3` JSON
   - `0` Back (skip saving)

Output is written to `extracted_output.<format>` in the current directory.

### Version flag

```bash
python shadowscraper.py --version
# ShadowScraper CLI v1.1.0
```

---

## 📂 Supported File Types

| Extension | Method |
|---|---|
| `.txt` `.log` `.csv` `.json` `.html` `.xml` | UTF-8 text read |
| `.docx` | `python-docx` paragraph extraction |
| `.pdf` | `PyPDF2` page text extraction |
| Binary / unknown | Best-effort `decode(errors='ignore')` |

---

## 🧠 Example Use Cases

- Bug bounty recon — harvest endpoints, emails, and IPs from downloaded assets
- OSINT investigations — extract contact info and infrastructure from leaked docs
- Log analysis — pull IPs and domains from server or firewall logs
- Malware traffic analysis — surface C2 IPs and URLs from capture files
- Endpoint / asset discovery — map an organisation's exposed infrastructure
- CTF challenges — rapid IOC extraction from challenge files

---

## 🧩 Roadmap

- [ ] Recursive folder / directory scanning
- [ ] Subdomain extraction
- [ ] URL reachability validation (`HEAD` request)
- [ ] Multi-threaded scanning for large file sets
- [ ] HTML report export
- [ ] Portable standalone EXE (PyInstaller build)
- [ ] Regex confidence scoring / false-positive filtering
- [ ] CIDR / IP range detection

---

## 📝 Changelog

### v1.1.0
- **Fix:** Domain regex no longer matches IPv4 addresses as domains (TLD now requires alpha characters only)
- **Fix:** IPv6 regex completely rewritten — all RFC-4291 compressed forms are now correctly matched (`fe80::1`, `::1`, `2001:db8::1000`, etc.)
- **Fix:** tqdm progress bar now advances in real chunks as the file is scanned instead of jumping from 0% to 100% at the end
- **Improvement:** Extractors refactored to use a shared chunked-iteration helper
- **Improvement:** Added `--version` / `-v` CLI flag
- **Improvement:** Empty-result case now shows a clear warning instead of silently skipping the save menu

### v1.0.0
- Initial release

---

## ⚠️ Disclaimer

> This tool is intended for **legal and ethical security research only**.  
> You are solely responsible for ensuring your use complies with all applicable laws, regulations, and authorisation requirements.  
> The author accepts no liability for misuse.

---

## 🧑‍💻 Author

**g33l0**

- Telegram: [@x0x0h33l0](https://t.me/x0x0h33l0)

---

<p align="center">
  <sub>Stay stealthy. Stay ethical.</sub>
</p>
