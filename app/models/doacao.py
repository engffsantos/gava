from app.__init__ import db
from flask import jsonify
from datetime import date
from app.models import Produto
from app.models.pedido_doacao import PedidoDoacao


class Doacao(db.Model):
    __tablename__ = 'doacoes'

    id = db.Column(db.Integer, primary_key=True)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoas.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data_doacao = db.Column(db.Date, nullable=False, default=date.today)

    pessoa = db.relationship('Pessoa', backref='doacoes_pessoa')
    produto = db.relationship('Produto', backref='doacoes_produto_rel')

    @staticmethod
    def validar_estoque(produto_id, quantidade):
        return Produto.validar_disponibilidade(produto_id, quantidade)

    @staticmethod
    def registrar_doacao(pessoa_id, produto_id, quantidade):
        produto = Produto.query.get(produto_id)
        if not produto or produto.quantidade < quantidade:
            return jsonify({"erro": "Estoque insuficiente para doação."}), 400

        nova_doacao = Doacao(
            pessoa_id=pessoa_id,
            produto_id=produto_id,
            quantidade=quantidade,
            data_doacao=db.func.current_date()
        )
        produto.quantidade -= quantidade
        db.session.add(nova_doacao)
        db.session.commit()

        # Excluir o pedido de doação correspondente, se existir
        pedido = PedidoDoacao.query.filter_by(pessoa_id=pessoa_id, produto_id=produto_id, quantidade=quantidade).first()
        if pedido:
            db.session.delete(pedido)
            db.session.commit()

        return jsonify({"mensagem": "Doação registrada com sucesso."}), 200