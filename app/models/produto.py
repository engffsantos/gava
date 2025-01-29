from app.__init__ import db

class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    nome_produto = db.Column(db.String(100), nullable=False)  # Nome do produto
    descricao = db.Column(db.String(255), nullable=True)      # Descrição opcional
    quantidade = db.Column(db.Integer, nullable=False, default=0)  # Quantidade no estoque
    data_entrada = db.Column(db.DateTime, nullable=False)          # Data de entrada no sistema

    def __init__(self, nome_produto, descricao, quantidade, data_entrada):
        self.nome_produto = nome_produto
        self.descricao = descricao
        self.quantidade = quantidade
        self.data_entrada = data_entrada
