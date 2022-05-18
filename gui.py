import re
from sys import getsizeof

from PyInquirer import prompt
from prompt_toolkit.validation import Validator, ValidationError

from ebc import run_ebc
from main import str_to_int


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


class InitializationVector(Validator):
    def validate(self, document):
        ok = re.match('^\\d+$', str(document.text))
        isAtLeast32Bit = getsizeof(int(document.text)) < 32 if ok else False
        if not ok or isAtLeast32Bit:
            raise ValidationError(
                message='Initalization vector must be at least 32-bit number',
                cursor_position=len(document.text)
            )


  #TODO
# class MessageValidator(Validator):
#     def validate(self, document):
#         message_to_int_blocks = str_to_int(document.text)
#         for m

def get_input_params():
    answers = prompt([
        {
            'type': 'input',
            'name': 'input_plaintext',
            'default': 'I want to break free',
            'message': 'Please enter the plaintext to be encrypted',
            'validate': lambda answer: len(answer) > 0 or 'Plaintext must not be blank'
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

    return answers['input_plaintext'], int(answers['p']), int(answers['q'])


def gui():
    plaintext, p, q = get_input_params()

    run_ebc(p, q, plaintext)



gui()
