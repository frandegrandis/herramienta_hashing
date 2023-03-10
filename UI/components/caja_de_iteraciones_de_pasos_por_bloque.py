from customtkinter import CTkFrame

from UI.components.caja_de_texto import CajaDeTexto
from UI.components.selector_pasos_bloques import SelectorPasosBloques
from dominio.algoritmos.sha1.serializador import serializar_paso_sha1
from helpers.debugger import Debugger
from dominio.algoritmos.md5.serializador import serializar_paso_md5


class CajaDeIteracionesDePasosPorBloque(CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.selector_pasos_bloques = SelectorPasosBloques(master=self,
                                                           on_change=self.recargar)
        self.selector_pasos_bloques.pack()

        self.caja_de_texto = CajaDeTexto(self)
        self.caja_de_texto.pack(fill='both', expand=1)

    def mostrar(self, hasher_debugger):
        self.debugger:Debugger = hasher_debugger
        self.selector_pasos_bloques.cambiar_pasos(self.pasos())
        self.selector_pasos_bloques.cambiar_bloques(self.bloques())
        self.recargar()

    def recargar(self):
        resultado = self.serializar(self.debugger, paso=self.selector_pasos_bloques.paso(),
                                        bloque=self.selector_pasos_bloques.bloque())
        self.caja_de_texto.mostrar(resultado)

    def pasos(self):
        return [f"Paso {i}" for i in range(1, self.debugger.cantidad_pasos() + 1)]

    def bloques(self):
        return [f"Bloque {i}" for i in range(1, self.debugger.cantidad_bloques() + 1)]

    def serializar_md5(self):
        self.serializar = serializar_paso_md5

    def serializar_sha1(self):
        self.serializar = serializar_paso_sha1
