import struct

import binascii

from dominio.algoritmo import Algoritmo
from dominio.algoritmos.sha256.constantes_sha256 import valores_iniciales, K
from dominio.algoritmos.sha256.iteracion_sha256 import IteracionSHA256
from dominio.algoritmos.sha256.operaciones import sigma0, sigma1
from helpers.operaciones_bit_a_bit import suma_modular


class SHA256(Algoritmo):
    def __init__(self):
        self.constantes =  K
        self.h = [i for i in valores_iniciales]
        self.iteraciones = []

    def update(self, message):
        if type(message) is not str:
            raise TypeError('Given message should be a string.')
        bytes_a_hashear = bytearray(message, encoding='utf-8')

        padding_len = 63 - (len(bytes_a_hashear) + 8) % 64
        ending = struct.pack('!Q', len(bytes_a_hashear) << 3)
        bytes_a_hashear.append(0x80)
        bytes_a_hashear.extend([0] * padding_len)
        bytes_a_hashear.extend(bytearray(ending))

        for chunk_start in range(0, len(bytes_a_hashear), 64):
            chunk = bytes_a_hashear[chunk_start:chunk_start + 64]
            word_schedule = self.generar_word_schedule(chunk)
            a, b, c, d, e, f, g, h = self.h
            for j in range(64):
                iteracion = IteracionSHA256(
                    a=a,
                    b=b,
                    c=c,
                    d=d,
                    e=e,
                    f=f,
                    g=g,
                    h=h,
                    constante_a_usar=self.constantes[j],
                    palabra_a_sumar=word_schedule[j]
                )
                a, b, c, d, e, f, g, h = iteracion.valores_finales()
                self.iteraciones.append(iteracion)
            self.h[0] = suma_modular(self.h[0], a)
            self.h[1] = suma_modular(self.h[1], b)
            self.h[2] = suma_modular(self.h[2], c)
            self.h[3] = suma_modular(self.h[3], d)
            self.h[4] = suma_modular(self.h[4], e)
            self.h[5] = suma_modular(self.h[5], f)
            self.h[6] = suma_modular(self.h[6], g)
            self.h[7] = suma_modular(self.h[7], h)
        return

    def hexdigest(self):
        return binascii.hexlify(
            b''.join(struct.pack('!I', element) for element in self.h),
        ).decode('utf-8')

    def generar_word_schedule(self, chunk):
        words = [0] * 64
        words[0:16] = struct.unpack('!16I', chunk)

        # Calcula 48 palabras adicionales
        for i in range(16, 64):
            words[i] = ((words[i - 16] + sigma0(words[i - 15]) + words[i - 7] + sigma1(words[i - 2])) & 0xFFFFFFFF)

        return words

    def cantidad_de_pasos_por_bloque(self):
        return 64