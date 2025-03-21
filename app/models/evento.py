from app.__init__ import db

class Evento(db.Model):
    __tablename__ = 'eventos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    local = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String(10), nullable=False)  # Ex: "07/24"
    doacao_para = db.Column(db.String(255), nullable=False)
    doacao = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Evento {self.nome} ({self.data})>"
