from app.controllers import pessoa_controller, produto_controller, doacao_controller, pedido_doacao_controller
from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

def init_routes(app):
    # Pessoas

    app.add_url_rule('/pessoas', 'listar_pessoas', pessoa_controller.listar_pessoas)
    app.add_url_rule('/cadastrar_pessoa', 'cadastrar_pessoa', pessoa_controller.cadastrar_pessoa, methods=['GET', 'POST'])
    app.add_url_rule('/editar_pessoa/<int:id>', 'editar_pessoa', pessoa_controller.editar_pessoa, methods=['GET', 'POST'])
    app.add_url_rule('/desativar_pessoa/<int:id>', 'desativar_pessoa', pessoa_controller.desativar_pessoa, methods=['POST'])

    # Produtos
    app.add_url_rule('/produtos', 'listar_produtos', produto_controller.listar_produtos)
    app.add_url_rule('/cadastrar_produto', 'cadastrar_produto', produto_controller.cadastrar_produto, methods=['GET', 'POST'])
    app.add_url_rule('/editar_produto/<int:id>', 'editar_produto', produto_controller.editar_produto, methods=['GET', 'POST'])

    # Doações
    app.add_url_rule('/doacoes', 'listar_doacoes', doacao_controller.listar_doacoes)
    app.add_url_rule('/registrar_doacao', 'registrar_doacao', doacao_controller.registrar_doacao, methods=['GET', 'POST'])
    app.add_url_rule('/editar_doacao/<int:id>', 'editar_doacao', doacao_controller.editar_doacao, methods=['GET', 'POST'])
    app.add_url_rule('/doacoes', 'relatorio_doacoes', doacao_controller.listar_doacoes)

    # Pedidos de Doação
    app.add_url_rule('/pedidos', 'listar_pedidos', pedido_doacao_controller.listar_pedidos)
    app.add_url_rule('/cadastrar_pedido', 'cadastrar_pedido', pedido_doacao_controller.cadastrar_pedido, methods=['GET', 'POST'])
    app.add_url_rule('/editar_pedido/<int:id>', 'editar_pedido', pedido_doacao_controller.editar_pedido, methods=['GET', 'POST'])
    app.add_url_rule('/relatorio_pedidos_pdf', 'relatorio_pedidos_pdf', pedido_doacao_controller.gerar_relatorio_pdf, methods=['GET'])
