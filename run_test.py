from ebc import bcolors
from main import ebc_encryption, ebc_decryption


def run_test(p, q):
    # Proper test below
    key = p * p * q if p < q else q * q *p
    with open('test.txt', 'r') as f:
        line = f.readline()
        i = 1
        with open('output.txt', 'w') as h:
            while line:
                line = f.readline()
                if p < q:
                    enc = ebc_encryption(line, key)
                    dec = ebc_decryption(enc, p, q)
                elif q < p:
                    enc = ebc_encryption(line, key)
                    dec = ebc_decryption(enc, q, p)

                assert line == dec
                print(f"{bcolors.GREEN}TEST {i} PASSED{bcolors.ENDC}")
                i += 1
                h.write(dec)