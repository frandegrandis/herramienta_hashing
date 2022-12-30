import unittest

from helpers.utilidades import suma_modular


class MyTestCase(unittest.TestCase):
    def test_suma_modular(self):
        self.assertEqual(suma_modular(9, 7, 5), 1)
        self.assertEqual(suma_modular(119, 136, 11), 2)
