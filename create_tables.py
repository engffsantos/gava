from app import create_app, db
from app.models.pessoa import Pessoa
from app.models.produto import Produto
from app.models.doacao import Doacao
from app.models.pedido_doacao import PedidoDoacao

app = create_app()

with app.app_context():
    try:
        print("🛠 Criando tabela 'pessoas'...")
        Pessoa.__table__.create(db.engine, checkfirst=True)  # Criando apenas a tabela Pessoa
        print("✅ Tabela 'pessoas' criada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar a tabela 'pessoas': {e}")

    try:
        print("🛠 Criando tabela 'produtos'...")
        Produto.__table__.create(db.engine, checkfirst=True)  # Criando apenas a tabela Produto
        print("✅ Tabela 'produtos' criada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar a tabela 'produtos': {e}")

    try:
        print("🛠 Criando tabela 'doacoes'...")
        Doacao.__table__.create(db.engine, checkfirst=True)  # Criando apenas a tabela Doacao
        print("✅ Tabela 'doacoes' criada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar a tabela 'doacoes': {e}")

    try:
        print("🛠 Criando tabela 'pedidos'...")
        PedidoDoacao.__table__.create(db.engine, checkfirst=True)  # Criando apenas a tabela Doacao
        print("✅ Tabela 'Pedidos' criada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar a tabela 'doacoes': {e}")
    try:
        print("🛠 Criando tabela 'pedidos'...")
        PedidoDoacao.__table__.create(db.engine, checkfirst=True)  # Criando apenas a tabela Doacao
        print("✅ Tabela 'Pedidos' criada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar a tabela 'doacoes': {e}")

