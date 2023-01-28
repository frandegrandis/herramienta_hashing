from customtkinter import CTkTabview

from UI.components.caja_de_iteraciones_de_pasos_por_bloque import CajaDeIteracionesDePasosPorBloque
from UI.components.caja_de_texto import CajaDeTexto
from UI.components.caja_de_iteraciones_de_bloques import CajaDeIteracionesDeBloques

Resultado = "Resultado"
PorBloques = "Debug por bloques"
PorPasos = "Debug por pasos"


class MostradorHash(CTkTabview):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pasos = None
        self.tab_de_pasos = None
        self.add(Resultado)
        self.caja_resultado = CajaDeTexto(master=self.tab(Resultado))
        self.caja_resultado.pack(fill="both", expand=1)

    def mostrar_texto(self, texto_a_mostrar):
        if self.debo_borrar_tabs():
            self.delete(PorPasos)
            self.delete(PorBloques)
        self.caja_resultado.mostrar(texto_a_mostrar)

    def mostrar_pasos(self, debugger):
        self.caja_resultado.mostrar(debugger.resultado_final())

        self.pasos.mostrar(debugger)

        self.bloques.mostrar(debugger)

    def cargar_tabs(self):
        if self.debo_mostrar_tabs():
            self.tab_de_pasos = self.add(PorPasos)
            self.pasos = CajaDeIteracionesDePasosPorBloque(master=self.tab(PorPasos))
            self.pasos.pack(fill="both", expand=1)
            self.add(PorBloques)
            self.bloques = CajaDeIteracionesDeBloques(master=self.tab(PorBloques))
            self.bloques.pack(fill="both", expand=1)

    def debo_mostrar_tabs(self):
        return not self.debo_borrar_tabs()

    def debo_borrar_tabs(self):
        try:
            self.tab(PorBloques)
            return True
        except:
            return False

    def mostrar_pasos_md5(self, debugger):
        self.cargar_tabs()
        self.set_up_md5()
        self.mostrar_pasos(debugger)

    def set_up_md5(self):
        self.pasos.serializar_md5()
        self.bloques.serializar_md5()

    def mostrar_pasos_sha1(self, debugger):
        self.cargar_tabs()
        self.set_up_sha1()
        self.mostrar_pasos(debugger)

    def set_up_sha1(self):
        self.pasos.serializar_sha1()
        self.bloques.serializar_sha1()
