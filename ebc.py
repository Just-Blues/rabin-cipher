from main import ebc_encryption, ebc_decryption, str_to_int


def run_ebc(p, q, plaintext):
    way_bigger_key = p * p * q  # any key has to be bigger than this one

    plaint_text_to_int = str_to_int(plaintext, way_bigger_key)
    cipher_text = ebc_encryption(plaint_text_to_int, way_bigger_key)
    decrypted_message = ebc_decryption(cipher_text, p, q)

    print("========================== Rabin Cipher - ECB mode ==========================")
    print()
    print("p = ", p)
    print()
    print("q = ", q)
    print()
    print("Plaintext: ", plaintext)
    print()
    print("Ciphertext: ", cipher_text)
    print()
    print(decrypted_message)