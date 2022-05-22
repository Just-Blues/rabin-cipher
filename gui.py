import re
from sys import getsizeof

import numpy as np
import numpy.ma
from PyInquirer import prompt
from prompt_toolkit.validation import Validator, ValidationError

from ebc import encrypt, decrypt
from run_test import run_test


def isprime(num):
    for n in range(2, int(num ** 0.5) + 1):
        if num % n == 0:
            return False
    return True


class PrimeValidator(Validator):
    def validate(self, document):
        isNumInteger = re.search('^\\d+$', str(document.text))
        isInputPrimeNum = isprime(int(document.text)) if bool(isNumInteger) else False
        if not bool(isNumInteger) or not isInputPrimeNum:
            raise ValidationError(
                message='You must provide prime number',
                cursor_position=len(document.text)
            )


class InitializationVectorValidator(Validator):
    def validate(self, document):
        ok = re.match('^\\d+$', str(document.text))
        isAtLeast32Bit = getsizeof(int(document.text)) < 32 if ok else False
        if not ok or isAtLeast32Bit:
            raise ValidationError(
                message='Initalization vector must be at least 32-bit number',
                cursor_position=len(document.text)
            )

class CipherTextBlockArrayValidator(Validator):
    def validate(self, document):

        ok = True

        arr = [int(x) for x in document.text.strip().split(',')]
        if not isinstance(arr, list):
            ok = False

        for item in arr:
            if type(item) != int:
                ok = False

        if not ok:
            raise ValidationError(
                message='You need to provide only encrypted blocks of numbers separated by comma',
                cursor_position=len(document.text)
            )



def get_input_params():
    answers = prompt([
        {
            'type': 'list',
            'name': 'app_mode',
            'message': 'Choose preferred action',
            'choices': ['Encryption', 'Decryption', 'All', 'Tests']
        },
        {
            'type': 'input',
            'name': 'input_plaintext',
            'default': 'I want to break free',
            'message': 'Please enter the plaintext to be encrypted',
            'validate': lambda answer: len(answer) > 0 or 'Plaintext must not be blank',
        },
        {
            'type': 'input',
            'name': 'p',
            'default': '40000000141',
            'message': 'Enter first prime number \'p\' to generate public and private key',
            'validate': PrimeValidator
        },
        {
            'type': 'input',
            'name': 'q',
            'default': '40000001051',
            'message': 'Enter second prime number \'q\' to generate public and private key',
            'validate': PrimeValidator
        },

    ])

    return answers['app_mode'], answers['input_plaintext'], int(answers['p']), int(answers['q'])


def gui():
    app_mode, plaintext, p, q = get_input_params()

    if p == q:
        raise Exception("p and q cannot be the same")

    if app_mode == "Encryption":

        encrypt(p, q, plaintext)

    elif app_mode == "All":

        cipher_text = encrypt(p, q, plaintext)
        encrypted_msg = decrypt(p, q, cipher_text)

    elif app_mode == "Decryption":
        answers = prompt({
            'type': 'input',
            'name': 'cipher_text',
            'message': 'Please enter the ciphertext as array of encrypted blocks. Example: 1, 3, 5, 7, 11 ...',
            'default': '41485667273132496669513841680320, 42103096247763058700214192038420, 5676178460851462154952244454129, 17137915331541212580406997050118, 40231125331961273935714897292992',
            'validate': CipherTextBlockArrayValidator
        })

        arr = [int(x) for x in answers['cipher_text'].strip().split(',')]
        decrypt(p, q, arr)

    elif app_mode == "Tests":
        run_test(p, q)


gui()
