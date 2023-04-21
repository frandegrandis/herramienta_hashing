from unittest import TestCase

from controllers.hasher_controller import HasherController
from helpers.debugger import Debugger
from tests.helpers.hasher_stub import HasherStub


class DebuggerStub:
    def creado_con(self, parametro_de_inicializacion):
        return self.string_a_hashear == parametro_de_inicializacion

    def __call__(self, *args, **kwargs):
        self.string_a_hashear = args[0]


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

    def test_hashea_un_string_con_sha512_y_retorna_el_resultado(self):
        valor_de_hash = "un valor hasheado"
        hasher_stub = HasherStub(valor_de_hash)
        controller = HasherController(hasher_stub)
        valor_a_hashear = "hola"

        self.assertEqual(controller.calcular_hash_sha512(valor_a_hashear), valor_de_hash)
        self.assertTrue(hasher_stub.recibio("sha256"))
        self.assertTrue(hasher_stub.recibio("hash", parametros=[valor_a_hashear]))

    def test_hashea_un_string_con_sha256_y_retorna_el_resultado(self):
        valor_de_hash = "un valor hasheado"
        hasher_stub = HasherStub(valor_de_hash)
        controller = HasherController(hasher_stub)
        valor_a_hashear = "hola"

        self.assertEqual(controller.calcular_hash_sha256(valor_a_hashear), valor_de_hash)
        self.assertTrue(hasher_stub.recibio("sha256"))
        self.assertTrue(hasher_stub.recibio("hash", parametros=[valor_a_hashear]))

    def test_el_debug_de_un_string_con_md5_retorna_un_debugger(self):
        debugger = HasherController().debugguear_md5("hola")

        self.assertTrue(isinstance(debugger, Debugger))

    def test_el_debug_de_un_string_con_md5_se_realiza_correctamente(self):
        string_a_hashear = "hola"
        debugger_stub = DebuggerStub()

        HasherController(debugger_md5=debugger_stub).debugguear_md5(string_a_hashear)

        self.assertTrue(debugger_stub.creado_con(string_a_hashear))

    def test_el_debug_de_un_string_con_sha1_retorna_un_debugger(self):
        debugger = HasherController().debugguear_sha1("hola")

        self.assertTrue(isinstance(debugger, Debugger))

    def test_el_debug_de_un_string_con_sha256_retorna_un_debugger(self):
        debugger = HasherController().debugguear_sha1("hola")

        self.assertTrue(isinstance(debugger, Debugger))

    def test_el_debug_de_un_string_con_sha1_se_realiza_correctamente(self):
        string_a_hashear = "hola"
        debugger_stub = DebuggerStub()

        HasherController(debugger_sha1=debugger_stub).debugguear_sha1(string_a_hashear)

        self.assertTrue(debugger_stub.creado_con(string_a_hashear))
