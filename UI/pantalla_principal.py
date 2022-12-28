from customtkinter import CTk, CTkFrame, CTkButton
from math import ceil

from UI.caja_de_texto import CajaDeTexto
from UI.zarasa import FloatSpinbox


class PantallaPrincipal(CTk):
    def __init__(self):
        super().__init__()

        self.title("Hashing")
        self.minsize(1080, 600)

        self.configurar_grilla()

        top_frame = CTkFrame(master=self, fg_color="green")
        top_frame.grid(column=0, row=0, sticky='nsew')
        self.input_a_hashear = FloatSpinbox(master=top_frame)
        self.input_a_hashear.pack()
        self.resultado_de_hash = CajaDeTexto(master=top_frame)
        self.resultado_de_hash.pack()

        bottom_frame = CTkFrame(master=self, fg_color="blue")
        bottom_frame.grid(column=0, row=1, sticky='nsew')
        boton = CTkButton(master=bottom_frame, text="Hash MD5", command=self.button_callback)
        boton.pack()

    def button_callback(self):
        print(self.input_a_hashear.get())
        self.resultado_de_hash.mostrar(str(self.input_a_hashear.get()))

    def configurar_grilla(self):
        alto_pantalla = self.alto_pantalla()
        maxima_particion_de_pantalla = 10
        parte_superior_pantalla = 8 / maxima_particion_de_pantalla
        parte_inferior_pantalla = 1 / maxima_particion_de_pantalla
        self.grid_rowconfigure(0, weight=ceil(alto_pantalla * parte_superior_pantalla))
        self.grid_rowconfigure(1, weight=ceil(alto_pantalla * parte_inferior_pantalla))
        self.grid_columnconfigure((0), weight=1)

    def alto_pantalla(self):
        return self.winfo_width()
