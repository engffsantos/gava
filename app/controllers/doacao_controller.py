from flask import render_template, request, redirect, url_for, flash
from app.models.doacao import Doacao
from app.models.pessoa import Pessoa
from app.models.produto import Produto
from app.__init__ import db
from datetime import datetime
def listar_doacoes():
    doacoes = Doacao.query.join(Pessoa, Doacao.pessoa_id == Pessoa.id).join(Produto, Doacao.produto_id == Produto.id).all()
    return render_template('doacoes/relatorio.html', doacoes=doacoes)

def registrar_doacao():
    if request.method == 'POST':
        pessoa_id = request.form['pessoa_id']
        produto_id = request.form['produto_id']
        quantidade = int(request.form['quantidade'])  # Certifique-se de que é um número inteiro
        #data_doacao = request.form['data_doacao']
        data_doacao = datetime.strptime(request.form['data_doacao'], "%Y-%m-%d").date()

        # Buscar o produto associado
        produto = Produto.query.get(produto_id)
        if not produto:
            flash('Produto não encontrado.', 'danger')
            return redirect(url_for('registrar_doacao'))

        # Verificar se há quantidade suficiente no estoque
        if produto.quantidade < quantidade:
            flash(f'Estoque insuficiente para o produto "{produto.nome_produto}".', 'danger')
            return redirect(url_for('registrar_doacao'))

        # Criar a doação e atualizar o estoque
        nova_doacao = Doacao(
            pessoa_id=pessoa_id,
            produto_id=produto_id,
            quantidade=quantidade,
            data_doacao=data_doacao
        )
        produto.quantidade -= quantidade  # Atualiza a quantidade no estoque

        # Salvar no banco de dados
        db.session.add(nova_doacao)
        db.session.commit()

        flash('Doação registrada com sucesso!', 'success')
        return redirect(url_for('listar_doacoes'))

    # Buscar pessoas e produtos para preencher o formulário
    pessoas = Pessoa.query.all()
    produtos = Produto.query.all()

    return render_template('doacoes/registro.html', pessoas=pessoas, produtos=produtos)
