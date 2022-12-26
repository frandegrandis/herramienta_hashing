from customtkinter import CTkFrame, CTkTextbox


class CajaDeTexto(CTkTextbox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,state= 'disabled',  **kwargs)
        
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