from customtkinter import CTkFrame, CTkOptionMenu


class SelectorPasosBloques(CTkFrame):
    def __init__(self, opciones_pasos, opciones_bloques, on_change, mostrar_pasos=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._paso = opciones_pasos[0]
        self._bloque = opciones_bloques[0]
        self.on_change = on_change
        if mostrar_pasos:
            self.set_up_pasos(opciones_pasos)
        self.set_up_bloques(opciones_bloques)

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
        self.selector_bloque.destroy()
        self.set_up_bloques(opciones_bloques)

    def bloque(self):
        return int(self._bloque.split(" ")[1])
