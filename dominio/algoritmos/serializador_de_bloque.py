import dominio.algoritmos.sha256.constantes_sha256
from helpers.utilidades import suma_modular
from helpers.utilidades_UI import hex_string_de


def serializar_bloque(bloque, debugger):
    iteracion = debugger.obtener_iteracion(paso=1, bloque=bloque)
    vueltas = ["Primera vuelta:", "Segunda vuelta:", "Tercera vuelta:", "Cuarta vuelta:"]
    iteraciones_por_vuelta = debugger.cantidad_pasos() // len(vueltas)
    valores_iniciales = dominio.algoritmos.sha256.constantes_sha256.valores_iniciales()
    cantidad_variables = len(valores_iniciales)
    resultado = f"Valores iniciales:\n"
    resultado += mostrar_introduccion(valores_iniciales) + "\n\n"
    for paso in range(1, debugger.cantidad_pasos() + 1):
        if (paso - 1) % iteraciones_por_vuelta == 0:
            resultado += vueltas[paso // iteraciones_por_vuelta] + '\n'
        valores = (debugger.valores_finales(paso, bloque))
        resultado += f"Paso {paso:^3}: "
        resultado += f"{renglon_hex_de_(valores)}\n"
    valores_finales = debugger.valores_finales(debugger.cantidad_pasos(), bloque)
    resultado += f"\nActualización final: (valores iniciales + valores paso {debugger.cantidad_pasos()})\n"
    resultado += f"\t  "
    resultado += f"{renglon_hex_de_(valores_iniciales)}\n\t+ "
    resultado += f"{renglon_hex_de_(valores_finales)}\n\t{'-' * (4 + cantidad_variables * 9)}\n"  # 2 caracteres antes de las variables + 8 caracteres por variable + 1 espacio entre cada variable + 2 espacios al final
    actualizacion_final = [suma_modular(x, y) for x, y in zip(valores_iniciales, valores_finales)]
    resultado += f"\t  "
    resultado += renglon_hex_de_(actualizacion_final)
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


def renglon_hex_de_(valores):
    a = ""
    for i in valores:
        a += hex_string_de(i) + " "
    return a
