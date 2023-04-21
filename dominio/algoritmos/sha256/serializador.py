from dominio.algoritmos.serializador_de_bloque import serializar_bloque_por_bits
from dominio.algoritmos.sha1.operaciones_sha1 import F, G, H, I
from dominio.algoritmos.sha256.operaciones import gamma1, ch, gamma0, maj, sigma1, sigma0
from helpers.debugger import Debugger
from helpers.operaciones_bit_a_bit import rotar_izquierda
from helpers.utilidades_UI import mostrar_32_bits_centrados_con_espacio, hex_string_de, crear_linea


def calculo_generar_palabra(debugger: Debugger, paso, bloque):
    if paso <= 15:
        return ""
    resultado = f"\n\nCálculo prévio de una palabra a partir del bloque {bloque}:"
    resultado += f"\nPalabra generada paso {paso} = Sigma1(W[{paso - 2}]) + W[{paso - 7}] + Sigma0(W[{paso - 15}]) + W[{paso - 16}]"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(sigma1(debugger.palabra_a_sumar_en(paso=paso, bloque=bloque)))} = Sigma1(W[{paso -2}])"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(debugger.palabra_a_sumar_en(paso - 7, bloque))} = W[{paso - 7}]"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(sigma0(debugger.palabra_a_sumar_en(paso - 15, bloque)))} = Sigma0(W[{paso - 15}])"
    resultado += f"\n+   {mostrar_32_bits_centrados_con_espacio(debugger.palabra_a_sumar_en(paso - 16, bloque))} = W[{paso - 16}]"
    resultado += crear_linea()
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(debugger.palabra_a_sumar_en(paso, bloque))} = Palabra para este paso"
    return resultado


def calculo_de_T1(iteracion, paso):
    _, _, _, _, E, F, G, H = iteracion.valores_iniciales()
    resultado = f"\n\n    {mostrar_32_bits_centrados_con_espacio(H)} = H"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(gamma1(E))} = gamma1(E)"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(ch(E, F, G))} = ch(E,F,G)"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(iteracion.palabra_a_sumar)} = k[{paso}]"
    resultado += f"\n+   {mostrar_32_bits_centrados_con_espacio(iteracion.constante_a_usar)} = w[{paso}]"
    resultado += crear_linea()
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(iteracion.t1())} = T1"
    return resultado


def calculo_de_T2(iteracion):
    A, B, C, _, _, _, _, _ = iteracion.valores_iniciales()
    resultado = f"\n\n    {mostrar_32_bits_centrados_con_espacio(gamma0(A))} = gamma0(A)"
    resultado += f"\n+   {mostrar_32_bits_centrados_con_espacio(maj(A, B, C))} = maj(A,B,C)"
    resultado += crear_linea()
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(iteracion.t2())} = T2"
    return resultado


def mostrar_suma_de_a_b_guardada_en_c(nombre_a, nombre_b, nombre_c, valor_a, valor_b, valor_c):
    resultado = f"\n    {mostrar_32_bits_centrados_con_espacio(valor_a)} = {nombre_a}"
    resultado += f"\n+   {mostrar_32_bits_centrados_con_espacio(valor_b)} = {nombre_b}"
    resultado += crear_linea()
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(valor_c)} = Es ahora la palabra: {nombre_c}"
    return resultado


