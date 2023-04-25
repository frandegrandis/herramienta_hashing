from bitarray import bitarray
from customtkinter import CTkTabview

from UI.components.caja_de_iteraciones_de_pasos_por_bloque import CajaDeIteracionesDePasosPorBloque
from UI.components.caja_de_texto import CajaDeTexto
from UI.components.caja_de_iteraciones_de_bloques import CajaDeIteracionesDeBloques
from helpers.debugger import Debugger
from helpers.operaciones_bit_a_bit import bitarray_a_numero
from helpers.utilidades_UI import mostrar_32_bits_centrados_con_espacio, mostrar_64_bits_centrados_con_espacio

Resultado = "Resultado"
Padding = "Debug del padding"
PorBloques = "Debug por bloques"
PorPasos = "Debug por pasos"
PorPasosResumido = "Debug por pasos resumidos"


def serializar_padding(debugger: Debugger):
    tamanio_en_bytes_de_palabra = debugger.tamanio_de_palbra_en_bytes()
    bytearray_inicial = debugger.bytearray_inicial()
    palabras_despues_del_padding = debugger.bytearray_con_padding()
    resultado = "Se comienza con las palabras:\n"
    mostrar_bits = mostrar_32_bits_centrados_con_espacio
    if tamanio_en_bytes_de_palabra == 8:
        mostrar_bits = mostrar_64_bits_centrados_con_espacio


    for i in range(0, len(bytearray_inicial), tamanio_en_bytes_de_palabra):
        resultado+=f"Palabra {(i//tamanio_en_bytes_de_palabra)+1} = "
        bytearray = bytearray_inicial[i:i + tamanio_en_bytes_de_palabra]
        bitarray2 = bitarray()
        bitarray2.frombytes(bytearray)
        if i == range(0, len(bytearray_inicial), tamanio_en_bytes_de_palabra)[-1]:
            resultado += f"    {bin(abs(bitarray_a_numero(bitarray2)))[2:]}\n"
        else:
            resultado+= f"{mostrar_bits(bitarray2)}\n"

    resultado += "Luego de aplicar el padding obtenemos:\n"
    i=1
    # FIXME: MD5 esta andando mal
    for palabra in palabras_despues_del_padding:
        if i < 10:
            resultado+= f"Palabra 0{i} = {mostrar_bits(palabra)}\n"
        else:
            resultado+= f"Palabra {i} = {mostrar_bits(palabra)}\n"
        i+=1
    return resultado


class MostradorHash(CTkTabview):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add(Resultado)
        self.caja_resultado = CajaDeTexto(master=self.tab(Resultado))
        self.caja_resultado.pack(fill="both", expand=1)

    def mostrar_texto(self, texto_a_mostrar):
        self._borrar_tabs()

        self.caja_resultado.mostrar(texto_a_mostrar)

    def mostrar_pasos_md5(self, debugger):
        self._borrar_tabs()

        self._cargar_tabs([Padding, PorPasos, PorBloques])

        self.cargar_padding(debugger)
        CajaDeIteracionesDePasosPorBloque.md5(master=self.tab(PorPasos), debugger=debugger).pack(fill="both", expand=1)
        CajaDeIteracionesDeBloques.md5(master=self.tab(PorBloques), debugger=debugger).pack(fill="both", expand=1)

        self.caja_resultado.mostrar(debugger.resultado_final())

    def cargar_padding(self, debugger):
        padding = CajaDeTexto(master=self.tab(Padding))
        padding.mostrar(serializar_padding(debugger))
        padding.pack(fill="both", expand=1)

    def mostrar_pasos_sha1(self, debugger):
        self._borrar_tabs()

        self._cargar_tabs([Padding, PorPasos, PorBloques])

        self.cargar_padding(debugger)
        CajaDeIteracionesDeBloques.sha1(master=self.tab(PorBloques), debugger=debugger).pack(fill="both", expand=1)
        CajaDeIteracionesDePasosPorBloque.sha1(master=self.tab(PorPasos), debugger=debugger).pack(fill="both", expand=1)

        self.caja_resultado.mostrar(debugger.resultado_final())

    def mostrar_pasos_sha256(self, debugger):
        self._borrar_tabs()

        self._cargar_tabs([Padding, PorPasos, PorBloques, PorPasosResumido])

        self.cargar_padding(debugger)
        CajaDeIteracionesDePasosPorBloque.sha256(master=self.tab(PorPasos), debugger=debugger).pack(fill="both",
                                                                                                    expand=1)
        CajaDeIteracionesDeBloques.sha256(master=self.tab(PorBloques), debugger=debugger).pack(fill="both", expand=1)
        CajaDeIteracionesDePasosPorBloque.sha256_resumido(master=self.tab(PorPasosResumido), debugger=debugger).pack(
            fill="both", expand=1)

        self.caja_resultado.mostrar(debugger.resultado_final())

    def _cargar_tabs(self, tabs_a_cargar):
        for tab in tabs_a_cargar:
            self.add(tab)

    def _borrar_tabs(self):
        posibles_tabs = [Padding, PorPasos, PorBloques, PorPasosResumido]
        for tab in posibles_tabs:
            try:
                self.delete(tab)
            except:
                pass

    def mostrar_pasos_sha512(self, debugger):
        self._borrar_tabs()

        self._cargar_tabs([Padding, PorPasos, PorBloques, PorPasosResumido])

        self.cargar_padding(debugger)
        CajaDeIteracionesDePasosPorBloque.sha512(master=self.tab(PorPasos), debugger=debugger).pack(fill="both",
                                                                                                    expand=1)
        CajaDeIteracionesDeBloques.sha512(master=self.tab(PorBloques), debugger=debugger).pack(fill="both", expand=1)
        CajaDeIteracionesDePasosPorBloque.sha512_resumido(master=self.tab(PorPasosResumido), debugger=debugger).pack(
            fill="both", expand=1)

        self.caja_resultado.mostrar(debugger.resultado_final())
