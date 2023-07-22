from customtkinter import CTk, CTkFrame, CTkButton

from UI.components.input_con_aumento_de_bits import InputConAumentoDeBits
from UI.mostrador_hash import MostradorHash
from controllers.hasher_controller import HasherController


class PantallaPrincipal(CTk):
    def __init__(self):
        super().__init__()

        self.title("Remake CriptoRes")
        self.minsize(1280, 720)

        self.configurar_grilla()

        top_frame = CTkFrame(master=self)
        top_frame.grid(column=0, row=0, sticky='nsew')
        self.input_a_hashear = InputConAumentoDeBits(master=top_frame)
        self.input_a_hashear.pack(fill="x")
        self.resultado_de_hash = MostradorHash(master=top_frame)
        self.resultado_de_hash.pack(fill="both", expand=1)
        self.botonera()

    def botonera(self):
        bottom_frame = CTkFrame(master=self)
        bottom_frame.grid(column=0, row=1)
        CTkButton(master=bottom_frame, text="Hash MD5", command=self.calcular_hash_md5).grid(column=0, row=0, padx=20, pady=10)
        CTkButton(master=bottom_frame, text="Hash SHA1", command=self.calcular_hash_sha1).grid(column=1, row=0, padx=20, pady=10)
        CTkButton(master=bottom_frame, text="Hash SHA256", command=self.calcular_hash_sha256).grid(column=2, row=0, padx=20, pady=10)
        CTkButton(master=bottom_frame, text="Hash SHA512", command=self.calcular_hash_sha512).grid(column=3, row=0, padx=20, pady=10)
        CTkButton(master=bottom_frame, text="Debug MD5", command=self.debuguear_hash_md5).grid(column=0, row=1, padx=20, pady=10)
        CTkButton(master=bottom_frame, text="Debug SHA1", command=self.debuguear_hash_sha1).grid(column=1, row=1, padx=20, pady=10)
        CTkButton(master=bottom_frame, text="Debug SHA256", command=self.debuguear_hash_sha256).grid(column=2, row=1, padx=20, pady=10)
        CTkButton(master=bottom_frame, text="Debug SHA512", command=self.debuguear_hash_sha512).grid(column=3, row=1, padx=20, pady=10)

    def calcular_hash_md5(self):
        self._obtener_hash(HasherController().calcular_hash_md5, "MD5")

    def calcular_hash_sha1(self):
        self._obtener_hash(HasherController().calcular_hash_sha1, "SHA1")

    def calcular_hash_sha256(self):
        self._obtener_hash(HasherController().calcular_hash_sha256, "SHA256")

    def calcular_hash_sha512(self):
        self._obtener_hash(HasherController().calcular_hash_sha512, "SHA512")

    def debuguear_hash_md5(self):
        self.resultado_de_hash.mostrar_pasos_md5(HasherController().debugguear_md5(self.valor_a_hashear()))

    def debuguear_hash_sha1(self):
        self.resultado_de_hash.mostrar_pasos_sha1(HasherController().debugguear_sha1(self.valor_a_hashear()))

    def debuguear_hash_sha256(self):
        self.resultado_de_hash.mostrar_pasos_sha256(HasherController().debugguear_sha256(self.valor_a_hashear()))

    def debuguear_hash_sha512(self):
        self.resultado_de_hash.mostrar_pasos_sha512(HasherController().debugguear_sha512(self.valor_a_hashear()))

    def configurar_grilla(self):
        self.grid_rowconfigure(0, weight=9)
        self.grid_rowconfigure(1)
        self.grid_columnconfigure((0), weight=1)

    def alto_pantalla(self):
        return self.winfo_width()

    def _obtener_hash(self, calculo_hash, algoritmo):
        valor_a_hashear = self.valor_a_hashear()
        self.resultado_de_hash.append_texto(f"Aplicando {algoritmo} sobre {valor_a_hashear}: {calculo_hash(valor_a_hashear)}")

    def valor_a_hashear(self):
        if self.input_a_hashear.archivo_seleccionado:
            valor_a_hashear = open(self.input_a_hashear.get(), "rb")
        else:
            valor_a_hashear = self.input_a_hashear.get()
        return valor_a_hashear
