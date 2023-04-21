import unittest

from dominio.algoritmos.sha256.sha256_clase import SHA256
from helpers.operaciones_bit_a_bit import bitarray_de_string

test_vector_1 = bitarray_de_string("")
test_vector_2 = bitarray_de_string("abc")
test_vector_3 = bitarray_de_string("abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq")
test_vector_4 = bitarray_de_string(
    "abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu")
test_vector_5 = bitarray_de_string("a" * 1000000)
test_vector_6 = bitarray_de_string("abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopqp")
test_vector_7 = bitarray_de_string("abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopqpqpmomom")
test_vector_8 = bitarray_de_string(
    "ibsnqwpzhillptcinmtvamymvixjxaumjddwxsxxjhjhnftynajhsluuctgjytazlcdewsexbjcpumdcfbbbmzwxcmjmnxfqurvaarapdswyatlyvqsxdefmehicwwdnkshzgysaxxenmtpirbhphxyaesgwigdxzqpekouenexqkqgpnzzwyjppc")
sha_1 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
sha_2 = 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'
sha_3 = "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1"
sha_4 = "cf5b16a778af8380036ce59e7b0492370b249b11e8f07a51afac45037afee9d1"
sha_5 = "cdc76e5c9914fb9281a1c7e284d73e67f1809a48a497200e046d39ccc7112cd0"
sha_6 = "3234a5b08b1112a6cb90bf9920ca1863535c9380a65633e5442befda64f84a6f"
sha_7 = "19c638400f16d98b8d955a0bfe853cb11c33a987389ac2311b9c0ba2cd1efa34"
sha_8 = '6540979c2b56a3f4b17dada9a3d1fba7161d0e10f2c2d87b0b6486377bf88ecc'


class TESTS(unittest.TestCase):
    # hash

    def test_sha256(self):
        """tests if sha256 hashes correctly"""
        r_1 = self.sha256_a(test_vector_1)
        r_2 = self.sha256_a(test_vector_2)
        r_3 = self.sha256_a(test_vector_3)
        r_4 = self.sha256_a(test_vector_4)
        # r_5 = self.sha256_a(test_vector_5)
        r_6 = self.sha256_a(test_vector_6)
        r_7 = self.sha256_a(test_vector_7)
        r_8 = self.sha256_a(test_vector_8)
        self.assertEqual(r_1, sha_1)
        self.assertEqual(r_2, sha_2)
        self.assertEqual(r_3, sha_3)
        self.assertEqual(r_4, sha_4)
        # self.assertEqual(r_5, sha_5)
        self.assertEqual(r_6, sha_6)
        self.assertEqual(r_7, sha_7)
        self.assertEqual(r_8, sha_8)

    def sha256_a(self, text_vector):
        hasher = SHA256()
        hasher.update(text_vector)
        return hasher.hexdigest()


if __name__ == '__main__':
    unittest.main()
