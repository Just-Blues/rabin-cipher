from crypto_methods import str_to_int, encryption, \
    decryption, int_to_str
from helpers import bcolors


def encrypt_cbc(p, q, plaintext, initializing_vector=920441868394157507):
    cipher_text = cbc_encryption(plaintext, p * p * q if p < q else q * q * p, initializing_vector)

    print()
    print(
        f"{bcolors.GREEN}====================== {bcolors.BOLD}Rabin Cipher - CBC mode - ENCRYPTION{bcolors.ENDC} {bcolors.GREEN}======================{bcolors.ENDC}")
    print()
    print(f"{bcolors.CYAN}p = ", p)
    print(f"q = ", q)
    print(f"{bcolors.ENDC}")
    print(f"{bcolors.ORANGE}Plaintext: ", plaintext)
    print(f"{bcolors.ENDC}")
    print(f"{bcolors.RED}Ciphertext: ", cipher_text)
    print(f"{bcolors.ENDC}")

    return cipher_text


def decrypt_cbc(p, q, cipher_text, initializing_vector=920441868394157507):
    decrypted_message = cbc_decryption(cipher_text, p, q, initializing_vector)

    print("\n")
    print(
        f"{bcolors.GREEN}====================== {bcolors.BOLD}Rabin Cipher - CBC mode - DECRYPTION{bcolors.ENDC} {bcolors.GREEN}======================{bcolors.ENDC}")
    print()
    print(f"{bcolors.CYAN}p = ", p)
    print(f"q = ", q)
    print(f"{bcolors.ENDC}")
    print(f"{bcolors.ORANGE}Ciphertext: ", cipher_text)
    print(f"{bcolors.ENDC}")
    print(f"{bcolors.RED}Decrypted message as plaintext: ", decrypted_message)
    print(f"{bcolors.ENDC}")

    return decrypted_message


# Initializing_vector must have 64 bits (size of block)
def cbc_encryption(plaintext, n, initializing_vector):
    int_plaintext = str_to_int(plaintext)
    encrypted = []
    for i in range(0, len(int_plaintext)):
        if i == 0:
            aux = int_plaintext[0] ^ initializing_vector
        else:
            mask = encrypted[i - 1] & 0xFFFFFFFFFFFFFFFFFFFF
            aux = int_plaintext[i] ^ mask
        encrypted.append(encryption(aux, n))

    return encrypted


def cbc_decryption(ciphered_msg, p, q, initializing_vector):
    decrypted = []
    for i in range(0, len(ciphered_msg)):
        if i == 0:
            aux = decryption(ciphered_msg[0], p, q) ^ initializing_vector
        else:
            mask = ciphered_msg[i - 1] & 0xFFFFFFFFFFFFFFFFFFFF
            aux = decryption(ciphered_msg[i], p, q) ^ mask

        decrypted.append(aux)

    str_decrypted = int_to_str(decrypted)
    return str_decrypted

