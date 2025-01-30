from app.__init__ import db

class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    nome_produto = db.Column(db.String(100), nullable=False, unique=True)  # Evita duplicação
    descricao = db.Column(db.String(255), nullable=True)
    quantidade = db.Column(db.Integer, nullable=False, default=0)
    data_entrada = db.Column(db.DateTime, nullable=False)

    @staticmethod
    def validar_disponibilidade(produto_id, quantidade):
        produto = Produto.query.get(produto_id)
        return produto and produto.quantidade >= quantidade
