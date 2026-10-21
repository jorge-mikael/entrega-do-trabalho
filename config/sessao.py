class Sessao():
    _id = None
    _nome = None


    @classmethod
    def get_id(cls):
        return cls._id


    @classmethod
    def get_nome(cls):
        return cls._nome


    @classmethod
    def set_usuario(cls, id, nome):
        cls._id = id
        cls._nome = nome
    