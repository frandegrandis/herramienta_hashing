from customtkinter import CTkTabview

from UI.components.caja_de_iteraciones import CajaDeIteraciones
from UI.components.caja_de_texto import CajaDeTexto

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
        if self.debo_mostrar_tabs():
            self.tab_de_pasos = self.add(PorPasos)
            self.pasos = CajaDeIteraciones(master=self.tab(PorPasos), debugger= debugger)
            self.pasos.pack(fill="both", expand=1)
            self.add(PorBloques)
            self.bloques = CajaDeIteraciones(master=self.tab(PorBloques), debugger= debugger, mostrar_pasos = False)
            self.bloques.pack(fill="both", expand=1)

        self.caja_resultado.mostrar(debugger.resultado_final())

        self.pasos.mostrar(debugger)

        self.bloques.mostrar(debugger)

    def debo_mostrar_tabs(self):
        return not self.debo_borrar_tabs()

    def debo_borrar_tabs(self):
        try:
            self.tab(PorBloques)
            return True
        except:
            return False
