from pathlib import Path
from tempfile import TemporaryDirectory

from django.test import SimpleTestCase

from .services.hashing import generate_file_sha256, verify_file_integrity
from .services.cipher import caesar_cipher


class CaesarCipherTests(SimpleTestCase):
    def test_caesar_cipher_shifts_letters_by_15(self):
        self.assertEqual(
            caesar_cipher("Attack at Dawn! Zebra-123", 15),
            "Piiprz pi Splc! Otqgp-123",
        )

    def test_caesar_cipher_reverses_shift_by_15(self):
        self.assertEqual(
            caesar_cipher("Piiprz pi Splc! Otqgp-123", -15),
            "Attack at Dawn! Zebra-123",
        )


class FileHashingTests(SimpleTestCase):
    def test_generate_file_sha256_hashes_file_bytes(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "payload.bin"
            file_path.write_bytes(b"abc")

            self.assertEqual(
                generate_file_sha256(str(file_path)),
                "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
            )

    def test_verify_file_integrity_compares_file_hash(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "payload.bin"
            file_path.write_bytes(b"abc")

            result = verify_file_integrity(
                str(file_path),
                "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
            )

            self.assertTrue(result["is_match"])
