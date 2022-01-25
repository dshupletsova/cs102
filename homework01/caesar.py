import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    ciphertext = ""
    for letter in plaintext:
        if letter.isalpha():
            if letter.islower():
                letter = chr(ord(letter) + shift)
                if ord(letter) > ord("z"):
                    letter = chr(ord(letter) - 26)
            else:
                letter = chr(ord(letter) + shift)
                if ord(letter) > ord("Z"):
                    letter = chr(ord(letter) - 26)
        ciphertext += letter
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    plaintext = ""
    for letter in ciphertext:
        if letter.isalpha():
            if letter.islower():
                letter = chr(ord(letter) - shift)
                if ord(letter) < ord("a"):
                    letter = chr(ord(letter) + 26)
            else:
                letter = chr(ord(letter) - shift)
                if ord(letter) < ord("A"):
                    letter = chr(ord(letter) + 26)
        plaintext += letter
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    best_shift = 0
    return best_shift
