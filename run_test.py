import filecmp

import auxilliary
from cbc import cbc_encryption, cbc_decryption
from ebc import ebc_encryption, ebc_decryption
from helpers import bcolors


def run_test():
    # Proper test below
    print(f"{bcolors.ORANGE}\n\nTEST 1{bcolors.ENDC}")

    text = "ź{}random string, test|EjLmQ6yxCJ, V4nA4RUJxe ą 52G8AiCnv2 osSq4PGlJi  DAoMc7bIj3 BjYV0ewIf1sadxz///522u30LrCk ę "
    print(f"{bcolors.CYAN}Input text:{bcolors.RED}")
    print(text)
    print(f"{bcolors.CYAN}Generating p, q and IV using Miller-Rabin Primality Testing")
    p = auxilliary.generate_a_prime_number(64)
    q = auxilliary.generate_a_prime_number(64)
    IV = auxilliary.generate_a_prime_number(64)

    if p < q:
        key = p * p * q
        print(f"{bcolors.CYAN}EBC TEST")
        enc_test = ebc_encryption(text, key)
        dec_test = ebc_decryption(enc_test, p, q)  # p has to be smaller than q, otherwise it won't work for some reason
        print(f"{bcolors.CYAN}EBC Output text{bcolors.RED}")
        print(dec_test)
        check_result(text, dec_test)
        print(f"{bcolors.CYAN}CBC TEST")
        cbc_enc = cbc_encryption(text, key, IV)
        cbc_dec = cbc_decryption(cbc_enc, p, q, IV)
        print(f"{bcolors.CYAN}CBC Output text:{bcolors.RED}")
        print(cbc_dec)
        check_result(text, cbc_dec)


    elif q < p:
        key = q * q * p
        print(f"{bcolors.CYAN}\n\nEBC TEST")
        enc_test = ebc_encryption(text, key)
        dec_test = ebc_decryption(enc_test, q, p)  # q has to be smaller than p, otherwise it won't work for some reason
        print(f"{bcolors.CYAN}EBC Output text:{bcolors.RED}")
        print(dec_test)
        check_result(text, dec_test)
        print(f"{bcolors.CYAN}\n\nCBC TEST")
        cbc_enc = cbc_encryption(text, key, IV)
        cbc_dec = cbc_decryption(cbc_enc, q, p, IV)
        print(f"{bcolors.CYAN}CBC Output text:{bcolors.RED}")
        print(cbc_dec)
        check_result(text, cbc_dec)



    # EBC test
    # Proper test below
    print(f"{bcolors.ORANGE}\n\nTEST 2 - EBC{bcolors.ENDC}")
    print("EBC short file decryption:")
    with open('short_test.txt', 'r') as f:
        line = f.readline()
        with open('ebc_output.txt', 'w') as h:

            while line:
                if p < q:
                    enc = ebc_encryption(line, key)
                    dec = ebc_decryption(enc, p, q)
                elif q < p:
                    enc = ebc_encryption(line, key)
                    dec = ebc_decryption(enc, q, p)
                line = f.readline()
                h.write(dec)
                # print(line)

    if filecmp.cmp("short_test.txt", "ebc_output.txt"):
        print(f"{bcolors.GREEN}File was decrypted correctly{bcolors.ENDC}")
    else:
        print(f"{bcolors.RED}There was a problem with file decryption{bcolors.ENDC}")

    # CBC test
    print(f"{bcolors.ORANGE}\n\nTest 3 - CBC {bcolors.ENDC}")
    print("CBC short file decryption:")
    with open('short_test.txt', 'r') as f:
        line = f.readline()
        with open('cbc_output.txt', 'w') as h:

            while line:
                if p < q:
                    enc = cbc_encryption(line, key, IV)
                    dec = cbc_decryption(enc, p, q, IV)
                elif q < p:
                    enc = cbc_encryption(line, key, IV)
                    dec = cbc_decryption(enc, q, p, IV)
                line = f.readline()
                h.write(dec)
                # print(line)

    if filecmp.cmp("short_test.txt", "cbc_output.txt"):
        print(f"{bcolors.GREEN}File was decrypted correctly{bcolors.ENDC}")
    else:
        print(f"{bcolors.RED}There was a problem with file decryption{bcolors.ENDC}")


    # EBC test
    # Proper test below
    print(f"{bcolors.ORANGE}\n\nTest 4 - EBC {bcolors.ENDC}")

    print(f"{bcolors.CYAN}\nThe program will attempt to encrypt and decrypt long file called: TheVoyageofBeagle.txt")
    print(f"It might take few seconds, please DO NOT turn off the program{bcolors.ENDC}")

    print(f"{bcolors.CYAN}\nEBC operation starts now:{bcolors.ENDC}")
    with open('TheVoyageofBeagle.txt', 'r') as f:
        line = f.readline()
        with open('ebc_Voyage.txt', 'w') as h:

            while line:
                if p < q:
                    enc = ebc_encryption(line, key)
                    dec = ebc_decryption(enc, p, q)
                elif q < p:
                    enc = ebc_encryption(line, key)
                    dec = ebc_decryption(enc, q, p)
                line = f.readline()
                h.write(dec)
                # print(line)

    print(f"{bcolors.CYAN}Comparing files{bcolors.ENDC}")
    if filecmp.cmp("TheVoyageofBeagle.txt", "ebc_Voyage.txt"):
        print(f"{bcolors.GREEN}File was decrypted correctly{bcolors.ENDC}")
    else:
        print(f"{bcolors.RED}There was a problem with file decryption{bcolors.ENDC}")

    # CBC test
    print(f"{bcolors.ORANGE}\n\nTest 5 - CBC {bcolors.ENDC}")
    print(f"{bcolors.CYAN}CBC operation starts now:{bcolors.ENDC}")
    with open('TheVoyageofBeagle.txt', 'r') as f:
        line = f.readline()
        with open('cbc_Voyage.txt', 'w') as h:

            while line:
                if p < q:
                    enc = cbc_encryption(line, key, IV)
                    dec = cbc_decryption(enc, p, q, IV)
                elif q < p:
                    enc = cbc_encryption(line, key, IV)
                    dec = cbc_decryption(enc, q, p, IV)
                line = f.readline()
                h.write(dec)
                # print(line)

    print(f"{bcolors.CYAN}Comparing files{bcolors.ENDC}")
    if filecmp.cmp("TheVoyageofBeagle.txt", "cbc_Voyage.txt"):
        print(f"{bcolors.GREEN}File was decrypted correctly{bcolors.ENDC}")
    else:
        print(f"{bcolors.RED}There was a problem with file decryption{bcolors.ENDC}")


def check_result(enc, dec):
    if enc == dec:
        print(f"{bcolors.GREEN}Message was decrypted correctly{bcolors.ENDC}")
    else:
        print(f"{bcolors.RED}There was a problem with message decryption{bcolors.ENDC}")