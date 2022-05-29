import re
from sys import getsizeof

from PyInquirer import prompt
from prompt_toolkit.validation import Validator, ValidationError

from auxilliary import isPrime
from cbc import encrypt_cbc, decrypt_cbc
from ebc import encrypt_ebc, decrypt_ebc
from run_test import run_test


class PrimeValidator(Validator):
    def validate(self, document):
        isNumInteger = re.search('^\\d+$', str(document.text))
        isInputPrimeNum = isPrime(int(document.text)) if bool(isNumInteger) else False
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


def get_input_params(app_mode):
    answers = prompt([
        {
            'type': 'list',
            'name': 'mode',
            'message': 'Choose mode of the rabin cipher',
            'choices': ['EBC', 'CBC'],
            'when': lambda answer: app_mode != 'Tests'
        },
        {
            'type': 'input',
            'name': 'input_plaintext',
            'default': 'I want to break free',
            'message': 'Please enter the plaintext to be encrypted',
            'validate': lambda answer: len(answer) > 0 or 'Plaintext must not be blank',
            'when': lambda answer: app_mode != 'Tests'
        },
        {
            'type': 'input',
            'name': 'p',
            'default': '17518782197258984731',
            'message': 'Enter first prime number \'p\' to generate public and private key',
            'validate': PrimeValidator,
            'when': lambda answer: app_mode != 'Tests'
        },
        {
            'type': 'input',
            'name': 'q',
            'default': '3172620527333942071',
            'message': 'Enter second prime number \'q\' to generate public and private key',
            'validate': PrimeValidator,
            'when': lambda answer: app_mode != 'Tests'
        },

    ])

    return answers['mode'], answers['input_plaintext'], int(answers['p']), int(answers['q'])


def get_app_mode():
    answer = prompt({
        'type': 'list',
        'name': 'app_mode',
        'message': 'Choose preferred action',
        'choices': ['Encryption', 'Decryption', 'All', 'Tests']
    })
    return answer['app_mode']


def gui():
    app_mode = get_app_mode()

    if app_mode == "Tests":
        run_test()
        return

    cipher_mode, plaintext, p, q = get_input_params(app_mode)

    if p == q:
        raise Exception("p and q cannot be the same")

    vector_question = prompt({
        'type': 'input',
        'name': 'initializing_vector',
        'default': '920441868394157507',
        'message': 'Enter initializing vector \'IV\' for CBC mode',
        'validate': PrimeValidator
    })

    if app_mode == "Encryption":

        if cipher_mode == 'EBC':
            encrypt_ebc(p, q, plaintext)
        elif cipher_mode == 'CBC':
            encrypt_cbc(p, q, plaintext, int(vector_question['initializing_vector']))

    elif app_mode == "All":

        if cipher_mode == 'EBC':
            print("EBC")
            cipher_text = encrypt_ebc(p, q, plaintext)
            encrypted_msg = decrypt_ebc(p, q, cipher_text)
        elif cipher_mode == 'CBC':
            print("CBC")
            cipher_text = encrypt_cbc(p, q, plaintext, int(vector_question['initializing_vector']))
            encrypted_msg = decrypt_cbc(p, q, cipher_text, int(vector_question['initializing_vector']))

    elif app_mode == "Decryption":
        print(1)
        if cipher_mode == 'EBC':

            answers = prompt({
                'type': 'input',
                'name': 'cipher_text',
                'message': 'Please enter the ciphertext as array of encrypted blocks. Example: 1, 3, 5, 7, 11 ...',
                'default': '745485690733932635825234071524561, 1066103130372563261108534526357316, 1029676212585651664563272578773025, 81137917464341225230927017945049, 808231150925561425741955148032164',
                'validate': CipherTextBlockArrayValidator
            })
            arr = [int(x) for x in answers['cipher_text'].strip().split(',')]
            decrypt_ebc(p, q, arr)

        elif cipher_mode == 'CBC':
            answers = prompt({
                'type': 'input',
                'name': 'cipher_text',
                'message': 'Please enter the ciphertext as array of encrypted blocks. Example: 1, 3, 5, 7, 11 ...',
                'default': '831227259404327193279348641169600100, 1045529968525375526012071574453563659396370569316, 991996860635384581504254207361522559957239664761, 309142744290595779935423381016999201867053630224, 324917755166148243682939354559149132472000576100',
                'validate': CipherTextBlockArrayValidator
            })
            arr = [int(x) for x in answers['cipher_text'].strip().split(',')]
            decrypt_cbc(p, q, arr)


gui()
