def caesar_cipher(text: str, shift: int) -> str:
    shifted = []

    for char in text:
        if char.isalpha():
            base = ord("A") if char.isupper() else ord("a")
            shifted.append(chr((ord(char) - base + shift) % 26 + base))
        else:
            shifted.append(char)

    return "".join(shifted)