def serializar_paso_sha256(debugger, paso, bloque):
    iteracion = debugger.obtener_iteracion(paso=paso, bloque=bloque)
    A, B, C, D, E, F, G, H = iteracion.valores_iniciales()
    # Muestro el hashing teorico
    # Muestro como calculo T1 de forma teorica
    # Muestro como calculo T2 de forma teorica
    # H' = G
    # G' = F
    # F' = E
    # E' = D + T1
    # D' = C
    # C' = B
    # B' = A
    # Muestro el calculo de A' que seria T1 + T2

    # Valores iniciales
    # Calculo previo de le palabra a sumar
    # Calculo de variable t1
    # Calculo de variable T2
    # La palabra G pasa a ocupar el lugar de H
    # La palabra F pasa a ocupar el lugar de G
    # La palabra E pasa a ocupar el lugar de F
    # Muestro la suma de D + T1 y al resultado "Ahora es la palabra E
    # La palabra C pasa a ocupar el lugar de D
    # La palabra B pasa a ocupar el lugar de C
    # La palabra A pasa a ocupar el lugar de B
    # Muestro suma de T1 y T2 y al resultado le digo: "Ahora es la palabra A"

    # Cuando tenga que mostrar los sigmas y gammas tengo que printear los numeros binarios y poner que es A rotado der. X bits, ver ejemplos de otros hash cuando roto izq

    # introduccion:
    resultado = f"maj(X, Y, Z)= (X and Y) xor ((not X) and Z)\n"
    resultado += f"ch= (X, Y, Z)= (X and Y) xor (X and Z) xor (Y and Z)\n"

    resultado += f"T1= H + gamma1(E) + ch(E, F, G) + K[j] + W[j]\n"
    resultado += f"T2= gamma0(A) + maj(A, B, C)\n"
    resultado += "A´ = T1 + T2\n"
    resultado += "H´ = G; G´ = F; F´ = E; E´= D + T1; D´= C; C´= B; B´= A\n"

    # valores iniciales
    resultado += f"\nA = {mostrar_32_bits_centrados_con_espacio(A)} = {hex_string_de(A)}"
    resultado += f"\nB = {mostrar_32_bits_centrados_con_espacio(B)} = {hex_string_de(B)}"
    resultado += f"\nC = {mostrar_32_bits_centrados_con_espacio(C)} = {hex_string_de(C)}"
    resultado += f"\nD = {mostrar_32_bits_centrados_con_espacio(D)} = {hex_string_de(D)}"
    resultado += f"\nE = {mostrar_32_bits_centrados_con_espacio(E)} = {hex_string_de(E)}"
    resultado += f"\nF = {mostrar_32_bits_centrados_con_espacio(F)} = {hex_string_de(F)}"
    resultado += f"\nG = {mostrar_32_bits_centrados_con_espacio(G)} = {hex_string_de(G)}"
    resultado += f"\nH = {mostrar_32_bits_centrados_con_espacio(H)} = {hex_string_de(H)}"
    resultado += "\nUsando:"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(debugger.palabra_a_sumar_en(paso, bloque))} = Palabra a sumar"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(iteracion.t1())} = T1"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(iteracion.t2())} = T2"

    resultado+= "\n"
    # Calculo de palabra a sumar
    #resultado += calculo_generar_palabra(debugger, paso, bloque)

    # Calculo de T1
    #resultado += calculo_de_T1(iteracion=iteracion, paso=paso)

    # Calculo de T2:
    #resultado += calculo_de_T2(iteracion=iteracion)

    #resultado += "\n"

    # Muestro resultados
    resultado += la_palabra_a_pasa_al_lugar_de_b("G", "H")
    resultado += la_palabra_a_pasa_al_lugar_de_b("F", "G")
    resultado += la_palabra_a_pasa_al_lugar_de_b("E", "F")
    resultado += mostrar_suma_de_a_b_guardada_en_c("D", "T1", "E", D, iteracion.t1(), E)
    resultado += la_palabra_a_pasa_al_lugar_de_b("C", "D")
    resultado += la_palabra_a_pasa_al_lugar_de_b("B", "C")
    resultado += la_palabra_a_pasa_al_lugar_de_b("A", "B")
    resultado += mostrar_suma_de_a_b_guardada_en_c("T1", "T2", "A", iteracion.t1(), iteracion.t2(), A)
    # TODO: Falta mostrar la actualizacion final!
    return resultado


def la_palabra_a_pasa_al_lugar_de_b(palabra_a, palabra_b):
    return f"\nLa palabra {palabra_a} pasa a ocupar el lugar de {palabra_b}"


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


def serializar_bloque_sha256(debugger, bloque):
    return serializar_bloque_por_bits(bloque, debugger)
