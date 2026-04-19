from django.test import TestCase

from .services.cipher import caesar_cipher


class CaesarCipherTests(TestCase):
    def test_caesar_cipher_shifts_letters_by_15(self):
        self.assertEqual(caesar_cipher("Attack at Dawn! Zebra-123", 15), "Piiprz pi Splc! Otqgp-123")
