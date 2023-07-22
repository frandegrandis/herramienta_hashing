from customtkinter import CTkTextbox


class CajaDeTexto(CTkTextbox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, state='disabled', font=('Courier New', 14), wrap="word", **kwargs)

    def insert(self, index, text, tags=None):
        self.configure(state='normal')
        super().insert(index, text, tags)
        self.configure(state='disabled')

    def mostrar(self, texto_a_mostrar):
        self.configure(state='normal')
        self.vaciar()
        super().insert("0.0", texto_a_mostrar)
        self.configure(state='disabled')

    def vaciar(self):
        super().delete("0.0", "end")

    def append(self, texto_a_mostrar):
        texto_actual = self.get("0.0","end")
        hay_que_limpiar = not any(funcion_de_hash in texto_actual for funcion_de_hash in ["MD5", "SHA1", "SHA256", "SHA512"])
        if self.get("0.0") == '\n' or hay_que_limpiar:
            self.mostrar(texto_a_mostrar)
            return
        self.configure(state='normal')
        super().insert("end","\n" + texto_a_mostrar)
        self.configure(state='disabled')
