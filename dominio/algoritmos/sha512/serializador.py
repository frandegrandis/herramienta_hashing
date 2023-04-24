from dominio.algoritmos.serializador_de_bloque import serializar_bloque_de_numeros
from dominio.algoritmos.sha512.operaciones import gamma1, ch, gamma0, maj, sigma0, sigma1
from helpers.debugger import Debugger
from helpers.operaciones_bit_a_bit import rotar_derecha
from helpers.utilidades_UI import mostrar_64_bits_centrados_con_espacio, hex_string_de, crear_linea


def serializar_paso_sha512_completo(debugger, paso, bloque):
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


def serializar_paso_sha512_resumido(debugger, paso, bloque):
    iteracion = debugger.obtener_iteracion(paso=paso, bloque=bloque)
    A, B, C, D, E, F, G, H = iteracion.valores_iniciales()

    resultado = introduccion(A, B, C, D, E, F, G, H)

    resultado += "\nUsando:"
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio(debugger.palabra_a_sumar_en(paso, bloque))} = W[{paso}]"
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio(iteracion.t1())} = T1"
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio(iteracion.t2())} = T2"
    resultado += "\n"

    resultado = cambios_finales(A, D, E, iteracion, resultado)
    return resultado


def serializar_bloque_sha512(debugger, bloque):
    return serializar_bloque_de_numeros(bloque, debugger, cantidad_de_bits = 64)


def calculo_generar_palabra(debugger: Debugger, paso, bloque):
    if paso <= 15:
        return ""
    resultado = f"\nPalabra generada paso {paso} = Sigma1(W[{paso - 2}]) + W[{paso - 7}] + Sigma0(W[{paso - 15}]) + W[{paso - 16}]"
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio(sigma1(debugger.palabra_a_sumar_en(paso=paso, bloque=bloque)))} = Sigma1(W[{paso - 2}])"
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio(debugger.palabra_a_sumar_en(paso - 7, bloque))} = W[{paso - 7}]"
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio(sigma0(debugger.palabra_a_sumar_en(paso - 15, bloque)))} = Sigma0(W[{paso - 15}])"
    resultado += f"\n+   {mostrar_64_bits_centrados_con_espacio(debugger.palabra_a_sumar_en(paso - 16, bloque))} = W[{paso - 16}]"
    resultado += crear_linea()
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio(debugger.palabra_a_sumar_en(paso, bloque))} = Palabra para este paso"
    return resultado


def calculo_de_T1(iteracion, paso):
    _, _, _, _, E, F, G, H = iteracion.valores_iniciales()
    resultado = f"\n T2:"
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio(H)} = H"
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio(gamma1(E))} = gamma1(E)"
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio(ch(E, F, G))} = ch(E,F,G)"
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio(iteracion.palabra_a_sumar)} = w[{paso}]"
    resultado += f"\n+   {mostrar_64_bits_centrados_con_espacio(iteracion.constante_a_usar)} = k[{paso}]"
    resultado += crear_linea()
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio(iteracion.t1())} = T1"
    return resultado


def calculo_de_T2(iteracion):
    A, B, C, _, _, _, _, _ = iteracion.valores_iniciales()
    resultado = f"\n T1:"
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio(gamma0(A))} = gamma0(A)"
    resultado += f"\n+   {mostrar_64_bits_centrados_con_espacio(maj(A, B, C))} = maj(A,B,C)"
    resultado += crear_linea()
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio(iteracion.t2())} = T2"
    return resultado


def mostrar_suma_de_a_b_guardada_en_c(nombre_a, nombre_b, nombre_c, valor_a, valor_b, valor_c):
    resultado = f"\n    {mostrar_64_bits_centrados_con_espacio(valor_a)} = {nombre_a}"
    resultado += f"\n+   {mostrar_64_bits_centrados_con_espacio(valor_b)} = {nombre_b}"
    resultado += crear_linea()
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio(valor_c)} = Es ahora la palabra: {nombre_c}"
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
    resultado += f"ch= (X, Y, Z)=(X and Y) xor ((not X) and Z)\n"
    resultado += f"gamma0= (X)= ROTR28(X) xor ROTR34(X) xor ROTR39(X)\n"
    resultado += f"gamma1= (X)= ROTR14(X) xor ROTR18(X) xor ROTR41(X)\n"
    resultado += f"Sigma0= (X)= ROTR1(X) xor ROTR8(X) xor SHR7(X)\n"
    resultado += f"Sigma1= (X)= ROTR19(X) xor ROTR61(X) xor SHR6(X)\n"
    resultado += f"T1= H + gamma1(E) + ch(E, F, G) + k[j] + w[j]\n"
    resultado += f"T2= gamma0(A) + maj(A, B, C)\n"
    resultado += "A´ = T1 + T2\n"
    resultado += "H´ = G; G´ = F; F´ = E; E´= D + T1; D´= C; C´= B; B´= A\n"
    resultado += "A partir del paso 16 W[n] = W[n] = Sigma1(W[n -2]) + W[n-7] + Sigma0(W[n-15]) + W[n-16]\n"

    # valores iniciales
    resultado += f"\nA = {mostrar_64_bits_centrados_con_espacio(A)} = {hex_string_de(A, 16)}"
    resultado += f"\nB = {mostrar_64_bits_centrados_con_espacio(B)} = {hex_string_de(B, 16)}"
    resultado += f"\nC = {mostrar_64_bits_centrados_con_espacio(C)} = {hex_string_de(C, 16)}"
    resultado += f"\nD = {mostrar_64_bits_centrados_con_espacio(D)} = {hex_string_de(D, 16)}"
    resultado += f"\nE = {mostrar_64_bits_centrados_con_espacio(E)} = {hex_string_de(E, 16)}"
    resultado += f"\nF = {mostrar_64_bits_centrados_con_espacio(F)} = {hex_string_de(F, 16)}"
    resultado += f"\nG = {mostrar_64_bits_centrados_con_espacio(G)} = {hex_string_de(G, 16)}"
    resultado += f"\nH = {mostrar_64_bits_centrados_con_espacio(H)} = {hex_string_de(H, 16)}"
    return resultado


