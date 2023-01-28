from dominio.algoritmos.md5.md5_operations import F, G, H, I
from helpers.utilidades import suma_modular
from helpers.utilidades_UI import mostrar_32_bits_centrados_con_espacio, nombre_clase_de, hex_string_de, crear_linea


def mostrar_operacion_I(B, C, D, resultado):
    resultado += f"\n\n    {mostrar_32_bits_centrados_con_espacio(B | (~D))} = (B or (not D))"
    resultado += f"\nXOR {mostrar_32_bits_centrados_con_espacio(C)} = C"
    return resultado


def mostrar_operacion_H(B, C, D, resultado):
    resultado += f"\n\n    {mostrar_32_bits_centrados_con_espacio(B)} = B"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(C)} = C"
    resultado += f"\nXOR {mostrar_32_bits_centrados_con_espacio(D)} = D"
    return resultado


def mostrar_operacion_G(B, C, D, resultado):
    resultado += f"\n\n    {mostrar_32_bits_centrados_con_espacio(B & D)} = (B and D)"
    resultado += f"\n OR {mostrar_32_bits_centrados_con_espacio(C & ~D)} = (C and (not D))"
    return resultado


def mostrar_operacion_F(B, C, D, resultado):
    resultado += f"\n\n    {mostrar_32_bits_centrados_con_espacio(B & C)} = (B and C)"
    resultado += f"\n OR {mostrar_32_bits_centrados_con_espacio((~B) & D)} = ((not B) and D)"
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
    resultado += f"\n\nA = {mostrar_32_bits_centrados_con_espacio(A)} = {hex_string_de(A)}"
    resultado += f"\nB = {mostrar_32_bits_centrados_con_espacio(B)} = {hex_string_de(B)}"
    resultado += f"\nC = {mostrar_32_bits_centrados_con_espacio(C)} = {hex_string_de(C)}"
    resultado += f"\nD = {mostrar_32_bits_centrados_con_espacio(D)} = {hex_string_de(D)}"
    resultado = mostrar_operacion_correspondiente(B, C, D, operacion, resultado)
    resultado += crear_linea()
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(operacion.aplicar_a(B, C, D))} = {nombre_clase_de(operacion)}(B,C,D)"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(A)} = Valor de A"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(iteracion.palabra_a_sumar)} = Palabra {debugger.numero_de_palabra_a_sumar_en_paso(paso=paso)} del bloque {bloque}"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(iteracion.constante_s)} = Valor de constante Nº {paso}"
    resultado += crear_linea()
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(iteracion.suma_inicial())}"
    resultado += crear_linea()
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(iteracion.rotacion())} Rotado a izquierda {iteracion.bits_a_rotar} bits"
    resultado += f"\n+   {mostrar_32_bits_centrados_con_espacio(B)} = Valor de B"
    resultado += crear_linea()
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(iteracion.suma_final())} Es ahora la palabra B"
    resultado += f"\n\nLa palabra D pasa a ocupar el lugar de A\nLa palabra C pasa a ocupar el lugar de D\nLa " \
                 f"palabra B pasa a ocupar el lugar de C"
    # TODO: Falta mostrar la actualizacion final!
    return resultado


def mostrar_operacion_correspondiente(B, C, D, operacion, resultado):
    if isinstance(operacion, F):
        resultado = mostrar_operacion_F(B, C, D, resultado)
    if isinstance(operacion, G):
        resultado = mostrar_operacion_G(B, C, D, resultado)
    if isinstance(operacion, H):
        resultado = mostrar_operacion_H(B, C, D, resultado)
    if isinstance(operacion, I):
        resultado = mostrar_operacion_I(B, C, D, resultado)
    return resultado


def serializar_bloque_md5(debugger, bloque):
    iteracion = debugger.obtener_iteracion(paso=1, bloque=bloque)
    vueltas = ["Primera vuelta", "Segunda vuelta", "Tercera vuelta", "Cuarta vuelta"]
    A_inicial, B_inicial, C_inicial, D_inicial = iteracion.valores_iniciales()
    resultado = f"Valores iniciales:\n"
    resultado += f"A= {hex_string_de(A_inicial)}\n"
    resultado += f"B= {hex_string_de(B_inicial)}\n"
    resultado += f"C= {hex_string_de(C_inicial)}\n"
    resultado += f"D= {hex_string_de(D_inicial)}\n"
    resultado += f"\nPaso i:\t A B C D\n\n"
    for paso in range(1, debugger.cantidad_pasos() + 1):
        if (paso - 1) % 16 == 0:
            resultado += vueltas[paso // 16] + '\n'
        A, B, C, D = map(hex_string_de, debugger.valores_finales(paso, bloque))
        resultado += f"Paso {paso:^3}: {A} {B} {C} {D}\n"
    A, B, C, D = debugger.valores_finales(debugger.cantidad_pasos(), bloque)
    resultado += f"\nActualización final: (valores iniciales + valores paso 64)\n"
    resultado += f"\t  {hex_string_de(A_inicial)} {hex_string_de(B_inicial)} {hex_string_de(C_inicial)} {hex_string_de(D_inicial)}\n"
    resultado += f"\t+ {hex_string_de(A)} {hex_string_de(B)} {hex_string_de(C)} {hex_string_de(D)}\n"
    resultado += f"\t{'-' * (40)}\n"
    resultado += f"\t  {hex_string_de(suma_modular(A_inicial, A))} {hex_string_de(suma_modular(B_inicial, B))} {hex_string_de(suma_modular(C_inicial, C))} {hex_string_de(suma_modular(D_inicial, D))}"
    return resultado
