import random

from CloudBuffer.settings import MEDIA_ROOT

ALPHABET = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')


gened_codes = set()


def gen_code(size=64):
    return ''.join(random.choices(ALPHABET, k=size))


def gen_code_unique(size=64):
    new_code = gen_code(size)
    while new_code in gened_codes:
        new_code = gen_code(size)

    gened_codes.add(new_code)
    return new_code


def get_file_path(account, token):
    file_name = f'{account.user.username}__{token}'
    return f'{MEDIA_ROOT}/{file_name}'
