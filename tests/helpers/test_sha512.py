import unittest

from dominio.algoritmos.sha512.sha512_clase import SHA512

test_vector_1 = ("")
test_vector_2 = ("abc")
test_vector_3 = ("abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq")
test_vector_4 = (
    "abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu")
test_vector_5 = ("a" * 1000000)
test_vector_6 = ("abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopqp")
test_vector_7 = ("abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopqpqpmomom")
test_vector_8 = (
    "ibsnqwpzhillptcinmtvamymvixjxaumjddwxsxxjhjhnftynajhsluuctgjytazlcdewsexbjcpumdcfbbbmzwxcmjmnxfqurvaarapdswyatlyvqsxdefmehicwwdnkshzgysaxxenmtpirbhphxyaesgwigdxzqpekouenexqkqgpnzzwyjppc")
sha_1 = "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e"
sha_2 = "ddaf35a193617abacc417349ae20413112e6fa4e89a97ea20a9eeee64b55d39a2192992a274fc1a836ba3c23a3feebbd454d4423643ce80e2a9ac94fa54ca49f"
sha_3 = "204a8fc6dda82f0a0ced7beb8e08a41657c16ef468b228a8279be331a703c33596fd15c13b1b07f9aa1d3bea57789ca031ad85c7a71dd70354ec631238ca3445"
sha_4 = "8e959b75dae313da8cf4f72814fc143f8f7779c6eb9f7fa17299aeadb6889018501d289e4900f7e4331b99dec4b5433ac7d329eeb6dd26545e96e55b874be909"
sha_5 = "e718483d0ce769644e2e42c7bc15b4638e1f98b13b2044285632a803afa973ebde0ff244877ea60a4cb0432ce577c31beb009c5c2c49aa2e4eadb217ad8cc09b"
sha_6 = "01eebc298d686f9abbcc33acba67d6edeb9a024da4ecdf9ddaf0c8749a8b88567f4cc9c9b09ffd14ea79aeb56a80be95b0f6d05c75d591f17c81a9096f8dbcfe"
sha_7 = "887baf0b21093e9af359682aeff551d2424a47e010f53c5ef45c7593516594caf9e342f6bcc4e501f3afac8ba59d0d3658a87dcbf74f36baea90670318b2836e"
sha_8 = '73f909e9d33972471f8f92b50d02d30966eb8160e20551d8159cd97f750a0655cfab842921c6050b3ebfdd6f48a0345ada173b3dc250a6d4137cd8d62c4efe04'


class SHA512Test(unittest.TestCase):
    # hash

    def test_sha512(self):
        """tests if sha256 hashes correctly"""
        r_1 = self.sha512_a(test_vector_1)
        r_2 = self.sha512_a(test_vector_2)
        r_3 = self.sha512_a(test_vector_3)
        r_4 = self.sha512_a(test_vector_4)
        r_5 = self.sha512_a(test_vector_5)
        r_6 = self.sha512_a(test_vector_6)
        r_7 = self.sha512_a(test_vector_7)
        r_8 = self.sha512_a(test_vector_8)
        self.assertEqual(r_1, sha_1)
        self.assertEqual(r_2, sha_2)
        self.assertEqual(r_3, sha_3)
        self.assertEqual(r_4, sha_4)
        self.assertEqual(r_5, sha_5)
        self.assertEqual(r_6, sha_6)
        self.assertEqual(r_7, sha_7)
        self.assertEqual(r_8, sha_8)

    def sha512_a(self, text_vector):
        hasher = SHA512()
        hasher.update(text_vector)
        return hasher.hexdigest()