import io
import struct

from dominio.algoritmos.operaciones_sha1 import I, H, F, G
from helpers.operaciones_bit_a_bit import rotar_izquierda
from helpers.utilidades import suma_modular, detectar


class SHA1(object):
    """A class that mimics that hashlib api and implements the SHA-1 algorithm."""

    name = 'python-sha1'
    digest_size = 20
    block_size = 64

    def __init__(self):
        # Initial digest variables
        self._h = (
            0x67452301,
            0xEFCDAB89,
            0x98BADCFE,
            0x10325476,
            0xC3D2E1F0,
        )

        # bytes object with 0 <= len < 64 used to store the end of the message
        # if the message length is not congruent to 64
        self._unprocessed = b''
        # Length in bytes of all data that has been processed so far
        self._message_byte_length = 0

        self.operaciones = [F(), G(), H(), I()]
        self.constantes = [0x5A827999, 0x6ED9EBA1, 0x8F1BBCDC, 0xCA62C1D6]

    def update(self, arg):
        """Update the current digest.

        This may be called repeatedly, even after calling digest or hexdigest.

        Arguments:
            arg: bytes, bytearray, or BytesIO object to read from.
        """
        if isinstance(arg, (bytes, bytearray)):
            arg = io.BytesIO(arg)

        # Try to build a chunk out of the unprocessed data, if any
        chunk = self._unprocessed + arg.read(64 - len(self._unprocessed))

        # Read the rest of the data, 64 bytes at a time
        while len(chunk) == 64:
            self._process_chunk(chunk)
            self._message_byte_length += 64
            chunk = arg.read(64)

        self._unprocessed = chunk
        return self

    def digest(self):
        """Produce the final hash value (big-endian) as a bytes object"""
        return b''.join(struct.pack(b'>I', h) for h in self._produce_digest())

    def hexdigest(self):
        """Produce the final hash value (big-endian) as a hex string"""
        return '%08x%08x%08x%08x%08x' % self._produce_digest()

    def _produce_digest(self):
        """Return finalized digest variables for the data processed so far."""
        # Pre-processing:
        message = self._unprocessed
        message_byte_length = self._message_byte_length + len(message)

        # append the bit '1' to the message
        message += b'\x80'

        # append 0 <= k < 512 bits '0', so that the resulting message length (in bytes)
        # is congruent to 56 (mod 64)
        message += b'\x00' * ((56 - (message_byte_length + 1) % 64) % 64)

        # append length of message (before pre-processing), in bits, as 64-bit big-endian integer
        message_bit_length = message_byte_length * 8
        message += struct.pack(b'>Q', message_bit_length)

        # Process the final chunk
        # At this point, the length of the message is either 64 or 128 bytes.
        self._process_chunk(message[:64])
        if len(message) == 64:
            return self._h
        self._process_chunk(message[64:])
        return self._h

    def _process_chunk(self, chunk):
        """Process a chunk of data and return the new digest variables."""
        assert len(chunk) == 64

        w = [0] * 80

        # Break chunk into sixteen 4-byte big-endian words w[i]
        for iteracion in range(16):
            w[iteracion] = struct.unpack(b'>I', chunk[iteracion * 4:iteracion * 4 + 4])[0]

        # Extend the sixteen 4-byte words into eighty 4-byte words
        for iteracion in range(16, 80):
            b1 = w[iteracion - 3] ^ w[iteracion - 8]
            c1 = w[iteracion - 14]
            d1 = w[iteracion - 16]
            w[iteracion] = rotar_izquierda(b1 ^ c1 ^ d1, 1)

        # Initialize hash value for this chunk
        a = self._h[0]
        b = self._h[1]
        c = self._h[2]
        d = self._h[3]
        e = self._h[4]

        for iteracion in range(1, 81):
            k = self.constantes[(iteracion - 1) // 20]

            a, b, c, d, e = (
            suma_modular(rotar_izquierda(a, 5) + self.aplicar_operacion_de_sobre(iteracion, [b, c, d]) + e + k,
                         w[iteracion - 1]),
            a, rotar_izquierda(b, 30), c, d)

        # Add this chunk's hash to result so far
        h0 = suma_modular(self._h[0], a)
        h1 = suma_modular(self._h[1], b)
        h2 = suma_modular(self._h[2], c)
        h3 = suma_modular(self._h[3], d)
        h4 = suma_modular(self._h[4], e)

        self._h = (h0, h1, h2, h3, h4)

    def aplicar_operacion_de_sobre(self, iteracion, elementos):
        return self.obtener_operacion_en(iteracion).aplicar_a(*elementos)

    def obtener_operacion_en(self, iteracion):
        return detectar(self.operaciones, lambda operacion: operacion.aplica_a(iteracion))
