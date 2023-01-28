from customtkinter import CTkFrame, CTkOptionMenu


class SelectorPasosBloques(CTkFrame):
    def __init__(self, on_change, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._paso = "Paso 1"
        self._bloque = "Bloque 1"
        self.on_change = on_change

    def set_up_pasos(self, opciones_pasos):
        self.selector_pasos = CTkOptionMenu(master=self,
                                            values=opciones_pasos,
                                            command=self.cambio_paso)
        self.selector_pasos.grid(row=0, column=0)

    def set_up_bloques(self, opciones_bloques):
        self.selector_bloque = CTkOptionMenu(master=self,
                                             values=opciones_bloques,
                                             command=self.cambio_bloque)
        self.selector_bloque.grid(row=0, column=1)

    def cambio_paso(self, choice):
        self._paso = choice
        self.on_change()

    def cambio_bloque(self, choice):
        self._bloque = choice
        self.on_change()

    def paso(self):
        return int(self._paso.split(" ")[1])

    def cambiar_bloques(self, opciones_bloques):
        try:
            self.selector_bloque.destroy()
        except:
            pass
        self.set_up_bloques(opciones_bloques)

    def bloque(self):
        return int(self._bloque.split(" ")[1])

    def cambiar_pasos(self, opciones_paso):
        try:
            self.selector_bloque.destroy()
        except:
            pass
        self.set_up_pasos(opciones_paso)
