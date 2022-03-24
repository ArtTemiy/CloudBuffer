import random


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
