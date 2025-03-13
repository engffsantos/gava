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
    from app.models.pedido_doacao import PedidoDoacao  # Importação corrigida dentro da função

    pessoa_id = request.args.get('pessoa_id', type=int)
    produto_id = request.args.get('produto_id', type=int)
    quantidade = request.args.get('quantidade', type=int)

    if request.method == 'POST':
        pessoa_id = request.form['pessoa_id']
        produto_id = request.form['produto_id']
        quantidade = int(request.form['quantidade'])
        data_doacao = request.form['data_doacao']

        if not data_doacao:
            flash('A data da doação é obrigatória.', 'danger')
            return redirect(url_for('registrar_doacao'))

        produto = Produto.query.get(produto_id)
        if not produto or produto.quantidade < quantidade:
            flash(f'Produto insuficiente para a doação!', 'danger')
            return redirect(
                url_for('registrar_doacao', pessoa_id=pessoa_id, produto_id=produto_id, quantidade=quantidade))

        nova_doacao = Doacao(
            pessoa_id=pessoa_id,
            produto_id=produto_id,
            quantidade=quantidade,
            data_doacao=datetime.strptime(data_doacao, '%Y-%m-%d')
        )
        produto.quantidade -= quantidade
        db.session.add(nova_doacao)
        db.session.commit()
        flash('Doação registrada com sucesso!', 'success')

        # Excluir o pedido de doação correspondente
        pedido = PedidoDoacao.query.filter_by(pessoa_id=pessoa_id, produto_id=produto_id, quantidade=quantidade).first()
        if pedido:
            db.session.delete(pedido)
            db.session.commit()

        return redirect(url_for('listar_doacoes'))

    pessoas = Pessoa.query.all()
    produtos = Produto.query.all()
    return render_template('doacoes/registro.html', pessoas=pessoas, produtos=produtos, pessoa_id=pessoa_id,
                           produto_id=produto_id, quantidade=quantidade, today=date.today())

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


def delete_doacao(id):

    doacao = Doacao.query.get_or_404(id)
    # Recuperar o produto associado e devolver a quantidade ao estoque
    produto = Produto.query.get(doacao.produto_id)
    if produto:
        produto.quantidade += doacao.quantidade  # Devolve ao estoque

    # Excluir a doação do banco de dados
    db.session.delete(doacao)
    db.session.commit()

    flash('Doação excluída e quantidade devolvida ao estoque!', 'success')
    return redirect(url_for('listar_doacoes'))  # Redireciona para a lista de doações
def validar_pedido():
    pessoa_id = request.args.get('pessoa_id', type=int)
    produto_id = request.args.get('produto_id', type=int)
    quantidade = request.args.get('quantidade', type=int)

    pessoa = Pessoa.query.get(pessoa_id)
    if not pessoa or not pessoa.ativo:
        flash(f'Esta pessoa está inativa e não pode receber doações!', 'danger')
        return redirect(url_for('listar_pedidos'))

    produto = Produto.query.get(produto_id)
    if not produto or produto.quantidade < quantidade:
        flash(f'Produto insuficiente para atender o pedido!', 'danger')
        return redirect(url_for('listar_pedidos'))

    return redirect(url_for('registrar_doacao', pessoa_id=pessoa_id, produto_id=produto_id, quantidade=quantidade))
