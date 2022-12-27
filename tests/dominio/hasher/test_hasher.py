import os
from unittest import TestCase

from dominio.hasher.hasher import Hasher


class HasherTestCase(TestCase):
    def test_obtener_hash_md5_de_strings_distintos(self):
        self.assertEqual("4d186321c1a7f0f354b297e8914ab240", self.hasher_md5().hash("hola"))
        self.assertEqual("d0a4a9d5eae1444b3285be84e98afcf8", self.hasher_md5().hash("chau"))
        return

    def test_obtener_hash_con_caracteres_especiales(self):
        hasher = self.hasher_md5()

        self.assertEqual("97e5094e8302a2129151f075165779e2", hasher.hash("ñandú"))
        return

    def test_obtain_hash_md5_de_archivo_pequeño(self):
        hasher = self.hasher_md5()
        file = open(self.path_de("test_file_short.txt"), "rb")

        self.assertEqual("d6b7f65ee6b6ac2c7b8cc44f87292535", hasher.hash(file))
        file.close()
        return

    def test_obtener_hash_md5_de_archivo_con_2k_lineas(self):
        hasher = self.hasher_md5()
        file = open(self.path_de("test_file_2000_lines.txt"), "rb")

        self.assertEqual("d42796d0445ab5e2f8543351dc47b3e4", hasher.hash(file))
        file.close()
        return

    def hasher_md5(self):
        return Hasher()

    def path_de(self, nombre_archivo):
        return os.path.join(os.path.dirname(__file__), nombre_archivo)
