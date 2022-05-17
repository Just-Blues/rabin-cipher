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
        #print("P mod 4, r= ", r)
    elif p % 8 == 5:
        r = auxilliary.sqrt_p_5_mod_8(ciphered_msg, p)
        #print("P mod 8, r= ", r)
    # for q
    if q % 4 == 3:
        s = auxilliary.sqrt_p_3_mod_4(ciphered_msg, q)
        #print("Q mod 4, s= ", s)
    elif q % 8 == 5:
        s = auxilliary.sqrt_p_5_mod_8(ciphered_msg, q)
        #print("Q mod 8, s= ", s)

    gcd, c, d = auxilliary.egcd(p, q)
    #print(gcd, c, d)
    x = (r * d * q + s * c * p) % n
    y = (r * d * q - s * c * p) % n
    lst = [x, n - x, y, n - y]
    print(lst)

    i = 0
    aux = 0
    plaintext = 0
    #Find the correct answer from lst
    while i < 4:
        aux = lst[i]**2 % (n*p) #n = p^2 * q ?????
        if aux == ciphered_msg:
            print(i,aux, "==", ciphered_msg)
            plaintext = lst[i]
        i += 1
    
    #plaintext = lst[i]
    #print(plaintext)

    return plaintext


def decryption_cbc_verification(ciphered_msg, p, q, previous):
    n = p * q
    r, s = 0, 0
    # find sqrt
    # for p
    if p % 4 == 3:
        r = auxilliary.sqrt_p_3_mod_4(ciphered_msg, p)
        #print("P mod 4, r= ", r)
    elif p % 8 == 5:
        r = auxilliary.sqrt_p_5_mod_8(ciphered_msg, p)
        #print("P mod 8, r= ", r)
    # for q
    if q % 4 == 3:
        s = auxilliary.sqrt_p_3_mod_4(ciphered_msg, q)
        #print("Q mod 4, s= ", s)
    elif q % 8 == 5:
        s = auxilliary.sqrt_p_5_mod_8(ciphered_msg, q)
        #print("Q mod 8, s= ", s)

    gcd, c, d = auxilliary.egcd(p, q)
    #print(gcd, c, d)
    x = (r * d * q + s * c * p) % n
    y = (r * d * q - s * c * p) % n
    lst = [x, n - x, y, n - y]
    #lst[0] = lst[0] ^ previous
    #lst[1] = lst[1] ^ previous
    #lst[2] = lst[2] ^ previous
    #lst[3] = lst[3] ^ previous
    print(lst)

    i = 0
    aux = 0
    plaintext = 0
    #Find the correct answer from lst
    while i < 4:
        aux = lst[i]**2 % (n*p) #n = p^2 * q ?????
        #aux = aux ^ previous
        if aux == ciphered_msg^previous:
            print(i,aux, "==", ciphered_msg)
            plaintext = lst[i]
        i += 1
    
    #plaintext = lst[i]
    #print(plaintext)

    return plaintext


#Changes string to 32-bits blocks
def str_to_int(plaintext,radix):
    result = []
    a = 0
    j = len(plaintext)
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
def int_to_str(number,radix):
    plaintext = ""
    for i in range(0, len(number)):
        #binary_str = bin(number[i])
        while number[i] != 0:
            a = int(number[i] % radix)
            plaintext += chr(a)
            number[i] = (number[i] - a) / radix

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
            aux = plaintext[0] ^ initializing_vector
        else:
            aux = plaintext[i] ^ encrypted[i-1]  
        encrypted.append(encryption(aux,n))

    return encrypted

def cbc_decryption(ciphered_msg, p, q, initializing_vector):
    decrypted = []
    for i in range(0, len(ciphered_msg)):
        if i == 0:
            aux = decryption(ciphered_msg[0],p,q) ^ initializing_vector
        else:
            aux = decryption(ciphered_msg[i],p,q) ^ ciphered_msg[i-1]

        decrypted.append(aux)

    return decrypted

text = "podovne do obsydianu XD"
radix = 256 #for bigger radix we need enormous key
int_text = str_to_int(text, radix)
print(int_text)

#Some enormous keys are required for the decryption to work properly
key = 50539 * 50543 * 50539
#key2 = 118249 * 118633
#large_key = 1000081 * 1000193 * 1000081
#129096451502903 = p^2 * q -> because if it's only p*q, the verification mechanism doesn't work, hence why we use p^2 * q
#doesn't change much, becuase the key has to be factorized anyway and one of the factors is a prime number anyway
key3 = 11362979 * 11363239 * 11362979 #not so big

#enc_test = ebc_encryption(int_text,key3) #43869243335189 = 32779^2 * 40829, 1338333791 = 32779 * 40829
#print(enc_test)

#dec_test = ebc_decryption(enc_test,11362979, 11363239) #p has to be smaller than q, otherwise it won't work for some reason
#print(dec_test)

#end_text = int_to_str(dec_test, radix)
#print(end_text)

IV = 0

test1 = encryption(int_text[0]^2343827943983,key3)
test2 = encryption(int_text[1]^test1,key3)
test3 = encryption(int_text[2]^test2,key3)

#test1 = test1 ^ 0
#test2 = test2 ^ test1
#test3 = test3 ^ test2
print(test1, test2, test3)

test4 = decryption_cbc_verification(test1,11362979, 11363239, IV)
#test4 = test4 ^ 2343827943983
test5 = decryption_cbc_verification(test2,11362979, 11363239, test1) 
#test5 = test5 ^ test1
test6 = decryption_cbc_verification(test3,11362979, 11363239, test2) 
#test6 = test6 ^ test2

print(test4, test5, test6)

#cenc_test = cbc_encryption(int_text,key,IV)
#print(cenc_test)

#cdec_test = cbc_decryption(cenc_test,50539, 50543, IV)
#print(cdec_test)


#[1868853104, 543518326, 1864396644, 1685680994, 1970168169, 4479008]
#[36525370897054, 39489659200212, 52889442799461, 107515953933006, 19606803028060, 20061512664064]


#[36525370897054, 69297185668918, 2045933516730, 127811932270049, 42800105976976, 92633153595235]

