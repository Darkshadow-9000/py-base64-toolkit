import sys

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def manual_encode(data):
    """
    Encode text to Base64 manually.
    Supports UTF-8 encoded text with multi-byte characters.
    """
    if isinstance(data, str):
        data_bytes = data.encode('utf-8')
    else:
        data_bytes = data
    
    binary_str = ""
    for byte in data_bytes:
        binary_str += format(byte, "08b")

    padding_bits = (6 - len(binary_str) % 6) % 6
    binary_str += "0" * padding_bits

    encoded = ""
    for i in range(0, len(binary_str), 6):
        chunk = binary_str[i : i + 6]
        encoded += ALPHABET[int(chunk, 2)]

    # Correct padding logic: check how many bytes were in the original
    if len(data_bytes) % 3 == 1:
        encoded += "=="
    elif len(data_bytes) % 3 == 2:
        encoded += "="

    return encoded

def manual_decode(data):
    """
    Decode Base64 string back to text.
    Properly handles UTF-8 multi-byte characters.
    """
    if not isinstance(data, str):
        raise TypeError("Input must be a string")
    
    for char in data.rstrip("="):
        if char not in ALPHABET:
            raise ValueError(f"Invalid Base64 character: '{char}'")
    
    padding = data.count("=")
    clean_data = data.rstrip("=")

    binary_str = ""
    for char in clean_data:
        index = ALPHABET.index(char)
        binary_str += format(index, "06b")

    decoded_bytes = bytearray()

    for i in range(0, len(binary_str), 8):
        byte = binary_str[i : i + 8]
        if len(byte) == 8:
            decoded_bytes.append(int(byte, 2))

    if padding:
        decoded_bytes = decoded_bytes[:-padding]

    try:
        decoded_str = decoded_bytes.decode('utf-8')
    except UnicodeDecodeError:
        raise ValueError("Decoded data is not valid UTF-8")

    return decoded_str

def show_help():
    print("""
Base64 Manual Tool (No Libraries)
Usage: python3 base64.py [FLAG] [TEXT]

Flags:
  -e, --encode    Convert plain text to Base64
  -d, --decode    Convert Base64 string back to plain text
  -h, --help      Show this manual
  -n              no newline
    """
)

# Check if -n flag is present
no_newline = "-n" in sys.argv

# Filter out script name and -n flag
clean_args = [arg for arg in sys.argv[1:] if arg != "-n"]

if len(clean_args) < 1 or clean_args[0] in ["-h", "--help"]:
    show_help()
elif len(clean_args) < 2:
    print("[-] Error: Missing text. See --help")
else:
    flag = clean_args[0]
    text = " ".join(clean_args[1:])

    if flag in ["-e", "--encode"]:
        final_input = text if no_newline else text + "\n"
        try:
            print(f"Result: {manual_encode(final_input)}")
        except Exception as e:
            print(f"[-] Error during encoding: {e}")

    elif flag in ["-d", "--decode"]:
        try:
            print(f"Result: {manual_decode(text.strip())}")
        except ValueError as e:
            print(f"[-] Error: {e}")
        except TypeError as e:
            print(f"[-] Error: {e}")
    else:
        show_help()