from crypto_methods import str_to_int, encryption, decryption, int_to_str
from helpers import bcolors


def encrypt_ebc(p, q, plaintext):
    cipher_text = ebc_encryption(plaintext, p * p * q if p < q else q * q * p)

    print()
    print(
        f"{bcolors.GREEN}====================== {bcolors.BOLD}Rabin Cipher - ECB mode - ENCRYPTION{bcolors.ENDC} {bcolors.GREEN}======================{bcolors.ENDC}")
    print()
    print(f"{bcolors.CYAN}p = ", p)
    print(f"q = ", q)
    print(f"{bcolors.ENDC}")
    print(f"{bcolors.ORANGE}Plaintext: ", plaintext)
    print(f"{bcolors.ENDC}")
    print(f"{bcolors.RED}Ciphertext: ", cipher_text)
    print(f"{bcolors.ENDC}")

    return cipher_text


def decrypt_ebc(p, q, cipher_text):
    decrypted_message = ebc_decryption(cipher_text, p, q)

    print("\n")
    print(
        f"{bcolors.GREEN}====================== {bcolors.BOLD}Rabin Cipher - ECB mode - DECRYPTION{bcolors.ENDC} {bcolors.GREEN}======================{bcolors.ENDC}")
    print()
    print(f"{bcolors.CYAN}p = ", p)
    print(f"q = ", q)
    print(f"{bcolors.ENDC}")
    print(f"{bcolors.ORANGE}Ciphertext: ", cipher_text)
    print(f"{bcolors.ENDC}")
    print(f"{bcolors.RED}Decrypted message as plaintext: ", decrypted_message)
    print(f"{bcolors.ENDC}")

    return decrypted_message


def ebc_encryption(plaintext, n):
    int_plaintext = str_to_int(plaintext)
    encrypted = []
    for i in range(0, len(int_plaintext)):
        encrypted.append(encryption(int_plaintext[i], n))

    return encrypted


def ebc_decryption(ciphered_msg, p, q):
    decrypted = []
    for i in range(0, len(ciphered_msg)):
        # print("Iteration: ", i)
        decrypted.append(decryption(ciphered_msg[i], p, q))

    str_decrypted = int_to_str(decrypted)

    return str_decrypted

