from app.__init__ import db

class Doacao(db.Model):
    __tablename__ = 'doacoes'

    id = db.Column(db.Integer, primary_key=True)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoas.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data_doacao = db.Column(db.Date, nullable=False)

    pessoa = db.relationship('Pessoa', backref='doacoes_pessoa')
    produto = db.relationship('Produto', backref='doacoes_produto_rel')
