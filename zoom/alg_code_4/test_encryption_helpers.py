import unittest
from encryption_helpers import encrypt_string, decrypt_string, encrypt_character, decrypt_character

class TestEncryptionHelpers(unittest.TestCase):
    def setUp(self):
        self.source = 'abcdefghijklmnopqrstuvwxyz'
        self.slug = 'bcdefghijklmnopqrstuvwxyza'

    def test_encrypt_character(self):
        self.assertEqual(encrypt_character('a', self.source, self.slug), 'b')
        self.assertEqual(encrypt_character('z', self.source, self.slug), 'a')
        self.assertEqual(encrypt_character('!', self.source, self.slug), '!')

    def test_decrypt_character(self):
        self.assertEqual(decrypt_character('b', self.source, self.slug), 'a')
        self.assertEqual(decrypt_character('a', self.source, self.slug), 'z')
        self.assertEqual(decrypt_character('!', self.source, self.slug), '!')

    def test_encrypt_string(self):
        self.assertEqual(encrypt_string('abc', self.source, self.slug), 'bcd')
        self.assertEqual(encrypt_string('xyz', self.source, self.slug), 'yza')

    def test_decrypt_string(self):
        self.assertEqual(decrypt_string('bcd', self.source, self.slug), 'abc')
        self.assertEqual(decrypt_string('yza', self.source, self.slug), 'xyz')

if __name__ == '__main__':
    unittest.main()
