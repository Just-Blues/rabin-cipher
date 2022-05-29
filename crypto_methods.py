import auxilliary
import filecmp

# Find SQROOT in Zp where p = 3 mod 4
def sqrt_p_3_mod_4(a, p):
    r = pow(a, (p + 1) // 4, p)
    return r

# encryption function
def encryption(plaintext, n):
    # c = m^2 mod n
    cipher = plaintext ** 2 % n
    return cipher

# decryption function
def decryption(ciphered_msg, p, q):
    n = p * q
    r, s = 0, 0
    # find sqrt
    # for p
    if p % 4 == 3:
        r = sqrt_p_3_mod_4(ciphered_msg, p)
    else:
        print("p mod 4 != 3")
    # for q
    if q % 4 == 3:
        s = sqrt_p_3_mod_4(ciphered_msg, q)
    else:
        print("q mod 4 != 3")

    gcd, c, d = auxilliary.egcd(p, q)

    x = (r * d * q + s * c * p) % n
    y = (r * d * q - s * c * p) % n
    lst = [x, n - x, y, n - y]

    i = 0
    plaintext = 0
    #Find the correct answer from lst
    while i < 4:
        aux = lst[i]**2 % (n*p) #n = p^2 * q ?????
        if aux == ciphered_msg:
            plaintext = lst[i]
        i += 1
    
    return plaintext

#Changes string to 64-bits blocks (depends on radix)
def str_to_int(plaintext):
    result = []
    a = 0
    j = len(plaintext)
    #Padding
    if j % 4 != 0:
        plaintext += "\0"*(4 - j%4)

    for i in range(0, j):
        #size of each block is 32/64 bits 
        if i % 4 == 0: 
            a = ord(plaintext[i]) + ord(plaintext[i+1]) * 65536 + ord(plaintext[i+2])* 65536**2 + ord(plaintext[i+3])* 65536**3
            result.append(a)

    return result

#Translates 64-bit integares into string of 4 chars
def int_to_str(number):
    plaintext = ""
    for i in range(0, len(number)):
        while number[i] != 0:
            a = int(number[i] % 65536)
            plaintext += chr(a)
            number[i] = (number[i] - a) / 65536

    return plaintext
