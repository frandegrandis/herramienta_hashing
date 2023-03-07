import unittest

import dominio.algoritmos.sha256.constantes_sha256
from helpers.debugger import Debugger
from dominio.algoritmos.md5.md5_operations import F


def debugger():
    return Debugger.md5("Hola")


def palabras_bloque_1():
    return [0x616C6F48, 0x00000080, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x00000020, 0x0]


def valores_iniciales_paso_3():
    return [0x98BADCFE, 0xDA1A0773, 0x5B578B25, 0xEFCDAB89]


def valores_finales_paso_4():
    return [0x5B578B25, 0x48417A79, 0xCD1E80D8, 0xDA1A0773]


class DebuggerTest(unittest.TestCase):
    def test_obtengo_las_palabras_de_un_bloque_particular(self):
        serializer = debugger()

        self.assertEqual(palabras_bloque_1(), serializer.palabras(bloque=1))

    def test_obtengo_los_valores_iniciales_paso_particular(self):
        serializer = debugger()

        self.assertEqual(valores_iniciales_paso_3(), dominio.algoritmos.sha256.constantes_sha256.valores_iniciales(paso=3, bloque=1))

    def test_obtengo_la_operacion_paso_particular(self):
        serializer = debugger()

        self.assertTrue(isinstance(serializer.operacion(paso=1, bloque=1), F))

    def test_obtengo_los_valores_finales_paso_particular(self):
        serializer = debugger()

        self.assertEqual(valores_finales_paso_4(), serializer.valores_finales(paso=4, bloque=1))

    def test_le_pido_al_debugger_el_debug_de_md5(self):
        debugger = Debugger.md5("Hola")

        self.assertEqual("f688ae26e9cfa3ba6235477831d5122e", debugger.resultado_final())
