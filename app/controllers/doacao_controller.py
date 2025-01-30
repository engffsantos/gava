from flask import render_template, request, redirect, url_for, flash
from app.models.doacao import Doacao
from app.models.pessoa import Pessoa
from app.models.produto import Produto
from app.__init__ import db
from datetime import datetime
from datetime import date


def listar_doacoes():
    search_pessoa = request.args.get('search_pessoa', '').strip()
    search_produto = request.args.get('search_produto', '').strip()

    query = Doacao.query.join(Pessoa).join(Produto)

    if search_pessoa:
        query = query.filter(Pessoa.nome.ilike(f"%{search_pessoa}%"))

    if search_produto:
        query = query.filter(Produto.nome_produto.ilike(f"%{search_produto}%"))

    doacoes = query.all()

    return render_template('doacoes/relatorio.html', doacoes=doacoes)



def registrar_doacao():
    if request.method == 'POST':
        pessoa_id = request.form['pessoa_id']
        produto_id = request.form['produto_id']
        quantidade = int(request.form['quantidade'])
        data_doacao = request.form['data_doacao']  # Captura a data do formulário

        if not data_doacao:
            flash('A data da doação é obrigatória.', 'danger')
            return redirect(url_for('registrar_doacao'))

        produto = Produto.query.get(produto_id)
        if produto.quantidade < quantidade:
            flash(f'Produto "{produto.nome_produto}" sem estoque suficiente!', 'danger')
            return redirect(url_for('registrar_doacao'))

        nova_doacao = Doacao(
            pessoa_id=pessoa_id,
            produto_id=produto_id,
            quantidade=quantidade,
            data_doacao=datetime.strptime(data_doacao, '%Y-%m-%d')  # Converte string para data
        )
        produto.quantidade -= quantidade
        db.session.add(nova_doacao)
        db.session.commit()
        flash('Doação registrada com sucesso!', 'success')
        return redirect(url_for('listar_doacoes'))

    pessoas = Pessoa.query.all()
    produtos = Produto.query.all()
    return render_template('doacoes/registro.html', pessoas=pessoas, produtos=produtos, today=date.today())

def editar_doacao(id):
    doacao = Doacao.query.get_or_404(id)

    if request.method == 'POST':
        nova_quantidade = int(request.form['quantidade'])

        if doacao.produto.quantidade + doacao.quantidade < nova_quantidade:
            flash(f'Estoque insuficiente para essa alteração!', 'danger')
            return redirect(url_for('listar_doacoes'))

        # Atualizar estoque corretamente
        doacao.produto.quantidade += doacao.quantidade  # Devolve estoque anterior
        doacao.produto.quantidade -= nova_quantidade  # Atualiza estoque com nova quantidade
        doacao.quantidade = nova_quantidade

        db.session.commit()
        flash('Doação editada com sucesso!', 'success')
        return redirect(url_for('listar_doacoes'))

    return render_template('doacoes/editar.html', doacao=doacao)
