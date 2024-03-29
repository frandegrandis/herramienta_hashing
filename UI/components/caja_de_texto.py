from customtkinter import CTkTextbox

from UI.Estado import Estado


class CajaDeTexto(CTkTextbox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, state='disabled', font=('Courier New', Estado.tamanio_letra), wrap="word", **kwargs)

    def insert(self, index, text, tags=None):
        self.configure(state='normal')
        super().insert(index, text, tags)
        self.configure(state='disabled')

    def mostrar(self, texto_a_mostrar):
        self.vaciar()
        self.insert("0.0", texto_a_mostrar)

    def vaciar(self):
        self.configure(state='normal')
        super().delete("0.0", "end")
        self.configure(state='disabled')

    def append(self, texto_a_mostrar):
        texto_actual = self.get("0.0", "end")
        hay_que_limpiar = not any(
            funcion_de_hash in texto_actual for funcion_de_hash in ["MD5", "SHA1", "SHA256", "SHA512"])
        if self.get("0.0") == '\n' or hay_que_limpiar:
            self.mostrar(texto_a_mostrar)
            return
        self.insert("end", "\n" + texto_a_mostrar)

    def actualizar_letra(self):
        self.configure(font=('Courier New', Estado.tamanio_letra))
