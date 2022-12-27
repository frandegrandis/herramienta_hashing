import os
from unittest import TestCase

from dominio.hasher.hasher import Hasher


class HasherTestCase(TestCase):
    def test_obtain_md5_hash_of_different_strings(self):
        hasher = self.md5_hasher()

        self.assertEqual("4d186321c1a7f0f354b297e8914ab240", hasher.hash("hola"))
        self.assertEqual("d0a4a9d5eae1444b3285be84e98afcf8", hasher.hash("chau"))
        return

    def test_obtain_md5_hash_special_characters(self):
        hasher = self.md5_hasher()

        self.assertEqual("97e5094e8302a2129151f075165779e2", hasher.hash("ñandú"))
        return

    def test_obtain_md5_hash_short_file(self):
        hasher = self.md5_hasher()
        file = open(self.get_file_path("test_file_short.txt"), "rb"
                                                               "")

        self.assertEqual("d6b7f65ee6b6ac2c7b8cc44f87292535", hasher.hash(file))
        file.close()
        return

    def test_obtain_md5_hash_2k_line_file(self):
        hasher = self.md5_hasher()
        file = open(self.get_file_path("test_file_2000_lines.txt"), "rb")

        self.assertEqual("d42796d0445ab5e2f8543351dc47b3e4", hasher.hash(file))
        file.close()
        return

    def md5_hasher(self):
        return Hasher()

    def get_file_path(self, filename):
        return os.path.join(os.path.dirname(__file__), filename)
