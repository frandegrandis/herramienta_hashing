import os
from unittest import TestCase

from dominio.hasher.hasher import Hasher


class HasherTestCase(TestCase):
    def test_obtener_hash_md5_de_strings_distintos(self):
        hash_md5_de_hola = "4d186321c1a7f0f354b297e8914ab240"
        hash_md5_de_chau = "d0a4a9d5eae1444b3285be84e98afcf8"

        self.assertEqual(hash_md5_de_hola, self.hasher_md5().hash("hola"))
        self.assertEqual(hash_md5_de_chau, self.hasher_md5().hash("chau"))
        return

    def test_obtener_hash_con_caracteres_especiales(self):
        hash_md5_de_ñandú = "97e5094e8302a2129151f075165779e2"

        self.assertEqual(hash_md5_de_ñandú, self.hasher_md5().hash("ñandú"))
        return

    def test_obtener_hash_md5_de_archivo_pequeño(self):
        file = open(self.path_de("test_file_short.txt"), "rb")

        self.assertEqual("d6b7f65ee6b6ac2c7b8cc44f87292535", self.hasher_md5().hash(file))
        file.close()
        return

    def test_obtener_hash_md5_de_archivo_con_2k_lineas(self):
        hasher = self.hasher_md5()
        file = open(self.path_de("test_file_2000_lines.txt"), "rb")

        self.assertEqual("d42796d0445ab5e2f8543351dc47b3e4", hasher.hash(file))
        file.close()
        return

    def test_obtener_hash_sha1_de_strings_distintos(self):
        hash_sha1_de_hola = "99800b85d3383e3a2fb45eb7d0066a4879a9dad0"
        hash_sha1_de_chau = "3d4a2606003e419d39092ab6fd09944cb1879ce4"

        self.assertEqual(hash_sha1_de_hola, self.hasher_sha1().hash("hola"))
        self.assertEqual(hash_sha1_de_chau, self.hasher_sha1().hash("chau"))
        return

    def test_obtener_hash_sha256_de_strings_distintos(self):
        hash_sha256_de_hola = "b221d9dbb083a7f33428d7c2a3c3198ae925614d70210e28716ccaa7cd4ddb79"
        hash_sha256_de_chau = "2274631b81def59664f20cb9fa010e4cde57f64a263f2874dfde0fe346d59c60"

        self.assertEqual(hash_sha256_de_hola, self.hasher_sha256().hash("hola"))
        self.assertEqual(hash_sha256_de_chau, self.hasher_sha256().hash("chau"))
        return

    def test_obtener_hash_sha512_de_strings_distintos(self):
        hash_sha512_de_hola = "e83e8535d6f689493e5819bd60aa3e5fdcba940e6d111ab6fb5c34f24f86496bf3726e2bf4ec59d6d2f5a2aeb1e4f103283e7d64e4f49c03b4c4725cb361e773"
        hash_sha512_de_chau = "12511bcbe20edf362ac825d282987ca255d1f5dbb5c989cfd506151b8443f9bcfba8c522abc418736ad0187e6533da39d6de85086c138d1fda78712637f48094"

        self.assertEqual(hash_sha512_de_hola, self.hasher_sha512().hash("hola"))
        self.assertEqual(hash_sha512_de_chau, self.hasher_sha512().hash("chau"))
        return

    def test_el_mismo_hasher_sirve_para_strings_distintos(self):
        hash_sha256_de_hola = "b221d9dbb083a7f33428d7c2a3c3198ae925614d70210e28716ccaa7cd4ddb79"
        hash_sha256_de_chau = "2274631b81def59664f20cb9fa010e4cde57f64a263f2874dfde0fe346d59c60"
        sha_hasher = self.hasher_sha256()

        self.assertEqual(hash_sha256_de_hola, sha_hasher.hash("hola"))
        self.assertEqual(hash_sha256_de_chau, sha_hasher.hash("chau"))

    def hasher_md5(self):
        return Hasher.md5()

    def path_de(self, nombre_archivo):
        return os.path.join(os.path.dirname(__file__), nombre_archivo)

    def hasher_sha1(self):
        return Hasher.sha1()

    def hasher_sha256(self):
        return Hasher.sha256()
    def hasher_sha512(self):
        return Hasher.sha512()
