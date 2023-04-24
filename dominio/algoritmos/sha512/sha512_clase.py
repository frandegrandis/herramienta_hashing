from dominio.algoritmo import Algoritmo
import binascii
import struct

from dominio.algoritmos.sha512.constantes_sha512 import initial_hash, round_constants
from dominio.algoritmos.sha512.iteracion_sha512 import IteracionSHA512
from dominio.algoritmos.sha512.operaciones import sigma1, sigma0
from helpers.utilidades import suma_modular


class SHA512(Algoritmo):

    def __init__(self):
        self.h = list(initial_hash)
        self.constantes = round_constants
        self.iteraciones = []

    def update(self, string):
        if type(string) is str:
            string = bytearray(string, encoding='utf-8')
        self.agregar_padding(string)
        for chunk_start in range(0, len(string), 128):
            chunk = string[chunk_start:chunk_start + 128]

            w = self.generar_word_schedule(chunk)

            a, b, c, d, e, f, g, h = self.h

            for i in range(80):
                iteracion = IteracionSHA512(
                    a=a,
                    b=b,
                    c=c,
                    d=d,
                    e=e,
                    f=f,
                    g=g,
                    h=h,
                    constante_a_usar=self.constantes[i],
                    palabra_a_sumar=w[i]
                )
                a, b, c, d, e, f, g, h = iteracion.valores_finales()
                self.iteraciones.append(iteracion)

            self.h = [
                suma_modular(x, y, modulo=2 ** 64)
                for x, y in zip(self.h, (a, b, c, d, e, f, g, h))
            ]
        return

    def hexdigest(self):
        return binascii.hexlify(
            b''.join(struct.pack('!Q', element) for element in (self.h)),
        ).decode('utf-8')

    def generar_word_schedule(self, chunk):
        w = [0] * 80
        w[0:16] = struct.unpack('!16Q', chunk)
        for i in range(16, 80):
            w[i] = suma_modular(w[i - 16] + (sigma0(w[i - 15])) + w[i - 7], (sigma1(w[i - 2])), modulo=2 ** 64)
        return w

    def agregar_padding(self, message_array):
        mdi = len(message_array) % 128
        padding_len = 119 - mdi if mdi < 112 else 247 - mdi
        ending = struct.pack('!Q', len(message_array) << 3)
        message_array.append(0x80)
        message_array.extend([0] * padding_len)
        message_array.extend(bytearray(ending))
