import unittest
from app import create_app
from app.utils.db import db
from app.models.produto import Produto

class TestProduto(unittest.TestCase):
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

    def test_criar_produto(self):
        with self.app.app_context():
            produto = Produto(nome_produto="Produto 1", descricao="Descrição", quantidade=10)
            db.session.add(produto)
            db.session.commit()

            produtos = Produto.query.all()
            self.assertEqual(len(produtos), 1)
            self.assertEqual(produtos[0].nome_produto, "Produto 1")
