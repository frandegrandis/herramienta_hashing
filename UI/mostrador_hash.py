from customtkinter import CTkTabview

from UI.components.caja_de_iteraciones_de_pasos_por_bloque import CajaDeIteracionesDePasosPorBloque
from UI.components.caja_de_texto import CajaDeTexto
from UI.components.caja_de_iteraciones_de_bloques import CajaDeIteracionesDeBloques

Resultado = "Resultado"
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

        self._cargar_tabs([PorPasos, PorBloques])

        CajaDeIteracionesDePasosPorBloque.md5(master=self.tab(PorPasos), debugger=debugger).pack(fill="both", expand=1)
        CajaDeIteracionesDeBloques.md5(master=self.tab(PorBloques), debugger=debugger).pack(fill="both", expand=1)

        self.caja_resultado.mostrar(debugger.resultado_final())

    def mostrar_pasos_sha1(self, debugger):
        self._borrar_tabs()

        self._cargar_tabs([PorPasos, PorBloques])

        CajaDeIteracionesDeBloques.sha1(master=self.tab(PorBloques), debugger=debugger).pack(fill="both", expand=1)
        CajaDeIteracionesDePasosPorBloque.sha1(master=self.tab(PorPasos), debugger=debugger).pack(fill="both", expand=1)

        self.caja_resultado.mostrar(debugger.resultado_final())

    def mostrar_pasos_sha256(self, debugger):
        self._borrar_tabs()

        self._cargar_tabs([PorPasos, PorBloques, PorPasosResumido])

        CajaDeIteracionesDePasosPorBloque.sha256(master=self.tab(PorPasos), debugger=debugger).pack(fill="both",
                                                                                                    expand=1)
        CajaDeIteracionesDeBloques.sha256(master=self.tab(PorBloques), debugger=debugger).pack(fill="both", expand=1)
        CajaDeIteracionesDePasosPorBloque.sha256_resumido(master=self.tab(PorPasosResumido), debugger=debugger).pack(fill="both", expand=1)

        self.caja_resultado.mostrar(debugger.resultado_final())

    def _cargar_tabs(self, tabs_a_cargar):
        for tab in tabs_a_cargar:
            self.add(tab)

    def _borrar_tabs(self):
        posibles_tabs = [PorPasos, PorBloques, PorPasosResumido]
        for tab in posibles_tabs:
            try:
                self.delete(tab)
            except:
                pass
