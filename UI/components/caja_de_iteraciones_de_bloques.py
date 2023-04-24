from customtkinter import CTkFrame

from UI.components.caja_de_texto import CajaDeTexto
from UI.components.selector_pasos_bloques import SelectorPasosBloques
from dominio.algoritmos.sha1.serializador import serializar_bloque_sha1
from dominio.algoritmos.md5.serializador import serializar_bloque_md5
from dominio.algoritmos.sha256.serializador import serializar_bloque_sha256
from dominio.algoritmos.sha512.serializador import serializar_bloque_sha512


class CajaDeIteracionesDeBloques(CTkFrame):
    def __init__(self, serializer, debugger, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.selector_pasos_bloques = SelectorPasosBloques(master=self,
                                                           on_change=self.recargar)
        self.selector_pasos_bloques.pack()

        self.caja_de_texto = CajaDeTexto(self)
        self.caja_de_texto.pack(fill='both', expand=1)

        self.serializar = serializer
        self.mostrar(debugger)

    def mostrar(self, hasher_debugger):
        self.debugger = hasher_debugger
        self.selector_pasos_bloques.cambiar_bloques(self.bloques())
        self.recargar()

    def recargar(self):
        resultado = self.serializar(self.debugger, bloque=self.selector_pasos_bloques.bloque())
        self.caja_de_texto.mostrar(resultado)

    def bloques(self):
        return [f"Bloque {i}" for i in range(1, self.debugger.cantidad_bloques() + 1)]

    def serializar_md5(self):
        self.serializar = serializar_bloque_md5

    def serializar_sha1(self):
        self.serializar = serializar_bloque_sha1

    def serializar_sha256(self):
        self.serializar = serializar_bloque_sha256

    @classmethod
    def sha256(cls, master,debugger):
        return cls(master=master, serializer=serializar_bloque_sha256, debugger=debugger)

    @classmethod
    def sha1(cls, master,debugger):
        return cls(master=master, serializer=serializar_bloque_sha1, debugger=debugger)

    @classmethod
    def md5(cls, master, debugger):
        return cls(master=master, serializer=serializar_bloque_md5, debugger=debugger)

    @classmethod
    def sha512(cls, master, debugger):
        return cls(master=master, serializer=serializar_bloque_sha512, debugger=debugger)
