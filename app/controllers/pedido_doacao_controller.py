from flask import render_template, request, redirect, url_for, flash
from app.models.pedido_doacao import PedidoDoacao
from app.models.pessoa import Pessoa
from app.models.produto import Produto
from app.__init__ import db
from datetime import datetime

def listar_pedidos():
    pedidos = PedidoDoacao.query.join(Pessoa, PedidoDoacao.pessoa_id == Pessoa.id).join(Produto, PedidoDoacao.produto_id == Produto.id).all()
    return render_template('pedidos/lista.html', pedidos=pedidos)

def cadastrar_pedido():
    if request.method == 'POST':
        pessoa_id = request.form['pessoa_id']
        produto_id = request.form['produto_id']
        quantidade = int(request.form['quantidade'])  # Certifique-se de que é um número inteiro
        data_pedido = datetime.now()  # Data atual para o pedido

        # Criar um novo pedido de doação
        novo_pedido = PedidoDoacao(
            pessoa_id=pessoa_id,
            produto_id=produto_id,
            quantidade=quantidade,
            data_pedido=data_pedido
        )

        # Salvar no banco de dados
        db.session.add(novo_pedido)
        db.session.commit()

        flash('Pedido de doação cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_pedidos'))

    # Buscar pessoas e produtos para preencher o formulário
    pessoas = Pessoa.query.all()
    produtos = Produto.query.all()

    return render_template('pedidos/cadastro.html', pessoas=pessoas, produtos=produtos)
