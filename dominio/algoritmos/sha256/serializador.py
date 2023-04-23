from dominio.algoritmos.serializador_de_bloque import serializar_bloque_de_numeros
from dominio.algoritmos.sha256.operaciones import gamma1, ch, gamma0, maj, sigma1, sigma0
from helpers.debugger import Debugger
from helpers.operaciones_bit_a_bit import rotar_derecha_bitarray
from helpers.utilidades_UI import mostrar_32_bits_centrados_con_espacio, hex_string_de, crear_linea

def serializar_paso_sha256_completo(debugger, paso, bloque):
    iteracion = debugger.obtener_iteracion(paso=paso, bloque=bloque)
    A, B, C, D, E, F, G, H = iteracion.valores_iniciales()
    resultado = introduccion(A, B, C, D, E, F, G, H)
    resultado += "\n"

    resultado += "\nCalculando:"
    resultado += calculo_gamma0(A)
    resultado += calculo_gamma1(E)
    resultado += calculo_sigma0(debugger, paso, bloque)
    resultado += calculo_sigma1(debugger, paso, bloque)
    resultado += calculo_ch(E, F, G)
    resultado += calculo_maj(A, B, C)
    resultado += calculo_generar_palabra(debugger, paso, bloque)
    resultado += calculo_de_T1(iteracion=iteracion, paso=paso)
    resultado += calculo_de_T2(iteracion=iteracion)
    resultado += "\n"

    resultado = cambios_finales(A, D, E, iteracion, resultado)
    return resultado


def serializar_paso_sha256_resumido(debugger, paso, bloque):
    iteracion = debugger.obtener_iteracion(paso=paso, bloque=bloque)
    A, B, C, D, E, F, G, H = iteracion.valores_iniciales()

    resultado = introduccion(A, B, C, D, E, F, G, H)

    resultado += "\nUsando:"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(debugger.palabra_a_sumar_en(paso, bloque))} = W[{paso}]"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(iteracion.t1())} = T1"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(iteracion.t2())} = T2"
    resultado += "\n"

    resultado = cambios_finales(A, D, E, iteracion, resultado)
    return resultado


def serializar_bloque_sha256(debugger, bloque):
    return serializar_bloque_de_numeros(bloque, debugger)


def calculo_generar_palabra(debugger: Debugger, paso, bloque):
    if paso <= 15:
        return ""
    resultado = f"\nPalabra generada paso {paso} = Sigma1(W[{paso - 2}]) + W[{paso - 7}] + Sigma0(W[{paso - 15}]) + W[{paso - 16}]"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(sigma1(debugger.palabra_a_sumar_en(paso=paso, bloque=bloque)))} = Sigma1(W[{paso - 2}])"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(debugger.palabra_a_sumar_en(paso - 7, bloque))} = W[{paso - 7}]"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(sigma0(debugger.palabra_a_sumar_en(paso - 15, bloque)))} = Sigma0(W[{paso - 15}])"
    resultado += f"\n+   {mostrar_32_bits_centrados_con_espacio(debugger.palabra_a_sumar_en(paso - 16, bloque))} = W[{paso - 16}]"
    resultado += crear_linea()
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(debugger.palabra_a_sumar_en(paso, bloque))} = Palabra para este paso"
    return resultado


def calculo_de_T1(iteracion, paso):
    _, _, _, _, E, F, G, H = iteracion.valores_iniciales()
    resultado = f"\n T2:"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(H)} = H"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(gamma1(E))} = gamma1(E)"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(ch(E, F, G))} = ch(E,F,G)"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(iteracion.palabra_a_sumar)} = w[{paso}]"
    resultado += f"\n+   {mostrar_32_bits_centrados_con_espacio(iteracion.constante_a_usar)} = k[{paso}]"
    resultado += crear_linea()
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(iteracion.t1())} = T1"
    return resultado


def calculo_de_T2(iteracion):
    A, B, C, _, _, _, _, _ = iteracion.valores_iniciales()
    resultado = f"\n T1:"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(gamma0(A))} = gamma0(A)"
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


def cambios_finales(A, D, E, iteracion, resultado):
    resultado += "\nNos queda entonces:"
    resultado += la_palabra_a_pasa_al_lugar_de_b("G", "H")
    resultado += la_palabra_a_pasa_al_lugar_de_b("F", "G")
    resultado += la_palabra_a_pasa_al_lugar_de_b("E", "F")
    resultado += mostrar_suma_de_a_b_guardada_en_c("D", "T1", "E", D, iteracion.t1(), E)
    resultado += la_palabra_a_pasa_al_lugar_de_b("C", "D")
    resultado += la_palabra_a_pasa_al_lugar_de_b("B", "C")
    resultado += la_palabra_a_pasa_al_lugar_de_b("A", "B")
    resultado += mostrar_suma_de_a_b_guardada_en_c("T1", "T2", "A", iteracion.t1(), iteracion.t2(), A)
    return resultado


