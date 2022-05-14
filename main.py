# Rabin.py
import auxilliary

# encryption function
def encryption(plaintext, n):
    # c = m^2 mod n
    return plaintext ** 2 % n


# decryption function
def decryption(ciphered_msg, p, q):
    n = p * q
    r, s = 0, 0
    # find sqrt
    # for p
    if p % 4 == 3:
        r = auxilliary.sqrt_p_3_mod_4(ciphered_msg, p)
    elif p % 8 == 5:
        r = auxilliary.sqrt_p_5_mod_8(ciphered_msg, p)
    # for q
    if q % 4 == 3:
        s = auxilliary.sqrt_p_3_mod_4(ciphered_msg, q)
    elif q % 8 == 5:
        s = auxilliary.sqrt_p_5_mod_8(ciphered_msg, q)

    gcd, c, d = auxilliary.egcd(p, q)
    x = (r * d * q + s * c * p) % n
    y = (r * d * q - s * c * p) % n
    lst = [x, n - x, y, n - y]
    #print(lst)

    i = 0
    aux = 0

    #Find the correct answer from lst
    while aux != ciphered_msg and i < 4:
        aux = lst[i]**2 % (n*p)
        i += 1
    
    i -= 1
    plaintext = lst[i]
    #print(plaintext)


    return plaintext

#Changes string to 32-bits blocks
def str_to_int(plaintext):
    result = []
    a = 0
    j = len(plaintext)
    radix = 256
    #Padding
    if j % 4 != 0:
        plaintext += "\0"*(4 - j%4)

    for i in range(0, j):
        #size of each block is 32 bits
        if i % 4 == 0: 
            a = ord(plaintext[i]) + ord(plaintext[i+1]) * radix + ord(plaintext[i+2])* radix**2 + ord(plaintext[i+3])* radix**3
            result.append(a)

    return result

#Translates 32 bit integares into string of 4 chars
def int_to_str(number):
    plaintext = ""
    for i in range(0, len(number)):
        #binary_str = bin(number[i])
        while number[i] != 0:
            a = int(number[i] % 256)
            plaintext += chr(a)
            number[i] = (number[i] - a) / 256

    return plaintext


def ebc_encryption(plaintext, n):
    encrypted = []
    for i in range(0,len(plaintext)):
        encrypted.append(encryption(plaintext[i],n))    

    return encrypted

def ebc_decryption(ciphered_msg, p, q):
    decrypted = []
    for i in range(0, len(ciphered_msg)):
        #print("Iteration: ", i)
        decrypted.append(decryption(ciphered_msg[i], p, q))

    return decrypted

#Initializing_vector will be 32-bits, all vectors after the first will have to be padded or extended
def cbc_encryption(plaintext, n ,initializing_vector):
    encrypted = []
    for i in range(0, len(plaintext)):
        if i == 0:
            aux = plaintext[i] ^ initializing_vector
        else:
            aux = encrypted[i-1] ^ plaintext[i]

        encrypted.append(encryption(aux,n))

    return encrypted

def cbc_decryption(ciphered_msg, p, q, initializing_vector):
    decrypted = []
    for i in range(0, len(ciphered_msg)):
        if i == 0:
            aux = decryption(ciphered_msg[i],p,q) ^ initializing_vector
        else:
            aux = decryption(ciphered_msg[i],p,q) ^ ciphered_msg[i-1]

        decrypted.append(aux)



    return decrypted

text = "mdld68T 5l5 D0Xi1| 0hg"
int_text = str_to_int(text)
print(int_text)

#Some enormous keys are required for the decryption to work properly
enc_test = ebc_encryption(int_text, 129096451502903) #43869243335189 = 32779^2 * 40829, 1338333791 = 32779 * 40829
print(enc_test)

dec_test = ebc_decryption(enc_test,50539,50543)
print(dec_test)

end_text = int_to_str(dec_test)

print(end_text)

#większy radix i większy klucz, ogarnij n = p*q, aktaulnie jest n = p^2 * q
