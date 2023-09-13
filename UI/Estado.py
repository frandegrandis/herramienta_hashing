import gc


class Estado():
    tamanio_letra = 14

    @classmethod
    def agrandar_letra(cls):
        cls.tamanio_letra += 1
        cls._actualizar_cajas_de_texto()

    @classmethod
    def achicar_letra(cls):
        cls.tamanio_letra -= 1
        cls._actualizar_cajas_de_texto()

    @classmethod
    def _actualizar_cajas_de_texto(cls):
        from UI.components.caja_de_texto import CajaDeTexto
        '''
            Aca aprovechamos la metaprogramacion para "triggerear" un hook basicamente, esta clase representa el estado
            global de la aplicacion y todos los resultados son mostrados dentro de una CajaDeTexto, cuando el tamaño de la
            letra aumenta nos interesa refrescar el tamaño de texto de todos los componentes que muestren texto
            Esto nos ahorra meter mucha mugre entre todos los objetos de la UI permitiendo asi centrar todo en una unica 
            clase global :)
            '''
        cajas_de_texto = filter(lambda objeto: objeto.__class__ is CajaDeTexto, gc.get_referrers(CajaDeTexto))
        for caja_de_texto in cajas_de_texto:
            caja_de_texto.actualizar_letra()
