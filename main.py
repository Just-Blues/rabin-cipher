import auxilliary

# Find SQROOT in Zp where p = 3 mod 4
def sqrt_p_3_mod_4(a, p):
    r = pow(a, (p + 1) // 4, p)
    return r

# Find SQROOT in Zp where p = 5 mod 8
def sqrt_p_5_mod_8(a, p):
    d = pow(a, (p - 1) // 4, p)
    r =0
    if d == 1:
        r = pow(a, (p + 3) // 8, p)
    elif d == p - 1:
        r = 2 * a * pow(4 * a, (p - 5) // 8, p) % p

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
        #print("P mod 4, r= ", r)
    else:
        print("p mod 4 != 3")
    # for q
    if q % 4 == 3:
        s = sqrt_p_3_mod_4(ciphered_msg, q)
        #print("Q mod 4, s= ", s)
    else:
        print("q mod 4 != 3")

    gcd, c, d = auxilliary.egcd(p, q)
    #print(gcd, c, d)
    x = (r * d * q + s * c * p) % n
    y = (r * d * q - s * c * p) % n
    lst = [x, n - x, y, n - y]
    #print(lst)

    i = 0
    aux = 0
    plaintext = 0
    #Find the correct answer from lst
    while i < 4:
        aux = lst[i]**2 % (n*p) #n = p^2 * q ?????
        if aux == ciphered_msg:
            #print(i,aux, "==", ciphered_msg)
            plaintext = lst[i]
        i += 1
    
    #plaintext = lst[i]
    #print(plaintext)

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
        #binary_str = bin(number[i])
        while number[i] != 0:
            a = int(number[i] % 65536)
            plaintext += chr(a)
            number[i] = (number[i] - a) / 65536

    return plaintext

def ebc_encryption(plaintext, n):
    int_plaintext = str_to_int(plaintext)
    encrypted = []
    for i in range(0,len(int_plaintext)):
        encrypted.append(encryption(int_plaintext[i],n))    

    return encrypted

def ebc_decryption(ciphered_msg, p, q):
    decrypted = []
    for i in range(0, len(ciphered_msg)):
        #print("Iteration: ", i)
        decrypted.append(decryption(ciphered_msg[i], p, q))
    
    str_decrypted = int_to_str(decrypted)
    
    return str_decrypted


def decryption_cbc_verification(ciphered_msg, p, q, previous):
    n = p * q
    r, s = 0, 0
    # find sqrt
    # for p
    if p % 4 == 3:
        r = sqrt_p_3_mod_4(ciphered_msg, p)
        #print("P mod 4, r= ", r)
    else:
        print("p mod 4 != 3")
    # for q
    if q % 4 == 3:
        s = sqrt_p_3_mod_4(ciphered_msg, q)
        #print("Q mod 4, s= ", s)
    else:
        print("q mod 4 != 3")

    gcd, c, d = auxilliary.egcd(p, q)
    #print(gcd, c, d)
    x = (r * d * q + s * c * p) % n
    y = (r * d * q - s * c * p) % n
    lst = [x, n - x, y, n - y]
    #print(lst)
    print("Bit lenght of lst: ", lst[0].bit_length(), lst[1].bit_length(), lst[2].bit_length(),lst[3].bit_length())

    #lst[0] = lst[0] ^ previous
    #lst[1] = lst[1] ^ previous
    #lst[2] = lst[2] ^ previous
    #lst[3] = lst[3] ^ previous
    #print(lst)

    i = 0
    aux = 0
    plaintext = 0
    #Find the correct answer from lst
    while i < 4:
        aux = lst[i]**2 % (n*p) #n = p^2 * q ?????
        #aux = aux ^ previous
        #print(aux)
        if aux == ciphered_msg:
            print("FOUND!",i,)#aux, "==", ciphered_msg)
            plaintext = lst[i]
        i += 1
    
    #plaintext = lst[i]
    #print(plaintext)

    return plaintext^previous


#Some enormous keys are required for the decryption to work properly
#p^2 * q -> because if it's only p*q, the verification mechanism doesn't work, hence why we use p^2 * q
#doesn't change much, becuase if the cipher were to deciphered the key would have to be factorized anyway

text = "ź{}random string, test|EjLmQ6yxCJ, V4nA4RUJxe ą 52G8AiCnv2 osSq4PGlJi  DAoMc7bIj3 BjYV0ewIf1sadxz///522u30LrCk ę "
print("Input text: \n", text)

p = auxilliary.generate_a_prime_number(32)
q = auxilliary.generate_a_prime_number(32)

print(p)
print(q)

if p < q:
    key = p*p*q
    #print(key.bit_length())
    enc_test = ebc_encryption(text,key)
    #print(enc_test)
    #print("Original text: ", enc_test[0].bit_length(), enc_test[1].bit_length(),enc_test[3].bit_length(),enc_test[5].bit_length(),enc_test[2].bit_length(),enc_test[9].bit_length())
    dec_test = ebc_decryption(enc_test, p, q) #p has to be smaller than q, otherwise it won't work for some reason
    print("Output text: \n",dec_test)
    #print(dec_test)

elif q < p:
    key = q*q*p
    #print(key.bit_length())
    enc_test = ebc_encryption(text,key)
    #print(enc_test)
    #print("Original text: ", enc_test[0].bit_length(), enc_test[1].bit_length(),enc_test[3].bit_length(),enc_test[5].bit_length(),enc_test[2].bit_length(),enc_test[9].bit_length())
    dec_test = ebc_decryption(enc_test, q, p) #q has to be smaller than p, otherwise it won't work for some reason
    print("Output text: \n",dec_test)
    #print(dec_test)

#test_int = str_to_int(text)
#print(test_int)


test_q = 4101667043
test_p = 3281508959
IV = auxilliary.generate_a_prime_number(55)
#print(IV)

test_key = test_p * test_p * test_q
print("Key lenght = ", test_key.bit_length())
test_int = str_to_int(text)
print(test_int)
cipher = []
print("Original text: ", test_int[0].bit_length(), test_int[1].bit_length(),test_int[2].bit_length(),test_int[3].bit_length(),test_int[4].bit_length(),test_int[5].bit_length())
cipher.append(encryption(test_int[0]^ IV, test_key))
cipher.append(encryption(test_int[1]^ cipher[0], test_key))
cipher.append(encryption(test_int[2]^ cipher[1], test_key))
cipher.append(encryption(test_int[3]^ cipher[2], test_key))
cipher.append(encryption(test_int[4]^ cipher[3], test_key))
cipher.append(encryption(test_int[5]^ cipher[4], test_key))

print("Ciphers: \n",cipher[0].bit_length(), cipher[1].bit_length(), cipher[2].bit_length(), cipher[3].bit_length(),cipher[4].bit_length(), cipher[5].bit_length(),"\n\n")
print("Cipher in binary: ", bin(cipher[0]))
print(bin(cipher[1]))
print(bin(cipher[2]))
print(bin(cipher[3]))
print(bin(cipher[4]))
print(bin(cipher[5]))

output = []
output.append(decryption_cbc_verification(cipher[0],test_p, test_q, IV))
output.append(decryption_cbc_verification(cipher[1],test_p, test_q, cipher[0]))
output.append(decryption_cbc_verification(cipher[2],test_p, test_q, cipher[1])) 
output.append(decryption_cbc_verification(cipher[3],test_p, test_q, cipher[2])) 
output.append(decryption_cbc_verification(cipher[4],test_p, test_q, cipher[3])) 
output.append(decryption_cbc_verification(cipher[5],test_p, test_q, cipher[4])) 
print("Decrypted: \n", output[0].bit_length(), output[1].bit_length(), output[2].bit_length(), output[3].bit_length(),output[4].bit_length(), output[5].bit_length(),"\n\n")
print("Decrypted in binary: ", bin(output[0]))
print(bin(output[1]))
print(bin(output[2]))
print(bin(output[3]))
print(bin(output[4]))
print(bin(output[5]))

'''
#Proper test below
with open('test.txt','r') as f:
    line = f.readline()
    with open('output.txt','w') as h:

        while line:
            if p < q:
                enc = ebc_encryption(line, key)
                dec = ebc_decryption(enc, p,q)
            elif q < p:
                enc = ebc_encryption(line, key)
                dec = ebc_decryption(enc, q,p)
            line = f.readline()
            h.write(dec)
            #print(line)


'''

'''
#Initializing_vector will be 32/64-bits, all vectors after the first will have to be padded or extended (that was the plan, now I don't know)
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

'''