from app.__init__ import db  # Usa a instância configurada em app/__init__.py

def init_db():
    """
    Função auxiliar para garantir que as tabelas sejam criadas.
    Deve ser usada apenas em cenários específicos onde Flask-Migrate não é utilizado.
    """
    from app.models import pessoa, produto, doacao  # Importa os modelos para registrar as tabelas
    try:
        db.create_all()  # Cria as tabelas no banco, apenas para desenvolvimento inicial
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