def introduccion(A, B, C, D, E, F, G, H):
    resultado = f"maj(X, Y, Z)= (X and Y) xor (X and Z) xor (Y and Z)\n"
    resultado += f"ch= (X, Y, Z)= (X and Y) xor ((not X) and Z)\n"
    resultado += f"gamma0= (X)= ROTR2(X) xor ROTR13(X) xor ROTR22(X)\n"
    resultado += f"gamma1= (X)= ROTR6(X) xor ROTR11(X) xor ROTR25(X)\n"
    resultado += f"Sigma0= (X)= ROTR7(X) xor ROTR18(X) xor SHR3(X)\n"
    resultado += f"Sigma1= (X)= ROTR17(X) xor ROTR19(X) xor SHR10(X)\n"
    resultado += f"T1= H + gamma1(E) + ch(E, F, G) + K[j] + W[j]\n"
    resultado += f"T2= gamma0(A) + maj(A, B, C)\n"
    resultado += "A´ = T1 + T2\n"
    resultado += "H´ = G; G´ = F; F´ = E; E´= D + T1; D´= C; C´= B; B´= A\n"
    resultado += "A partir del paso 16 W[n] = Sigma1(W[n -2]) + W[n-7] + Sigma0(W[n-15]) + W[n-16]\n"

    # valores iniciales
    resultado += f"\nA = {mostrar_32_bits_centrados_con_espacio(A)} = {hex_string_de(A)}"
    resultado += f"\nB = {mostrar_32_bits_centrados_con_espacio(B)} = {hex_string_de(B)}"
    resultado += f"\nC = {mostrar_32_bits_centrados_con_espacio(C)} = {hex_string_de(C)}"
    resultado += f"\nD = {mostrar_32_bits_centrados_con_espacio(D)} = {hex_string_de(D)}"
    resultado += f"\nE = {mostrar_32_bits_centrados_con_espacio(E)} = {hex_string_de(E)}"
    resultado += f"\nF = {mostrar_32_bits_centrados_con_espacio(F)} = {hex_string_de(F)}"
    resultado += f"\nG = {mostrar_32_bits_centrados_con_espacio(G)} = {hex_string_de(G)}"
    resultado += f"\nH = {mostrar_32_bits_centrados_con_espacio(H)} = {hex_string_de(H)}"
    return resultado


def la_palabra_a_pasa_al_lugar_de_b(palabra_a, palabra_b):
    return f"\nLa palabra {palabra_a} pasa a ocupar el lugar de {palabra_b}"

def calculo_gamma0(A):
    resultado = f"\n Gamma0:"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(rotar_derecha_bitarray(A, 2))} A rotado a derecha 2 bits"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(rotar_derecha_bitarray(A, 2))} A rotado a derecha 13 bits"
    resultado += f"\nXOR {mostrar_32_bits_centrados_con_espacio(rotar_derecha_bitarray(A, 2))} A rotado a derecha 22 bits"
    resultado += crear_linea()
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(gamma0(A))}\n"
    return resultado


def calculo_sigma0(debugger, paso, bloque):
    if paso < 16:
        return ""
    A = debugger.palabra_a_sumar_en(paso, bloque)
    resultado = f"\n sigma0:"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(rotar_derecha_bitarray(A, 2))} w[{paso} - 15] rotado a derecha 7 bits"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(rotar_derecha_bitarray(A, 2))} w[{paso} - 15] rotado a derecha 18 bits"
    resultado += f"\nXOR {mostrar_32_bits_centrados_con_espacio(rotar_derecha_bitarray(A, 2))} w[{paso} - 15] >> 3"
    resultado += crear_linea()
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(sigma0(A))}\n"
    return resultado


def calculo_gamma1(X):
    resultado = f"\n Gamma1:"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(rotar_derecha_bitarray(X, 6))} E rotado a derecha 6 bits"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(rotar_derecha_bitarray(X, 11))} E rotado a derecha 11 bits"
    resultado += f"\nXOR {mostrar_32_bits_centrados_con_espacio(rotar_derecha_bitarray(X, 25))} E rotado a derecha 25 bits"
    resultado += crear_linea()
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(gamma1(X))}\n"
    return resultado


def calculo_sigma1(debugger, paso, bloque):
    if paso < 16:
        return ""
    A = debugger.palabra_a_sumar_en(paso, bloque)
    resultado = f"\n sigma1:"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(rotar_derecha_bitarray(A, 2))} w[{paso} - 2] rotado a derecha 17 bits"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(rotar_derecha_bitarray(A, 2))} w[{paso} - 2] rotado a derecha 19 bits"
    resultado += f"\nXOR {mostrar_32_bits_centrados_con_espacio(rotar_derecha_bitarray(A, 2))} w[{paso} - 2] >> 10"
    resultado += crear_linea()
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(sigma1(A))}\n"
    return resultado


def calculo_ch(E, F, G):
    resultado = f"\n ch:"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio((E & F))} E and F"
    resultado += f"\nXOR {mostrar_32_bits_centrados_con_espacio((~E & G))} (not E) and G"
    resultado += crear_linea()
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(ch(E,F,G))}\n"
    return resultado


def calculo_maj(A, B, C):
    resultado = f"\n maj:"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio((A & B))} A and B"
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio((A & C))} A and C"
    resultado += f"\nXOR {mostrar_32_bits_centrados_con_espacio((B & C))} B and C"
    resultado += crear_linea()
    resultado += f"\n    {mostrar_32_bits_centrados_con_espacio(maj(A,B,C))}\n"
    return resultado

