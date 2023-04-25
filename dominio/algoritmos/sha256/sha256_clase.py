import struct

import binascii

from bitarray import bitarray

from dominio.algoritmo import Algoritmo
from dominio.algoritmos.sha256.constantes_sha256 import valores_iniciales, K
from dominio.algoritmos.sha256.iteracion_sha256 import IteracionSHA256
from dominio.algoritmos.sha256.operaciones import sigma0, sigma1
from helpers.utilidades import suma_modular


class SHA256(Algoritmo):
    def __init__(self):
        self.constantes = K
        self.h = list(valores_iniciales)
        self.iteraciones = []
        self.palabras = None

    def update(self, bytes_a_hashear: [str, bytearray]):
        if type(bytes_a_hashear) is str:
            bytes_a_hashear = bytearray(bytes_a_hashear, encoding='utf-8')

        padding_len = 63 - (len(bytes_a_hashear) + 8) % 64
        ending = struct.pack('!Q', len(bytes_a_hashear) << 3)
        bytes_a_hashear.append(0x80)
        bytes_a_hashear.extend([0] * padding_len)
        bytes_a_hashear.extend(bytearray(ending))
        self.palabras = bytes_a_hashear
        a = bitarray()
        a.frombytes(bytes_a_hashear)

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

            self.h = [
                suma_modular(x, y)
                for x, y in zip(self.h, (a, b, c, d, e, f, g, h))
            ]
        return

    def hexdigest(self):
        return binascii.hexlify(
            b''.join(struct.pack('!I', element) for element in self.h),
        ).decode('utf-8')

    def generar_word_schedule(self, chunk):
        words = [0] * 64
        words[0:16] = struct.unpack('!16I', chunk)
        for i in range(16, 64):
            words[i] = suma_modular(words[i - 16] + sigma0(words[i - 15]) + words[i - 7], sigma1(words[i - 2]))

        return words

    def cantidad_de_pasos_por_bloque(self):
        return 64

    def palabras_hasheadas(self):
        palabras = []
        for i in range(0,len(self.palabras),4):
            palabras.append(int.from_bytes(self.palabras[i: i+4], byteorder="big", signed=False))
        return palabras

    def tamanio_de_palbra_en_bytes(self):
        return 4
