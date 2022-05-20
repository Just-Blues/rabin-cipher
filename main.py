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

#Some enormous keys are required for the decryption to work properly
#p^2 * q -> because if it's only p*q, the verification mechanism doesn't work, hence why we use p^2 * q
#doesn't change much, becuase if the cipher were to deciphered the key would have to be factorized anyway

text = "random string, test|EjLmQ6yxCJ, V4nA4RUJxe ą 52G8AiCnv2 osSq4PGlJi  DAoMc7bIj3 BjYV0ewIf1sadxz///522u30LrCk ę "
print("Input text: \n", text)

p = auxilliary.generate_a_prime_number(128)#Number of bits should be larger than 
q = auxilliary.generate_a_prime_number(128)

#print(p)
#print(q)

if p < q:
    key = p*p*q
    enc_test = ebc_encryption(text,key)
    #print(enc_test)
    dec_test = ebc_decryption(enc_test, p, q) #p has to be smaller than q, otherwise it won't work for some reason
    print("Output text: \n",dec_test)
    #print(dec_test)

elif q < p:
    key = q*q*p
    enc_test = ebc_encryption(text,key)
    #print(enc_test)
    dec_test = ebc_decryption(enc_test, q, p) #q has to be smaller than p, otherwise it won't work for some reason
    print("Output text: \n",dec_test)
    #print(dec_test)


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


