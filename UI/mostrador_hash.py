from customtkinter import CTkFrame, CTkTabview

from UI.components.caja_de_texto import CajaDeTexto

Resultado = "Resultado"
PorBloques = "Debug por bloques"
PorPasos = "Debug por pasos"


class MostradorHash(CTkTabview):
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)
        self.add(Resultado)
        self.caja_resultado = CajaDeTexto(master=self.tab(Resultado))
        self.caja_resultado.pack(fill = "both", expand = 1)

    def mostrar_texto(self, texto_a_mostrar):
        if self.debo_borrar_tabs():
            self.delete(PorPasos)
            self.delete(PorBloques)
        self.caja_resultado.mostrar(texto_a_mostrar)

    def mostrar_pasos(self, _lista_de_pasos):
        if self.debo_mostrar_tabs():
            self.add(PorPasos)
            self.add(PorBloques)
        # TODO: Mostrar la lista de pasos a hashear nueva

    def debo_mostrar_tabs(self):
        return not self.debo_borrar_tabs()

    def debo_borrar_tabs(self):
        try:
            self.tab(PorBloques)
            return True
        except:
            return False
