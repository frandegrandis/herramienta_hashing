class Algoritmo:
    def __init__(self):
        self.iteraciones = []

    def iteraciones_por_bloque(self):
        return [self.iteraciones[x:x + self.cantidad_de_pasos_por_bloque()] for x in range(0, len(self.iteraciones),
                                                                                           self.cantidad_de_pasos_por_bloque())]

    def cantidad_de_pasos_por_bloque(self):
        raise Exception("El mensaje debe ser implementado por la subclase")

    def cantidad_bloques(self):
        return len(self.iteraciones_por_bloque())

    def palabras_hasheadas(self):
        raise Exception("El mensaje debe ser implementado por la subclase")

    def tamanio_de_palbra_en_bytes(self):
        raise Exception("El mensaje debe ser implementado por la subclase")
