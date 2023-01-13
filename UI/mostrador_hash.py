from customtkinter import CTkFrame, CTkTabview

from UI.components.caja_de_texto import CajaDeTexto

Resultado = "Resultado"
PorBloques = "Debug por bloques"
PorPasos = "Debug por pasos"


def nombre_clase_de(objeto):
    return objeto.__class__.__name__


def bit_string_de(numero):
    a = bin(numero)[2::]
    if len(a) == 32:
        return a
    else:
        while len(a) < 32:
            a = "0" + a
        return a


def hex_string_de(numero):
    return hex(numero)[2::].upper()


class MostradorHash(CTkTabview):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tab_de_pasos = None
        self.add(Resultado)
        self.caja_resultado = CajaDeTexto(master=self.tab(Resultado))
        self.caja_resultado.pack(fill="both", expand=1)

    def mostrar_texto(self, texto_a_mostrar):
        if self.debo_borrar_tabs():
            self.delete(PorPasos)
            self.delete(PorBloques)
        self.caja_resultado.mostrar(texto_a_mostrar)

    def mostrar_pasos(self, debugger):
        if self.debo_mostrar_tabs():
            self.tab_de_pasos = self.add(PorPasos)
            self.pepe = CajaDeTexto(master=self.tab(PorPasos))
            self.pepe.pack(fill="both", expand=1)
            self.add(PorBloques)
        # TODO: Mostrar la lista de pasos a hashear nueva
        self.caja_resultado.mostrar(debugger.resultado_final())

        resultado = ""
        paso = 1
        bloque = 1
        iteracion = debugger.obtener_iteracion(paso=paso, bloque=bloque)
        operacion = iteracion.operacion
        A = debugger.valores_iniciales(paso, bloque)[0]
        B = debugger.valores_iniciales(paso, bloque)[1]
        C = debugger.valores_iniciales(paso, bloque)[2]
        D = debugger.valores_iniciales(paso, bloque)[3]

        resultado += operacion.to_string() + "\n"
        resultado += f"B´= B + ((A + {nombre_clase_de(operacion)}(B, C, D) + M[i] + K[j]) <<< S)"
        resultado += "\nA´= D; D´:= C; C´:= B"
        resultado += f"\n\nA = {bit_string_de(A):^40} = {hex_string_de(A)}"
        resultado += f"\n\nB = {bit_string_de(B):^40} = {hex_string_de(B)}"
        resultado += f"\n\nC = {bit_string_de(C):^40} = {hex_string_de(C)}"
        resultado += f"\n\nD = {bit_string_de(D):^40} = {hex_string_de(D)}"
        resultado += f"\n\n    {bit_string_de(B & C):^40} = (B and C)"
        resultado += f"\n OR {bit_string_de((~B) & D):^40} = ((not B) and D)"
        resultado += f"\n------------------------------------------------------------------------"
        resultado += f"\n    {bit_string_de(operacion.aplicar_a(B,C,D)):^40} = F(B,C,D)"
        resultado += f"\n    {bit_string_de(A):^40} = Valor de A"
        resultado += f"\n    {bit_string_de(iteracion.palabra_a_sumar):^40} = Palabra 0 del bloque 1"
        resultado += f"\n    {bit_string_de(iteracion.constante_s):^40} = Valor de constante Nº 0"
        resultado += f"\n------------------------------------------------------------------------"
        resultado += f"\n    {bit_string_de(iteracion.suma_inicial()):^40}"
        resultado += f"\n------------------------------------------------------------------------"
        resultado += f"\n    {bit_string_de(iteracion.rotacion()):^40} Rotado a izquierda 7 bits"
        resultado += f"\n+   {bit_string_de(B):^40} = Valor de B"
        resultado += f"\n------------------------------------------------------------------------"
        resultado += f"\n    {bit_string_de(iteracion.suma_final()):^40} Es ahora la palabra B"
        resultado += f"\n\nLa palabra D pasa a ocupar el lugar de A\nLa palabra C pasa a ocupar el lugar de D\nLa " \
                     f"palabra B pasa a ocupar el lugar de C"


        self.pepe.mostrar(resultado)

    def debo_mostrar_tabs(self):
        return not self.debo_borrar_tabs()

    def debo_borrar_tabs(self):
        try:
            self.tab(PorBloques)
            return True
        except:
            return False
