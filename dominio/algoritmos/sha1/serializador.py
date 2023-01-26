from dominio.algoritmos.operaciones_sha1 import F, G, H, I
from helpers.operaciones_bit_a_bit import rotar_izquierda
from helpers.utilidades_UI import nombre_clase_de, mostrar_32_bits_centrados_con_espacio, hex_string_de, crear_linea, \
    bit_string_de


def serializar_bloque_sha1(debugger, paso, bloque):
    return "Soy un bloque de sha1"


def serializar_paso_sha1(debugger, paso, bloque):
    iteracion = debugger.obtener_iteracion(paso=paso, bloque=bloque)
    operacion = iteracion.operacion
    A, B, C, D, E = iteracion.valores_iniciales()
    palabra_a_sumar = f"\n    {mostrar_32_bits_centrados_con_espacio(iteracion.palabra_a_sumar)} = Palabra {paso} del bloque {bloque}"
    resultado = operacion.to_string() + "\n"
    resultado += f"A´= E + {nombre_clase_de(operacion)}(B, C, D) + (A <<< 5) + M[i] + K[j]\n"
    resultado += "E´= D; D´= C; C´= (B <<< 30); B´= A\n"
    resultado += f"\nA = {mostrar_32_bits_centrados_con_espacio(A)} = {hex_string_de(A)}"
    resultado += f"\nB = {mostrar_32_bits_centrados_con_espacio(B)} = {hex_string_de(B)}"
    resultado += f"\nC = {mostrar_32_bits_centrados_con_espacio(C)} = {hex_string_de(C)}"
    resultado += f"\nD = {mostrar_32_bits_centrados_con_espacio(D)} = {hex_string_de(D)}"
    resultado += f"\nD = {mostrar_32_bits_centrados_con_espacio(E)} = {hex_string_de(E)}"
    resultado += mostrar_operacion_correspondiente(B, C, D, operacion)
    resultado += crear_linea()
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(operacion.aplicar_a(B, C, D))} = {nombre_clase_de(operacion)}(B,C,D)"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(E)} = Valor de E"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(rotar_izquierda(A,5))} = A rotado a izq. 5 bits"
    resultado += palabra_a_sumar
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(iteracion.constante_k)} = Constante {hex_string_de(iteracion.constante_k)}"
    resultado += crear_linea()
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(iteracion.suma_final())} = Es ahora la palabra A\n"
    resultado += f"\nLa palabra D pasa a ocupar el lugar de E"
    resultado += f"\nLa palabra C pasa a ocupar el lugar de D"
    resultado += f"\nLa palabra B rotada 30 posiciones a la izquierda:\n"
    resultado += f"    {bit_string_de(rotar_izquierda(B,30))} Es ahora la palabra C"
    resultado += f"\nLa palabra A pasa a ocupar el lugar de B"
    return resultado


def mostrar_operacion_F(B, C, D):
    resultado = f"\n\n    {mostrar_32_bits_centrados_con_espacio(B & C)} = (B and C)"
    resultado += f"\n OR {mostrar_32_bits_centrados_con_espacio((~B) & D)} = ((not B) and D)"
    return resultado


def mostrar_operacion_G(B, C, D):
    pass


def mostrar_operacion_H(B, C, D):
    pass


def mostrar_operacion_I(B, C, D):
    pass


def mostrar_operacion_correspondiente(B, C, D, operacion):
    if isinstance(operacion, F):
        return mostrar_operacion_F(B, C, D)
    if isinstance(operacion, G):
        return mostrar_operacion_G(B, C, D)
    if isinstance(operacion, H):
        return mostrar_operacion_H(B, C, D)
    if isinstance(operacion, I):
        return mostrar_operacion_I(B, C, D)
