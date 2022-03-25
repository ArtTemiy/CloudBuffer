import random

ALPHABET = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')


class TokenGenerator:
    def __init__(self):
        self.genned_codes = set()

    def gen_code(self, size=64):
        new_code = self._gen_code_once(size)
        while new_code in self.genned_codes:
            new_code = self._gen_code_once(size)

        self.genned_codes.add(new_code)
        return new_code

    def remove_code(self, code):
        if code in self.genned_codes:
            self.genned_codes.remove(code)

    @staticmethod
    def _gen_code_once(self, size=64):
        return ''.join(random.choices(ALPHABET, k=size))


token_generator = TokenGenerator()
