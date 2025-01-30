from app.__init__ import db
from flask import jsonify, request

class Pessoa(db.Model):
    __tablename__ = 'pessoas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)  # Evita duplicação
    endereco = db.Column(db.String(255))
    bairro = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    filhos = db.Column(db.String(50))
    profissao = db.Column(db.String(50))
    qtd_pessoas = db.Column(db.Integer)
    locomocao = db.Column(db.String(50))
    data_cadastro = db.Column(db.Date)
    ativo = db.Column(db.Boolean, default=True)  # Novo campo para ativação/desativação

    #doacoes = db.relationship('Doacao', backref='pessoa', lazy='dynamic')
    @staticmethod
    def buscar_por_nome(nome):
        return Pessoa.query.filter(Pessoa.nome.ilike(f"%{nome}%")).all()

    @staticmethod
    def desativar_pessoa(pessoa_id):
        pessoa = Pessoa.query.get(pessoa_id)
        if pessoa:
            pessoa.ativo = False
            db.session.commit()
            return jsonify({"mensagem": "Pessoa desativada com sucesso."}), 200
        return jsonify({"erro": "Pessoa não encontrada."}), 404
