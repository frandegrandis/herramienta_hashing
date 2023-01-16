from customtkinter import CTkFrame

from UI.components.caja_de_texto import CajaDeTexto
from helpers.serializador_md5 import serializar_iteracion_md5
from UI.selector_pasos_bloques import SelectorPasosBloques


class CajaDeIteraciones(CTkFrame):
    def __init__(self, debugger, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.debugger = debugger
        self.selector_pasos_bloques = SelectorPasosBloques(master=self, opciones_pasos=self.pasos(),
                                                           opciones_bloques=self.bloques(),
                                                           on_change=self.recargar)
        self.selector_pasos_bloques.pack()

        self.caja_de_texto = CajaDeTexto(self)
        self.caja_de_texto.pack(fill='both', expand=1)

    def pasos(self):
        return [f"Paso {i}" for i in range(1, 65)]

    def mostrar(self, hasher_debugger):
        self.debugger = hasher_debugger
        self.selector_pasos_bloques.cambiar_bloques(self.bloques())
        self.recargar()

    def recargar(self):
        resultado = serializar_iteracion_md5(self.debugger, paso=self.selector_pasos_bloques.paso(), bloque=1)
        self.caja_de_texto.mostrar(resultado)

    def bloques(self):
        return [f"Bloque {i}" for i in range(1, self.debugger.cantidad_bloques() + 1)]
