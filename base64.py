import sys

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def manual_encode(data):
    # 1. Convert everything to an 8-bit binary string
    binary_str = ""
    for char in data:
        binary_str += format(ord(char), "08b")

    # 2. Add '0' bits to make the TOTAL length a multiple of 6
    # This ensures the last character (like the 'o' in Hello) isn't cut off
    padding_bits = (6 - len(binary_str) % 6) % 6
    binary_str += "0" * padding_bits

    # 3. Convert 6-bit chunks into Base64 characters
    encoded = ""
    for i in range(0, len(binary_str), 6):
        chunk = binary_str[i : i + 6]
        encoded += ALPHABET[int(chunk, 2)]

    # 4. The Correct Padding Logic:
    # Instead of slicing [:-1], we check how many bytes were in the original
    # 1 byte left over -> needs 2 padding characters (==)
    # 2 bytes left over -> needs 1 padding character (=)
    if len(data) % 3 == 1:
        encoded += "=="
    elif len(data) % 3 == 2:
        encoded += "="

    return encoded


def manual_decode(data):
    padding = data.count("=")
    clean_data = data.rstrip("=")

    binary_str = ""
    for char in clean_data:
        index = ALPHABET.index(char)
        binary_str += format(index, "06b")

    decoded_bytes = []

    for i in range(0, len(binary_str), 8):
        byte = binary_str[i : i + 8]
        if len(byte) == 8:
            decoded_bytes.append(chr(int(byte, 2)))

    decoded_str = "".join(decoded_bytes)

    # remove padding effect
    if padding:
        decoded_str = decoded_str[:-padding]

    return decoded_str


def show_help():
    print("""
Base64 Manual Tool (No Libraries)
Usage: python3 manual_b64.py [FLAG] [TEXT]

Flags:
  -e, --encode    Convert plain text to Base64
  -d, --decode    Convert Base64 string back to plain text
  -h, --help      Show this manual
  -n              no newline
    """)


# --- Command Line Logic ---
# 1. Check if -n is present anywhere in the arguments
no_newline = "-n" in sys.argv

# 2. Filter out the script name AND the -n flag to find our command and text
# This leaves us with a clean list of just the meaningful parts
clean_args = [arg for arg in sys.argv[1:] if arg != "-n"]

if len(clean_args) < 1 or clean_args[0] in ["-h", "--help"]:
    show_help()
elif len(clean_args) < 2:
    print("[-] Error: Missing text. See --help")
else:
    flag = clean_args[0]
    # Grab all remaining arguments as the text to handle spaces automatically
    text = " ".join(clean_args[1:])

    if flag in ["-e", "--encode"]:
        # The Trick: If NO -n is present, add the newline to match 'echo'
        # If -n IS present, leave the text exactly as it is.
        final_input = text if no_newline else text + "\n"
        print(f"Result: {manual_encode(final_input)}")

    elif flag in ["-d", "--decode"]:
        try:
            # We strip the text for decoding to avoid math errors from trailing spaces
            print(f"Result: {manual_decode(text.strip())}")
        except ValueError:
            print("[-] Error: Invalid Base64 character provided.")
    else:
        show_help()
