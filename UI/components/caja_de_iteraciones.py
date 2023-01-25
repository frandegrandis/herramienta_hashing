from customtkinter import CTkFrame

from UI.components.caja_de_texto import CajaDeTexto
from UI.components.selector_pasos_bloques import SelectorPasosBloques
from helpers.serializador_md5 import serializar_paso_md5, serializar_bloque_md5


class CajaDeIteraciones(CTkFrame):
    def __init__(self, debugger, mostrar_pasos=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.debugger = debugger
        if mostrar_pasos:
            self.serializar = serializar_paso_md5
        else:
            self.serializar = serializar_bloque_md5
        self.selector_pasos_bloques = SelectorPasosBloques(master=self, opciones_pasos=self.pasos(),
                                                           opciones_bloques=self.bloques(),
                                                           mostrar_pasos=mostrar_pasos,
                                                           on_change=self.recargar)
        self.selector_pasos_bloques.pack()

        self.caja_de_texto = CajaDeTexto(self)
        self.caja_de_texto.pack(fill='both', expand=1)

    def mostrar(self, hasher_debugger):
        self.debugger = hasher_debugger
        self.selector_pasos_bloques.cambiar_bloques(self.bloques())
        self.recargar()

    def recargar(self):
        resultado = self.serializar(self.debugger, paso=self.selector_pasos_bloques.paso(),
                                        bloque=self.selector_pasos_bloques.bloque())
        self.caja_de_texto.mostrar(resultado)

    def pasos(self):
        return [f"Paso {i}" for i in range(1, 65)]

    def bloques(self):
        return [f"Bloque {i}" for i in range(1, self.debugger.cantidad_bloques() + 1)]
