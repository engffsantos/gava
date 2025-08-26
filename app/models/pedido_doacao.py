from app.__init__ import db
from flask import render_template, send_file
import pdfkit

class PedidoDoacao(db.Model):
    __tablename__ = 'pedidos_doacao'

    id = db.Column(db.Integer, primary_key=True)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoas.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    # Mantido como DateTime para permitir filtros por intervalo de dias com hora
    data_pedido = db.Column(db.DateTime, nullable=False)
    atendido = db.Column(db.Boolean, default=False)

    pessoa = db.relationship('Pessoa', backref='pedidos_doacao')
    produto = db.relationship('Produto', backref='pedidos_doacao')

    def __repr__(self) -> str:
        return f"<PedidoDoacao id={self.id} pessoa_id={self.pessoa_id} produto_id={self.produto_id} qtd={self.quantidade}>"
