# 🕶️ ShadowScraper CLI

A fast, cross-platform data extraction tool for security research, recon, and OSINT.  
Extract emails, domains, IP addresses, and full URLs from almost any file type with live progress and hacker-style output.

> Made by g33l0 | Telegram: @x0x0h33l0

---

## ✨ Features

- ✅ Email extractor  
- ✅ Website / domain extractor  
- ✅ IP address extractor (IPv4 + IPv6)  
- ✅ Full URL path extractor  
- ✅ Works on Windows, macOS, Linux  
- ✅ Reads almost any file type  
- ✅ Live colored progress bar  
- ✅ Real-time extraction preview  
- ✅ Clean + deduplicated output  
- ✅ Export to TXT / CSV / JSON  
- ✅ Interactive menu (ESC to exit, 0 to go back)

---

## 📦 Requirements

- Python 3.9+
- Works on Windows, macOS, Linux

### Install dependencies

```bash
pip install python-docx PyPDF2 colorama tqdm

Usage
	1.	Place shadow_scraper.py in a folder
	2.	Place target file(s) in the same folder
    3.	Run:
    python shadow_scraper.py
    4.	Choose what to extract:
	•	1 Email addresses
	•	2 Domains
	•	3 IP addresses
	•	4 Full URLs
	•	ESC Exit
	5.	Choose output format:
	•	TXT
	•	CSV
	•	JSON

📂 Supported File Types

ShadowScraper automatically reads content from:
	•	.txt
	•	.log
	•	.csv
	•	.json
	•	.html
	•	.xml
	•	.pdf
	•	.docx
	•	.doc
	•	Binary / unknown formats

⸻

🧠 Example Use Cases
	•	Bug bounty recon
	•	OSINT investigations
	•	Log analysis
	•	Malware traffic analysis
	•	Endpoint discovery
	•	Asset mapping

⸻

⚠️ Disclaimer

This tool is intended for legal and ethical use only.
You are responsible for complying with applicable laws and policies.

⸻

🧩 Roadmap (Planned)
	•	Recursive folder scanning
	•	Subdomain extraction
	•	URL validation
	•	Multithreaded scanning
	•	HTML reports
	•	Portable EXE build

⸻

🧑‍💻 Author

Made by g33l0
Telegram: @x0x0h33l0