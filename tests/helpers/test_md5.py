import unittest

import dominio.algoritmos.sha256.constantes_sha256
from dominio.algoritmos.md5.md5 import MD5
from dominio.algoritmos.md5.md5_operations import F
from helpers.utilidades import bytes_de_string


class TestMD5(unittest.TestCase):
    def test_md5(self):
        expectations = {
            "": "d41d8cd98f00b204e9800998ecf8427e",
            "a": "0cc175b9c0f1b6a831c399e269772661",
            "abc": "900150983cd24fb0d6963f7d28e17f72",
            "message digest": "f96b697d7cb7938d525a2f31aaf161d0",
            "abcdefghijklmnopqrstuvwxyz": "c3fcd3d76192e4007dfb496cca67e13b",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789": "d174ab98d277d9f5a5611c2c9f419d9f",
            "12345678901234567890123456789012345678901234567890123456789012345678901234567890": "57edf4a22be3c955ac49da2e2107b67a",
        }

        for string, md5_hash in expectations.items():
            with self.subTest(string=string, md5_hash=md5_hash):
                hasher = MD5()
                hasher.update(bytes_de_string(string))
                self.assertEqual(hasher.hexdigest(), md5_hash)

    def test_se_guardan_todos_los_pasos_luego_de_hashear(self):
        hasher = MD5()
        hasher.update(bytes_de_string("Hola"))

        self.assertEqual(64, len(hasher.iteraciones))

    def test_las_iteraciones_tienen_toda_la_info_necesaria(self):
        hasher = MD5()
        hasher.update(bytes_de_string("Hola"))
        iteracion = hasher.iteraciones[1]

        self.assertEqual([0x10325476, 0x5b578b25, 0xefcdab89, 0x98badcfe], dominio.algoritmos.sha256.constantes_sha256.valores_iniciales())
        self.assertTrue(isinstance(iteracion.operacion, F))
        self.assertEqual(128, iteracion.palabra_a_sumar)
        self.assertEqual(0xe8c7b756, iteracion.constante_s)
        self.assertEqual(12, iteracion.bits_a_rotar)
        self.assertEqual([0x98badcfe, 0xda1a0773, 0x5b578b25, 0xefcdab89], iteracion.valores_finales())

    def test_puedo_pedir_las_iteraciones_por_bloque(self):
        hasher = MD5()
        hasher.update(bytes_de_string("12345678901234567890123456789012345678901234567890123456789012345678901234567890"))
        iteraciones = hasher.iteraciones_por_bloque()

        self.assertEqual(2, len(iteraciones))
        self.assertEqual(64, len(iteraciones[0]))
        self.assertEqual(64, len(iteraciones[1]))
