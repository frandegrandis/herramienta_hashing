import io
import struct

from dominio.algoritmo import Algoritmo
from dominio.algoritmos.sha1.iteracion_sha1 import IteracionSHA1
from dominio.algoritmos.sha1.operaciones_sha1 import I, H, F, G
from helpers.operaciones_bit_a_bit import rotar_izquierda
from helpers.utilidades import suma_modular, detectar, obtener_palabras

sha1_block_size = 64


class SHA1(Algoritmo):
    def __init__(self):
        # Initial digest variables
        self._h = (
            0x67452301,
            0xEFCDAB89,
            0x98BADCFE,
            0x10325476,
            0xC3D2E1F0,
        )

        self.ya_proceso = False

        # bytes object with 0 <= len < 64 used to store the end of the message
        # if the message length is not congruent to 64
        self._unprocessed = b''
        # Length in bytes of all data that has been processed so far
        self._message_byte_length = 0
        self.iteraciones = []

        self.operaciones = [F(), G(), H(), I()]
        self.constantes = [0x5A827999, 0x6ED9EBA1, 0x8F1BBCDC, 0xCA62C1D6]
        self.palabras = []

    def update(self, arg):
        """Update the current digest.

        This may be called repeatedly, even after calling digest or hexdigest.

        Arguments:
            arg: bytes, bytearray, or BytesIO object to read from.
        """
        if isinstance(arg, (bytes, bytearray)):
            arg = io.BytesIO(arg)

        # Try to build a chunk out of the unprocessed data, if any
        chunk = self._unprocessed + arg.read(sha1_block_size - len(self._unprocessed))

        # Read the rest of the data, 64 bytes at a time
        while len(chunk) == sha1_block_size:
            self._process_chunk(chunk)
            self._message_byte_length += sha1_block_size
            chunk = arg.read(sha1_block_size)

        self._unprocessed = chunk
        self.hexdigest()
        return self

    def digest(self):
        """Produce the final hash value (big-endian) as a bytes object"""
        return b''.join(struct.pack(b'>I', h) for h in self._produce_digest())

    def hexdigest(self):
        """Produce the final hash value (big-endian) as a hex string"""
        return '%08x%08x%08x%08x%08x' % self._produce_digest()

    def _produce_digest(self):
        if self.ya_proceso:
            return self._h
        self.ya_proceso = True
        """Return finalized digest variables for the data processed so far."""
        # Pre-processing:
        message = self._unprocessed
        message_byte_length = self._message_byte_length + len(message)

        # append the bit '1' to the message
        message += b'\x80'

        # append 0 <= k < 512 bits '0', so that the resulting message length (in bytes)
        # is congruent to 56 (mod 64)
        message += b'\x00' * ((56 - (message_byte_length + 1) % sha1_block_size) % sha1_block_size)

        # append length of message (before pre-processing), in bits, as 64-bit big-endian integer
        message_bit_length = message_byte_length * 8
        message += struct.pack(b'>Q', message_bit_length)

        # Process the final chunk
        # At this point, the length of the message is either 64 or 128 bytes.
        self._process_chunk(message[:64])
        if len(message) == sha1_block_size:
            return self._h
        self._process_chunk(message[sha1_block_size:])
        return self._h

    def _process_chunk(self, chunk):

        palabras = obtener_palabras(chunk=chunk, byteorder='big', block_size=sha1_block_size)
        self.palabras.extend(palabras)

        self.agregar_palabras(palabras)

        a, b, c, d, e = self._h

        for i in range(1, 81):
            k = self.constante_de(i)
            operacion = self.obtener_operacion_en(i)
            iteracion = IteracionSHA1(constante_k=k,
                                      A=a,
                                      B=b,
                                      C=c,
                                      D=d,
                                      E=e,
                                      operacion=operacion,
                                      palabra_a_sumar=palabras[i - 1])
            self.iteraciones.append(iteracion)
            a, b, c, d, e = iteracion.ejecutar()

        self.actualizar_estado(a, b, c, d, e)

    def agregar_palabras(self, palabras):
        for i in range(16, 80):
            b1 = palabras[i - 3] ^ palabras[i - 8]
            c1 = palabras[i - 14]
            d1 = palabras[i - 16]
            palabras.append(rotar_izquierda(b1 ^ c1 ^ d1, 1))

    def actualizar_estado(self, a, b, c, d, e):
        h0 = suma_modular(self._h[0], a)
        h1 = suma_modular(self._h[1], b)
        h2 = suma_modular(self._h[2], c)
        h3 = suma_modular(self._h[3], d)
        h4 = suma_modular(self._h[4], e)
        self._h = (h0, h1, h2, h3, h4)

    def constante_de(self, iteracion):
        return self.constantes[(iteracion - 1) // 20]

    def aplicar_operacion_de_sobre(self, iteracion, elementos):
        return self.obtener_operacion_en(iteracion).aplicar_a(*elementos)

    def obtener_operacion_en(self, iteracion):
        return detectar(self.operaciones, lambda operacion: operacion.aplica_a(iteracion))

    def A(self):
        return self._h[0]

    def B(self):
        return self._h[1]

    def C(self):
        return self._h[2]

    def D(self):
        return self._h[3]

    def E(self):
        return self._h[4]

    def cantidad_de_pasos_por_bloque(self):
        return 80

    def palabras_hasheadas(self):
        return self.palabras

    def tamanio_de_palbra_en_bytes(self):
        return 4
