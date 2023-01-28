import unittest

from dominio.algoritmos.sha1.sha1_clase import SHA1
from helpers.utilidades import bytes_de_string


class TestAlgoritmoSHA1(unittest.TestCase):
    def test_sha1(self):
        expectations = {
            "": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
            "a": "86f7e437faa5a7fce15d1ddcb9eaeaea377667b8",
            "abc": "a9993e364706816aba3e25717850c26c9cd0d89d",
            "message digest": "c12252ceda8be8994d5fa0290a47231c1d16aae3",
            "abcdefghijklmnopqrstuvwxyz": "32d10c7b8cf96570ca04ce37f2a19d84240d3a89",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789": "761c457bf73b14d27e9e9265c46f4b4dda11f940",
            "12345678901234567890123456789012345678901234567890123456789012345678901234567890": "50abf5706a150990a08b2c5ea40fa0e585554732",
        }

        for string, hash_sha1 in expectations.items():
            with self.subTest(string=string, hash_sha1=hash_sha1):
                hasher = SHA1()
                hasher.update(bytes_de_string(string))
                self.assertEqual(hasher.hexdigest(), hash_sha1)


