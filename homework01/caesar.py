import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    chiphertext = ""
    for i, _ in enumerate(plaintext):
        if plaintext[i].isalpha():
            a_a = ord(plaintext[i])
            if plaintext[i].isupper() and a_a >= 91 - shift:
                chiphertext += chr(a_a - 26 + shift)
            elif plaintext[i].islower() and a_a >= 123 - shift:
                chiphertext += chr(a_a - 26 + shift)
            else:
                chiphertext += chr(a_a + shift)
        else:
            chiphertext += plaintext[i]
    return chiphertext


def decrypt_caesar(chiphertext: str, shift: int = 3) -> str:
    """
    Decrypts a chiphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for i, _ in enumerate(chiphertext):
        if chiphertext[i].isalpha():
            a_a = ord(chiphertext[i])
            if chiphertext[i].isupper() and a_a <= 64 + shift:
                plaintext += chr(a_a + 26 - shift)
            elif chiphertext[i].islower() and a_a <= 96 + shift:
                plaintext += chr(a_a + 26 - shift)
            else:
                plaintext += chr(a_a - shift)
        elif chiphertext.isspace():
            continue
        else:
            plaintext += chiphertext[i]
    return plaintext


def caesar_breaker_brute_force(chiphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    return best_shift
