from unittest import TestCase

from controllers.hasher_controller import HasherController
from tests.helpers.hasher_stub import HasherStub


class HasherTestCase(TestCase):
    def test_hashea_un_string_con_md5_y_retorna_el_resultado(self):
        valor_de_hash_md5 = "un valor hasheado"
        hasher_stub = HasherStub(valor_de_hash_md5)
        controller = HasherController(hasher_stub)
        valor_a_hashear = "hola"

        self.assertEqual(controller.calcular_hash_md5(valor_a_hashear), valor_de_hash_md5)
        self.assertTrue(hasher_stub.recibio("md5"))
        self.assertTrue(hasher_stub.recibio("hash", parametros=[valor_a_hashear]))

    def test_hashea_un_string_con_sha1_y_retorna_el_resultado(self):
        valor_de_hash = "un valor hasheado"
        hasher_stub = HasherStub(valor_de_hash)
        controller = HasherController(hasher_stub)
        valor_a_hashear = "hola"

        self.assertEqual(controller.calcular_hash_sha1(valor_a_hashear), valor_de_hash)
        self.assertTrue(hasher_stub.recibio("sha1"))
        self.assertTrue(hasher_stub.recibio("hash", parametros=[valor_a_hashear]))

    def test_hashea_un_string_con_sha256_y_retorna_el_resultado(self):
        valor_de_hash = "un valor hasheado"
        hasher_stub = HasherStub(valor_de_hash)
        controller = HasherController(hasher_stub)
        valor_a_hashear = "hola"

        self.assertEqual(controller.calcular_hash_sha256(valor_a_hashear), valor_de_hash)
        self.assertTrue(hasher_stub.recibio("sha256"))
        self.assertTrue(hasher_stub.recibio("hash", parametros=[valor_a_hashear]))
