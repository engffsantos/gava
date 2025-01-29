import unittest
from app import create_app
from app.utils.db import db
from app.models.pessoa import Pessoa

class TestPessoa(unittest.TestCase):
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

    def test_criar_pessoa(self):
        with self.app.app_context():
            pessoa = Pessoa(nome="Teste", endereco="Rua 1", telefone="12345678")
            db.session.add(pessoa)
            db.session.commit()

            pessoas = Pessoa.query.all()
            self.assertEqual(len(pessoas), 1)
            self.assertEqual(pessoas[0].nome, "Teste")
