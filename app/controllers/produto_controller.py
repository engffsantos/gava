from flask import render_template, request, redirect, url_for, flash
from app.models.produto import Produto
from app.__init__ import db
from datetime import datetime
def listar_produtos():
    produtos = Produto.query.all()
    return render_template('produtos/lista.html', produtos=produtos)

def cadastrar_produto():
    if request.method == 'POST':
        nome_produto = request.form['nome_produto']
        descricao = request.form['descricao']
        quantidade = request.form['quantidade']
        #data_entrada = request.form['data_entrada']
        data_entrada = datetime.strptime(request.form['data_entrada'], "%Y-%m-%d").date()

        novo_produto = Produto(nome_produto=nome_produto, descricao=descricao, quantidade=quantidade, data_entrada=data_entrada)

        db.session.add(novo_produto)
        db.session.commit()
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_produtos'))
    return render_template('produtos/cadastro.html')
