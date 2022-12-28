class HasherStub:
    def __init__(self, valor_retorno):
        self.valor_retorno = valor_retorno
        self.mensajes = {}

    def md5(self):
        self.mensajes["md5"] = []
        return self

    def hash(self, valor_a_hashear):
        self.mensajes["hash"] = [valor_a_hashear]
        return self.valor_retorno

    def sha1(self):
        self.mensajes["sha1"] = []
        return self

    def sha256(self):
        self.mensajes["sha256"] = []
        return self

    def recibio(self, nombre_metodo, parametros=[]):
        return nombre_metodo in self.mensajes and self.mensajes[nombre_metodo] == parametros
