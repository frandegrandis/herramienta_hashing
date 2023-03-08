from dominio.algoritmos.serializador_de_bloque import serializar_bloque_por_bits
from dominio.algoritmos.sha1.operaciones_sha1 import F, G, H, I
from helpers.debugger import Debugger
from helpers.operaciones_bit_a_bit import rotar_izquierda
from helpers.utilidades_UI import mostrar_32_bits_centrados_con_espacio, crear_linea


def serializar_bloque_sha256(debugger, bloque):
    return serializar_bloque_por_bits(bloque, debugger)


def calculo_generar_palabra(debugger: Debugger, paso, bloque):
    if paso <= 16:
        return ""
    resultado = f"\n\nCálculo prévio de una palabra a partir del bloque {bloque}:"
    resultado += f"\nPalabra generada paso {paso} = (XOR de las cuatro palabras usadas en los pasos {paso}-3, {paso}-8, {paso}-14 y {paso}-16) rotado a la izquierda 1 bit"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(debugger.palabra_en(paso - 3, bloque))} = Generada en paso {paso - 3}"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(debugger.palabra_en(paso - 8, bloque))} = Generada en paso {paso - 8}"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(debugger.palabra_en(paso - 14, bloque))} = Generada en paso {paso - 14}"
    resultado += f"\nXOR {mostrar_32_bits_centrados_con_espacio(debugger.palabra_en(paso - 16, bloque))} = Generada en paso {paso - 16}"
    resultado += crear_linea()
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(rotar_izquierda(debugger.palabra_en(paso, bloque), 31))} = Se rotará 1 bit a la izq."
    resultado += crear_linea()
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(debugger.palabra_en(paso, bloque))} = Palabra para este paso"
    return resultado


def serializar_paso_sha256(debugger, paso, bloque):
    resultado = "pepe lopez"
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
