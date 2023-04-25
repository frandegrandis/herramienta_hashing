from tkinter.filedialog import askopenfilename
from typing import Callable, Union

from customtkinter import CTkFrame, CTkButton, CTkEntry

from helpers.events import Events
from helpers.utilidades import aumentar_bits, reducir_bits


class InputConAumentoDeBits(CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: Union[int, float] = 1,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.archivo_seleccionado = False
        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2, 3), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = CTkButton(self, text="-1 bit", width=height - 6, height=height - 6,
                                         command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = CTkEntry(self, border_width=0)
        self.entry.bind(Events.on_change.value, self._archivo_deseleccionado)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=10, sticky="ew")

        self.add_button = CTkButton(self, text="+1 bit", width=height - 6, height=height - 6,
                                    command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        self.boton_archivo = CTkButton(self, text="Archivo", width=height - 6, height=height - 6,
                                       command=self.cargar_archivo)
        self.boton_archivo.grid(row=0, column=3, padx=(3, 3), pady=3)

        # default value
        self.entry.insert(0, "")

    def add_button_callback(self):
        try:
            self.mostrar(aumentar_bits(self.get(), 1))
        except ValueError:
            return

    def mostrar(self, value):
        self.entry.delete(0, "end")
        self.entry.insert(0, value)

    def subtract_button_callback(self):
        try:
            self.mostrar(reducir_bits(self.get(), 1))
        except ValueError:
            return

    def get(self):
        try:
            return self.entry.get()
        except ValueError:
            return None

    def cargar_archivo(self):
        path_archivo = askopenfilename()
        self._archivo_seleccionado()
        self.mostrar(path_archivo)

    def _archivo_seleccionado(self):
        self.archivo_seleccionado = True
        self.add_button.configure(state="disabled")
        self.subtract_button.configure(state="disabled")

    def _archivo_deseleccionado(self, _event=None):
        if not self.archivo_seleccionado:
            return
        self.archivo_seleccionado = False
        self.add_button.configure(state="normal")
        self.subtract_button.configure(state="normal")
