from helpers.md5_operations import F, G, H, I
from helpers.utilidades import suma_modular


def nombre_clase_de(objeto):
    return objeto.__class__.__name__


def bit_string_de(numero):
    a = bin(abs(numero))[2::]
    if len(a) >= 32:
        return a
    else:
        while len(a) < 32:
            a = "0" + a
        return a


def hex_string_de(numero):
    return hex(numero)[2::].upper()


def mostrar_operacion_I(B, C, D, resultado):
    resultado += f"\n\n    {bit_string_de(B | (~D)):^40} = (B or (not D))"
    resultado += f"\nXOR {bit_string_de(C):^40} = C"
    return resultado


def mostrar_operacion_H(B, C, D, resultado):
    resultado += f"\n\n    {bit_string_de(B):^40} = B"
    resultado += f"\n    {bit_string_de(C):^40} = C"
    resultado += f"\nXOR {bit_string_de(D):^40} = D"
    return resultado


def mostrar_operacion_G(B, C, D, resultado):
    resultado += f"\n\n    {bit_string_de(B & D):^40} = (B and D)"
    resultado += f"\n OR {bit_string_de(C & ~D):^40} = (C and (not D))"
    return resultado


def mostrar_operacion_F(B, C, D, resultado):
    resultado += f"\n\n    {bit_string_de(B & C):^40} = (B and C)"
    resultado += f"\n OR {bit_string_de((~B) & D):^40} = ((not B) and D)"
    return resultado


def serializar_paso_md5(debugger, paso, bloque):
    iteracion = debugger.obtener_iteracion(paso=paso, bloque=bloque)
    operacion = iteracion.operacion
    A = iteracion.valores_iniciales()[0]
    B = iteracion.valores_iniciales()[1]
    C = iteracion.valores_iniciales()[2]
    D = iteracion.valores_iniciales()[3]
    resultado = operacion.to_string() + "\n"
    resultado += f"B´= B + ((A + {nombre_clase_de(operacion)}(B, C, D) + M[i] + K[j]) <<< S)"
    resultado += "\nA´= D; D´:= C; C´:= B"
    resultado += f"\n\nA = {bit_string_de(A):^40} = {hex_string_de(A)}"
    resultado += f"\n\nB = {bit_string_de(B):^40} = {hex_string_de(B)}"
    resultado += f"\n\nC = {bit_string_de(C):^40} = {hex_string_de(C)}"
    resultado += f"\n\nD = {bit_string_de(D):^40} = {hex_string_de(D)}"
    if isinstance(operacion, F):
        resultado = mostrar_operacion_F(B, C, D, resultado)
    if isinstance(operacion, G):
        resultado = mostrar_operacion_G(B, C, D, resultado)
    if isinstance(operacion, H):
        resultado = mostrar_operacion_H(B, C, D, resultado)
    if isinstance(operacion, I):
        resultado = mostrar_operacion_I(B, C, D, resultado)
    resultado += f"\n------------------------------------------------------------------------"
    resultado += f"\n    {bit_string_de(operacion.aplicar_a(B, C, D)):^40} = {nombre_clase_de(operacion)}(B,C,D)"
    resultado += f"\n    {bit_string_de(A):^40} = Valor de A"
    resultado += f"\n    {bit_string_de(iteracion.palabra_a_sumar):^40} = Palabra {debugger.numero_de_palabra_a_sumar_en_paso(paso=paso)} del bloque {bloque}"
    resultado += f"\n    {bit_string_de(iteracion.constante_s):^40} = Valor de constante Nº {paso}"
    resultado += f"\n------------------------------------------------------------------------"
    resultado += f"\n    {bit_string_de(iteracion.suma_inicial()):^40}"
    resultado += f"\n------------------------------------------------------------------------"
    resultado += f"\n    {bit_string_de(iteracion.rotacion()):^40} Rotado a izquierda {iteracion.bits_a_rotar} bits"
    resultado += f"\n+   {bit_string_de(B):^40} = Valor de B"
    resultado += f"\n------------------------------------------------------------------------"
    resultado += f"\n    {bit_string_de(iteracion.suma_final()):^40} Es ahora la palabra B"
    resultado += f"\n\nLa palabra D pasa a ocupar el lugar de A\nLa palabra C pasa a ocupar el lugar de D\nLa " \
                 f"palabra B pasa a ocupar el lugar de C"
    # TODO: Falta mostrar la actualizacion final!xy[
    return resultado


def serializar_bloque_md5(debugger, paso, bloque):
    iteracion = debugger.obtener_iteracion(paso=1, bloque=bloque)
    cantidad_pasos_md5 = 64
    vueltas = ["Primera vuelta", "Segunda vuelta", "Tercera vuelta", "Cuarta vuelta"]
    A_inicial, B_inicial, C_inicial, D_inicial = iteracion.valores_iniciales()
    resultado = f"Valores iniciales:\n"
    resultado += f"A= {hex_string_de(A_inicial)}\n"
    resultado += f"B= {hex_string_de(B_inicial)}\n"
    resultado += f"C= {hex_string_de(C_inicial)}\n"
    resultado += f"D= {hex_string_de(D_inicial)}\n"
    resultado += f"\nPaso i:\t A B C D\n\n"
    for paso in range(1, cantidad_pasos_md5 + 1):
        if (paso - 1) % 16 == 0:
            resultado += vueltas[paso // 16] + '\n'
        A, B, C, D = map(hex_string_de, debugger.valores_finales(paso, bloque))
        resultado += f"Paso {paso:^3}: {A} {B} {C} {D}\n"
    A, B, C, D = debugger.valores_finales(cantidad_pasos_md5, bloque)
    resultado += f"\nActualización final: (valores iniciales + valores paso 64)\n"
    resultado += f"\t  {hex_string_de(A_inicial)} {hex_string_de(B_inicial)} {hex_string_de(C_inicial)} {hex_string_de(D_inicial)}\n"
    resultado += f"\t+ {hex_string_de(A)} {hex_string_de(B)} {hex_string_de(C)} {hex_string_de(D)}\n"
    resultado += f"\t{'-' * (40)}\n"
    resultado += f"\t  {hex_string_de(suma_modular(A_inicial, A))} {hex_string_de(suma_modular(B_inicial, B))} {hex_string_de(suma_modular(C_inicial, C))} {hex_string_de(suma_modular(D_inicial, D))}"
    return resultado
