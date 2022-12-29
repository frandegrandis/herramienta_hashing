from typing import Callable, Union

from customtkinter import CTkFrame, CTkButton, CTkEntry

from helpers.utilidades import aumentar_bits, reducir_bits


class InputConAumentoDeBits(CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: Union[int, float] = 1,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = CTkButton(self, text="-1 bit", width=height - 6, height=height - 6,
                                         command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = CTkEntry(self, width=width - (2 * height), height=height - 6, border_width=0)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = CTkButton(self, text="+1 bit", width=height - 6, height=height - 6,
                                    command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

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