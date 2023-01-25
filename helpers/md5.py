from io import BytesIO
from typing import BinaryIO

import numpy as np

from helpers.iteracion_md5 import IteracionMD5
from helpers.md5_operations import MD5SelectorDeOperaciones
from helpers.utilidades import suma_modular, obtener_palabras

md5_block_size = 64
md5_digest_size = 16

"""
Defino las permutaciones para las 4 rondas
"""


class MD5:
    def __init__(self):
        self.length: int = 0
        self.state: tuple[int, int, int, int] = (0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476)
        self.n_filled_bytes: int = 0
        self.buf: bytearray = bytearray(md5_block_size)
        self.iteraciones = []
        self.palabras_por_bloque = []

    def digest(self) -> bytes:
        return b''.join(x.to_bytes(length=4, byteorder='little') for x in self.state)

    def process(self, stream: BinaryIO) -> None:
        assert self.n_filled_bytes < len(self.buf)

        view = memoryview(self.buf)  # Utilizado para trabajar a nivel de bytes
        while bytes_read := stream.read(md5_block_size - self.n_filled_bytes):
            view[self.n_filled_bytes:self.n_filled_bytes + len(bytes_read)] = bytes_read
            if self.n_filled_bytes == 0 and len(bytes_read) == md5_block_size:
                self.iterar()
                self.length += md5_block_size
            else:
                self.n_filled_bytes += len(bytes_read)
                if self.n_filled_bytes == md5_block_size:
                    self.iterar()
                    self.length += md5_block_size
                    self.n_filled_bytes = 0

    def finalize(self) -> None:
        assert self.n_filled_bytes < md5_block_size

        self.length += self.n_filled_bytes
        self.buf[self.n_filled_bytes] = 0b10000000
        self.n_filled_bytes += 1

        n_bytes_needed_for_len = 8

        if self.n_filled_bytes + n_bytes_needed_for_len > md5_block_size:
            self.buf[self.n_filled_bytes:] = bytes(md5_block_size - self.n_filled_bytes)
            self.iterar()
            self.n_filled_bytes = 0

        self.buf[self.n_filled_bytes:] = bytes(md5_block_size - self.n_filled_bytes)
        bit_len_64 = (self.length * 8) % (2 ** 64)
        self.buf[-n_bytes_needed_for_len:] = bit_len_64.to_bytes(length=n_bytes_needed_for_len,
                                                                 byteorder='little')
        self.iterar()

    def iterar(self) -> None:
        shift = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
                 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]
        sines = np.abs(np.sin(np.arange(64) + 1))
        sine_randomness = [int(x) for x in np.floor(2 ** 32 * sines)]
        msg_chunk = self.buf
        assert len(msg_chunk) == md5_block_size  # 64 bytes, 512 bits
        palabras_del_bloque = obtener_palabras(chunk=msg_chunk, byteorder='little', block_size=md5_block_size)
        self.palabras_por_bloque.append(palabras_del_bloque)
        assert len(palabras_del_bloque) == 16

        a, b, c, d = self.state

        for i in range(md5_block_size):
            iteracion = IteracionMD5(a=a, b=b, c=c, d=d, bits_a_rotar=(shift[i]), s=(sine_randomness[i]),
                                     operacion=(MD5SelectorDeOperaciones.operacion_para(i)),
                                     palabra_a_sumar=(palabras_del_bloque[self.numero_de_palabra_a_sumar_en_paso(i)]))
            a, b, c, d = iteracion.ejecutar()
            self.iteraciones.append(iteracion)

        self.state = (
            suma_modular(self.state[0], a),
            suma_modular(self.state[1], b),
            suma_modular(self.state[2], c),
            suma_modular(self.state[3], d),
        )

    def update(self, s: bytes) -> bytes:
        self.process(BytesIO(s))
        self.finalize()
        return self.digest()

    def hexdigest(self):
        return self.digest().hex()

    def iteraciones_por_bloque(self):
        return [self.iteraciones[x:x+64] for x in range(0, len(self.iteraciones), 64)]

    def palabras_del_bloque(self, n):
        return self.palabras_por_bloque[n - 1]

    def numero_de_palabra_a_sumar_en_paso(self, paso):
        round_1_perm = [i for i in range(16)]  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        round_2_perm = [(5 * i + 1) % 16 for i in range(16)]  # [1, 6, 11, 0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12]
        round_3_perm = [(3 * i + 5) % 16 for i in range(16)]  # [5, 8, 11, 14, 1, 4, 7, 10, 13, 0, 3, 6, 9, 12, 15, 2]
        round_4_perm = [(7 * i) % 16 for i in range(16)]  # [0, 7, 14, 5, 12, 3, 10, 1, 8, 15, 6, 13, 4, 11, 2, 9]

        permutaciones = round_1_perm + round_2_perm + round_3_perm + round_4_perm
        return permutaciones[paso]

    def cantidad_bloques(self):
        return len(self.iteraciones_por_bloque())
