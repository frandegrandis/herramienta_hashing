from helpers.utilidades import suma_modular
from helpers.utilidades_UI import hex_string_de


def serializar_bloque_de_numeros(bloque, debugger, cantidad_de_bits=32):
    return serializar_bloque(bloque, suma_modular, debugger, cantidad_de_bits=cantidad_de_bits)


def serializar_bloque(bloque, calcular_suma_modular, debugger, cantidad_de_bits=32):
    digitos_hexa = cantidad_de_bits // 4
    iteracion = debugger.obtener_iteracion(paso=1, bloque=bloque)
    vueltas = ["Primera vuelta:", "Segunda vuelta:", "Tercera vuelta:", "Cuarta vuelta:"]
    iteraciones_por_vuelta = debugger.cantidad_pasos() // len(vueltas)
    valores_iniciales = iteracion.valores_iniciales()
    cantidad_variables = len(valores_iniciales)
    resultado = f"Valores iniciales:\n"
    resultado += mostrar_introduccion(valores_iniciales) + "\n\n"
    for paso in range(1, debugger.cantidad_pasos() + 1):
        if (paso - 1) % iteraciones_por_vuelta == 0:
            resultado += vueltas[paso // iteraciones_por_vuelta] + '\n'
        valores = (debugger.valores_finales(paso, bloque))
        resultado += f"Paso {paso:^3}: "
        resultado += f"{renglon_hex_de_(valores, tamanio_de_palabra_hexa=digitos_hexa)}\n"
    valores_finales = debugger.valores_finales(debugger.cantidad_pasos(), bloque)
    resultado += f"\nActualización final: (valores iniciales + valores paso {debugger.cantidad_pasos()})\n"
    resultado += f"\t  "
    resultado += f"{renglon_hex_de_(valores_iniciales, tamanio_de_palabra_hexa=digitos_hexa)}\n\t+ "
    resultado += f"{renglon_hex_de_(valores_finales, tamanio_de_palabra_hexa=digitos_hexa)}\n\t{'-' * (4 + cantidad_variables * 9)}\n"  # 2 caracteres antes de las variables + 8 caracteres por variable + 1 espacio entre cada variable + 2 espacios al final
    actualizacion_final = [calcular_suma_modular(x, y, modulo=2**cantidad_de_bits) for x, y in zip(valores_iniciales, valores_finales)]
    resultado += f"\t  "
    resultado += renglon_hex_de_(actualizacion_final, tamanio_de_palabra_hexa=digitos_hexa)
    return resultado


def mostrar_introduccion(valores_iniciales):
    letra = "A"
    explicacion_paso = f"\nPaso i:\t "
    a = ""
    for i in valores_iniciales:
        a += f"{letra}= {hex_string_de(i)}\n"
        explicacion_paso += letra + " "
        letra = chr(ord(letra) + 1)
    a += explicacion_paso
    return a


def renglon_hex_de_(valores, tamanio_de_palabra_hexa=8):
    a = ""
    for i in valores:
        a += hex_string_de(i,tamanio_de_palabra_hexa=tamanio_de_palabra_hexa) + " "
    return a
