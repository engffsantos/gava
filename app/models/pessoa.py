from app.__init__ import db

class Pessoa(db.Model):
    __tablename__ = 'pessoas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(255))
    bairro = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    filhos = db.Column(db.String(50))
    profissao = db.Column(db.String(50))
    qtd_pessoas = db.Column(db.Integer)
    locomocao = db.Column(db.String(50))
    data_cadastro = db.Column(db.Date)
