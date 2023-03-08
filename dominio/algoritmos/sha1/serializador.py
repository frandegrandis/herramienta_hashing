from dominio.algoritmos.serializador_de_bloque import serializar_bloque
from dominio.algoritmos.sha1.operaciones_sha1 import F, G, H, I
from helpers.debugger import Debugger
from helpers.operaciones_bit_a_bit import rotar_izquierda
from helpers.utilidades_UI import nombre_clase_de, mostrar_32_bits_centrados_con_espacio, hex_string_de, crear_linea, \
    bit_string_de


def serializar_bloque_sha1(debugger, bloque):
    return serializar_bloque(debugger=debugger, bloque=bloque)


def calculo_generar_palabra(debugger: Debugger, paso, bloque):
    if paso <= 16:
        return ""
    resultado = f"\n\nCálculo prévio de una palabra a partir del bloque {bloque}:"
    resultado += f"\nPalabra generada paso {paso} = (XOR de las cuatro palabras usadas en los pasos {paso}-3, {paso}-8, {paso}-14 y {paso}-16) rotado a la izquierda 1 bit"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(debugger.palabra_a_sumar_en(paso - 3, bloque))} = Generada en paso {paso - 3}"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(debugger.palabra_a_sumar_en(paso - 8, bloque))} = Generada en paso {paso - 8}"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(debugger.palabra_a_sumar_en(paso - 14, bloque))} = Generada en paso {paso - 14}"
    resultado += f"\nXOR {mostrar_32_bits_centrados_con_espacio(debugger.palabra_a_sumar_en(paso - 16, bloque))} = Generada en paso {paso - 16}"
    resultado += crear_linea()
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(rotar_izquierda(debugger.palabra_a_sumar_en(paso, bloque), 31))} = Se rotará 1 bit a la izq."
    resultado += crear_linea()
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(debugger.palabra_a_sumar_en(paso, bloque))} = Palabra para este paso"
    return resultado


def serializar_paso_sha1(debugger, paso, bloque):
    iteracion = debugger.obtener_iteracion(paso=paso, bloque=bloque)
    operacion = iteracion.operacion
    A, B, C, D, E = iteracion.valores_iniciales()
    resultado = operacion.to_string() + "\n"
    resultado += f"A´= E + {nombre_clase_de(operacion)}(B, C, D) + (A <<< 5) + M[i] + K[j]\n"
    resultado += "E´= D; D´= C; C´= (B <<< 30); B´= A\n"
    resultado += f"\nA = {mostrar_32_bits_centrados_con_espacio(A)} = {hex_string_de(A)}"
    resultado += f"\nB = {mostrar_32_bits_centrados_con_espacio(B)} = {hex_string_de(B)}"
    resultado += f"\nC = {mostrar_32_bits_centrados_con_espacio(C)} = {hex_string_de(C)}"
    resultado += f"\nD = {mostrar_32_bits_centrados_con_espacio(D)} = {hex_string_de(D)}"
    resultado += f"\nE = {mostrar_32_bits_centrados_con_espacio(E)} = {hex_string_de(E)}"
    resultado += calculo_generar_palabra(debugger, paso, bloque)
    resultado += mostrar_operacion_correspondiente(B, C, D, operacion)
    resultado += crear_linea()
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(operacion.aplicar_a(B, C, D))} = {nombre_clase_de(operacion)}(B,C,D)"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(E)} = Valor de E"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(rotar_izquierda(A, 5))} = A rotado a izq. 5 bits"
    resultado += palabra_a_sumar(bloque, iteracion, paso)
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(iteracion.constante_k)} = Constante {hex_string_de(iteracion.constante_k)}"
    resultado += crear_linea()
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(iteracion.suma_final())} = Es ahora la palabra A\n"
    resultado += f"\nLa palabra D pasa a ocupar el lugar de E"
    resultado += f"\nLa palabra C pasa a ocupar el lugar de D"
    resultado += f"\nLa palabra B rotada 30 posiciones a la izquierda:\n"
    resultado += f"    {bit_string_de(rotar_izquierda(B, 30))} Es ahora la palabra C"
    resultado += f"\nLa palabra A pasa a ocupar el lugar de B"
    # TODO: Falta mostrar la actualizacion final!
    return resultado


def palabra_a_sumar(bloque, iteracion, paso):
    palabra_a_sumar = f"\n    {mostrar_32_bits_centrados_con_espacio(iteracion.palabra_a_sumar)} = "
    if paso <= 16:
        palabra_a_sumar += f"Palabra {paso} del bloque {bloque}"
    else:
        palabra_a_sumar += f"Palabra generada"
    return palabra_a_sumar


def mostrar_operacion_F(B, C, D):
    resultado = f"\n\n    {mostrar_32_bits_centrados_con_espacio(B & C)} = (B and C)"
    resultado += f"\nOR  {mostrar_32_bits_centrados_con_espacio((~B) & D)} = ((not B) and D)"
    return resultado


def mostrar_operacion_G(B, C, D):
    resultado = f"\n\n    {mostrar_32_bits_centrados_con_espacio(B)} = B"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(C)} = C"
    resultado += f"\nXOR {mostrar_32_bits_centrados_con_espacio(D)} = D"
    return resultado


def mostrar_operacion_H(B, C, D):
    resultado = f"\n\n    {mostrar_32_bits_centrados_con_espacio(B & C)} = (B and C)"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(B & D)} = (B and D)"
    resultado += f"\nXOR {mostrar_32_bits_centrados_con_espacio(C & D)} = (C and D)"
    return resultado


def mostrar_operacion_I(B, C, D):
    resultado = f"\n\n    {mostrar_32_bits_centrados_con_espacio(B)} = B"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(C)} = C"
    resultado += f"\nXOR {mostrar_32_bits_centrados_con_espacio(D)} = D"
    return resultado


def mostrar_operacion_correspondiente(B, C, D, operacion):
    if isinstance(operacion, F):
        return mostrar_operacion_F(B, C, D)
    if isinstance(operacion, G):
        return mostrar_operacion_G(B, C, D)
    if isinstance(operacion, H):
        return mostrar_operacion_H(B, C, D)
    if isinstance(operacion, I):
        return mostrar_operacion_I(B, C, D)
