from main import ebc_encryption, ebc_decryption, str_to_int


def encrypt(p, q, plaintext):

    cipher_text = ebc_encryption(plaintext, p * p * q if p < q else q * q * p)

    print()
    print(f"{bcolors.GREEN}====================== {bcolors.BOLD}Rabin Cipher - ECB mode - ENCRYPTION{bcolors.ENDC} {bcolors.GREEN}======================{bcolors.ENDC}")
    print()
    print(f"{bcolors.CYAN}p = ", p)
    print(f"q = ", q)
    print(f"{bcolors.ENDC}")
    print(f"{bcolors.ORANGE}Plaintext: ", plaintext)
    print(f"{bcolors.ENDC}")
    print(f"{bcolors.RED}Ciphertext: ", cipher_text)
    print(f"{bcolors.ENDC}")

    return cipher_text


def decrypt(p, q, cipher_text):

    decrypted_message = ebc_decryption(cipher_text, p, q)

    print(decrypted_message)

    print("\n")
    print(f"{bcolors.GREEN}====================== {bcolors.BOLD}Rabin Cipher - ECB mode - DECRYPTION{bcolors.ENDC} {bcolors.GREEN}======================{bcolors.ENDC}")
    print()
    print(f"{bcolors.CYAN}p = ", p)
    print(f"q = ", q)
    print(f"{bcolors.ENDC}")
    print(f"{bcolors.ORANGE}Ciphertext: ", cipher_text)
    print(f"{bcolors.ENDC}")
    print(f"{bcolors.RED}Plaintext: ", decrypted_message)
    print(f"{bcolors.ENDC}")

    return cipher_text


class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'