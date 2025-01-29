import unittest
from app import create_app
from app.utils.db import db
from app.models.doacao import Doacao, Pessoa, Produto

class TestDoacao(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_registrar_doacao(self):
        with self.app.app_context():
            pessoa = Pessoa(nome="Teste Pessoa")
            produto = Produto(nome_produto="Teste Produto", quantidade=20)
            db.session.add(pessoa)
            db.session.add(produto)
            db.session.commit()

            doacao = Doacao(pessoa_id=pessoa.id, produto_id=produto.id, quantidade=5)
            db.session.add(doacao)
            db.session.commit()

            doacoes = Doacao.query.all()
            self.assertEqual(len(doacoes), 1)
            self.assertEqual(doacoes[0].quantidade, 5)
