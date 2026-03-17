# Base64 Manual Tool 🛠️

A library-free, manual implementation of the Base64 encoding and decoding algorithm. This tool was developed to handle raw data manipulation in security contexts, specifically for creating or decoding payloads where hidden characters (like newlines) can cause failure in web exploitation.

## 🚀 Features

* **Zero Dependencies:** Built from the ground up using Python's bit-manipulation capabilities.
* **Terminal Accuracy:** Precisely mirrors the behavior of the standard Linux `base64` binary.
* **Smart Flag Handling:** Includes a `-n` flag to control trailing newlines, essential for CTFs and exploit development.
* **Robust Input:** Supports multi-word strings and handles shell quoting effectively.

## 🛠️ Installation & Setup

Ensure you are on a Linux environment (Tested on Linux Mint).

1. Clone the repository:
   ```bash
   git clone [https://github.com/Darkshadow-9000/base64-manual-tool.git](https://github.com/Darkshadow-9000/base64-manual-tool.git)
   cd base64-manual-tool

2. Make the script executable:
    chmod +x base64.py

 Usage:
python3 base64.py [FLAG] [TEXT]

Flags:
-e, --encode          Convert plain text to Base64
-d, --decode          Convert Base64 back to plain text
-n                    No-Newline mode: Matches echo -n (prevents adding \n)
-h, --help            Show the tool manual


Examples
Encoding (Standard behavior)
Matches the output of echo "TEXT" | base64:

python3 base64.py -e "Hello World"
# Result: SGVsbG8gV29ybGQK

Decoding
python3 base64.py -d "RkxBRyBTHM0="
# Result: FLAG THM


Technical Overview
This tool performs a manual conversion from 8-bit bytes to 6-bit Base64 indexes using a custom mapping to the Base64 alphabet. It includes specific logic to handle the mathematical padding (=) required when the input bit-stream is not a multiple of 24.         