def la_palabra_a_pasa_al_lugar_de_b(palabra_a, palabra_b):
    return f"\nLa palabra {palabra_a} pasa a ocupar el lugar de {palabra_b}"


def calculo_gamma0(A):
    resultado = f"\n Gamma0:"
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio(rotar_derecha(A, 28, cantidad_de_bits=64))} A rotado a derecha 28 bits"
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio(rotar_derecha(A, 34, cantidad_de_bits=64))} A rotado a derecha 34 bits"
    resultado += f"\nXOR {mostrar_64_bits_centrados_con_espacio(rotar_derecha(A, 39, cantidad_de_bits=64))} A rotado a derecha 39 bits"
    resultado += crear_linea()
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio(gamma0(A))}\n"
    return resultado


def calculo_sigma0(debugger, paso, bloque):
    if paso < 16:
        return ""
    numero_a_rotar = debugger.palabra_a_sumar_en(paso-15, bloque)
    resultado = f"\n sigma0:"
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio(rotar_derecha(numero_a_rotar, 1, cantidad_de_bits=64))} w[{paso} - 15] rotado a derecha 1 bits"
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio(rotar_derecha(numero_a_rotar, 8, cantidad_de_bits=64))} w[{paso} - 15] rotado a derecha 8 bits"
    resultado += f"\nXOR {mostrar_64_bits_centrados_con_espacio(numero_a_rotar >> 7)} w[{paso} - 15] >> 7"
    resultado += crear_linea()
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio(sigma0(numero_a_rotar))}\n"
    return resultado


def calculo_gamma1(X):
    resultado = f"\n Gamma1:"
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio(rotar_derecha(X, 14, cantidad_de_bits=64))} E rotado a derecha 14 bits"
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio(rotar_derecha(X, 18, cantidad_de_bits=64))} E rotado a derecha 18 bits"
    resultado += f"\nXOR {mostrar_64_bits_centrados_con_espacio(rotar_derecha(X, 41, cantidad_de_bits=64))} E rotado a derecha 41 bits"
    resultado += crear_linea()
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio(gamma1(X))}\n"
    return resultado


def calculo_sigma1(debugger, paso, bloque):
    if paso < 16:
        return ""
    A = debugger.palabra_a_sumar_en(paso - 2, bloque)
    resultado = f"\n sigma1:"
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio(rotar_derecha(A, 19, cantidad_de_bits=64))} w[{paso} - 2] rotado a derecha 19 bits"
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio(rotar_derecha(A, 61, cantidad_de_bits=64))} w[{paso} - 2] rotado a derecha 61 bits"
    resultado += f"\nXOR {mostrar_64_bits_centrados_con_espacio(A >> 6)} w[{paso} - 2] >> 6"
    resultado += crear_linea()
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio(sigma1(A))}\n"
    return resultado


def calculo_ch(E, F, G):
    resultado = f"\n ch:"
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio((E & F))} E and F"
    resultado += f"\nXOR {mostrar_64_bits_centrados_con_espacio((~E & G))} (not E) and G"
    resultado += crear_linea()
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio(ch(E, F, G))}\n"
    return resultado


def calculo_maj(A, B, C):
    resultado = f"\n maj:"
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio((A & B))} A and B"
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio((A & C))} A and C"
    resultado += f"\nXOR {mostrar_64_bits_centrados_con_espacio((B & C))} B and C"
    resultado += crear_linea()
    resultado += f"\n    {mostrar_64_bits_centrados_con_espacio(maj(A, B, C))}\n"
    return resultado
