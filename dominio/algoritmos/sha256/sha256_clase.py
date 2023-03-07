from helpers.operaciones_bit_a_bit import bitarray_de_numero, rotar_derecha, \
    hex_de_bitarray, suma_modular_de_bitarrays, bitsarray_de_bytes

valores_iniciales = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]

K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4,
     0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe,
     0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f,
     0x4a7484aa, 0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
     0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc,
     0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b,
     0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070, 0x19a4c116,
     0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
     0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7,
     0xc67178f2]


def ch2(x, y, z):
    return (x & y) ^ (~x & z)


def maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)


def gamma0(x):
    return rotar_derecha(x, 2) ^ rotar_derecha(x, 13) ^ rotar_derecha(x, 22)


def gamma1(x):
    return rotar_derecha(x, 6) ^ rotar_derecha(x, 11) ^ rotar_derecha(x, 25)


def sigma0(x):
    return rotar_derecha(x, 7) ^ rotar_derecha(x, 18) ^ (x >> 3)


def sigma1(x):
    return rotar_derecha(x, 17) ^ rotar_derecha(x, 19) ^ (x >> 10)


class SHA256:
    def __init__(self):
        self.constantes = [bitarray_de_numero(v) for v in K]
        self.h = [bitarray_de_numero(v1) for v1 in valores_iniciales]

    def update(self, bytes_a_hashear):
        chunks = self.preprocessMessage(bytes_a_hashear)
        for chunk in chunks:
            word_schedule = self.generar_word_schedule(chunk)
            a, b, c, d, e, f, g, h = self.h
            for j in range(64):
                temp1 = suma_modular_de_bitarrays(suma_modular_de_bitarrays(
                    suma_modular_de_bitarrays(suma_modular_de_bitarrays(h, gamma1(e)), ch2(e, f, g)),
                    self.constantes[j]),
                    word_schedule[j])
                temp2 = suma_modular_de_bitarrays(gamma0(a), maj(a, b, c))
                h = g
                g = f
                f = e
                e = suma_modular_de_bitarrays(d, temp1)
                d = c
                c = b
                b = a
                a = suma_modular_de_bitarrays(temp1, temp2)
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
        message_len = bitarray_de_numero(len(bits), 8)
        bits.append(1)
        while (len(bits) + 64) % 512 != 0:
            bits.append(0)
        bits = bits + message_len
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
