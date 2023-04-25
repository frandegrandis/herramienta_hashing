from bitarray import bitarray

from helpers.debugger import Debugger
from helpers.operaciones_bit_a_bit import bitarray_a_numero
from helpers.utilidades_UI import mostrar_32_bits_centrados_con_espacio, mostrar_64_bits_centrados_con_espacio


def serializar_padding(debugger: Debugger):
    tamanio_en_bytes_de_palabra = debugger.tamanio_de_palbra_en_bytes()
    bytearray_inicial = debugger.bytearray_inicial()
    palabras_despues_del_padding = debugger.bytearray_con_padding()
    resultado = "Se comienza con las palabras:\n"
    mostrar_bits = mostrar_32_bits_centrados_con_espacio
    if tamanio_en_bytes_de_palabra == 8:
        mostrar_bits = mostrar_64_bits_centrados_con_espacio


    for i in range(0, len(bytearray_inicial), tamanio_en_bytes_de_palabra):
        resultado+=f"Palabra {(i//tamanio_en_bytes_de_palabra)+1} = "
        bytearray = bytearray_inicial[i:i + tamanio_en_bytes_de_palabra]
        bitarray2 = bitarray()
        bitarray2.frombytes(bytearray)
        if i == range(0, len(bytearray_inicial), tamanio_en_bytes_de_palabra)[-1]:
            resultado += f"    {bin(abs(bitarray_a_numero(bitarray2)))[2:]}\n"
        else:
            resultado+= f"{mostrar_bits(bitarray2)}\n"

    resultado += "Luego de aplicar el padding obtenemos:\n"
    i=1
    for palabra in palabras_despues_del_padding:
        if i < 10:
            resultado+= f"Palabra 0{i} = {mostrar_bits(palabra)}\n"
        else:
            resultado+= f"Palabra {i} = {mostrar_bits(palabra)}\n"
        i+=1
    return resultado
