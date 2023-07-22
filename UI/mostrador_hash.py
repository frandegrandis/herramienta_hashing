from customtkinter import CTkTabview

from UI.components.caja_de_iteraciones_de_pasos_por_bloque import CajaDeIteracionesDePasosPorBloque
from UI.components.caja_de_texto import CajaDeTexto
from UI.components.caja_de_iteraciones_de_bloques import CajaDeIteracionesDeBloques
from dominio.algoritmos.serializador_de_padding import serializar_padding

Resultado = "Resultado"
Padding = "Debug del padding"
PorBloques = "Debug por bloques"
PorPasos = "Debug por pasos"
PorPasosResumido = "Debug por pasos resumidos"


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

    def append_texto(self, texto_a_mostrar):
        self._borrar_tabs()

        self.caja_resultado.append(texto_a_mostrar)
