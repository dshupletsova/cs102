import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    chiphertext = ""
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


def decrypt_caesar(chiphertext: str, shift: int = 3) -> str:
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


def caesar_breaker_brute_force(chiphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    return best_shift
