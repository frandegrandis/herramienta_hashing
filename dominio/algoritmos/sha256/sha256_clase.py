from dominio.algoritmos.sha256.constantes_sha256 import valores_iniciales, K
from dominio.algoritmos.sha256.iteracion_sha256 import IteracionSHA256
from dominio.algoritmos.sha256.operaciones import sigma0, sigma1
from helpers.operaciones_bit_a_bit import bitarray_de_numero, hex_de_bitarray, suma_modular_de_bitarrays, bitsarray_de_bytes


class SHA256:
    def __init__(self):
        self.constantes = [bitarray_de_numero(v) for v in K]
        self.h = [bitarray_de_numero(v1) for v1 in valores_iniciales]
        self.iteraciones = []

    def update(self, bytes_a_hashear):
        chunks = self.preprocessMessage(bytes_a_hashear)
        for chunk in chunks:
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
            self.h[0] = suma_modular_de_bitarrays(self.h[0], a)
            self.h[1] = suma_modular_de_bitarrays(self.h[1], b)
            self.h[2] = suma_modular_de_bitarrays(self.h[2], c)
            self.h[3] = suma_modular_de_bitarrays(self.h[3], d)
            self.h[4] = suma_modular_de_bitarrays(self.h[4], e)
            self.h[5] = suma_modular_de_bitarrays(self.h[5], f)
            self.h[6] = suma_modular_de_bitarrays(self.h[6], g)
            self.h[7] = suma_modular_de_bitarrays(self.h[7], h)
        return

    def hexdigest(self):
        digest = ''
        for val in self.h:
            digest += hex_de_bitarray(val)
        return digest

    def preprocessMessage(self, message):
        bits = bitsarray_de_bytes(message)
        largo_en_bits = bitarray_de_numero(len(bits), 8)
        bits.append(1)
        while (len(bits) + 64) % 512 != 0:
            bits.append(0)
        bits = bits + largo_en_bits
        return self.chunker(bits, 512)

    def chunker(self, bits, chunk_length=8):
        chunked = []
        for b in range(0, len(bits), chunk_length):
            chunked.append(bits[b:b + chunk_length])
        return chunked

    def generar_word_schedule(self, chunk):
        word_schedule = self.chunker(chunk, 32)
        for _ in range(48):
            word_schedule.append(32 * [0])
        for i in range(16, 64):
            word_schedule[i] = suma_modular_de_bitarrays(
                suma_modular_de_bitarrays(suma_modular_de_bitarrays(sigma1(word_schedule[i - 2]), word_schedule[i - 7]),
                                          sigma0(word_schedule[i - 15])),
                word_schedule[i - 16])
        return word_schedule
