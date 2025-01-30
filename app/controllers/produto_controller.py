from flask import render_template, request, redirect, url_for, flash
from app.models.produto import Produto
from app.__init__ import db
from datetime import datetime  # ✅ Importa datetime para a data automática


def listar_produtos():
    search = request.args.get('search', '').strip()
    if search:
        produtos = Produto.query.filter(Produto.nome_produto.ilike(f"%{search}%")).all()
    else:
        produtos = Produto.query.all()
    return render_template('produtos/lista.html', produtos=produtos, search=search)


def cadastrar_produto():
    if request.method == 'POST':
        nome_produto = request.form['nome_produto']
        if Produto.query.filter_by(nome_produto=nome_produto).first():
            flash('Produto já cadastrado!', 'danger')
            return redirect(url_for('cadastrar_produto'))

        # ✅ Verifica se a data foi fornecida, senão usa a data atual
        data_entrada = request.form.get('data_entrada')
        if data_entrada:
            data_entrada = datetime.strptime(data_entrada, "%Y-%m-%d").date()
        else:
            data_entrada = datetime.now().date()  # Usa a data atual se não for fornecida

        novo_produto = Produto(
            nome_produto=nome_produto,
            descricao=request.form['descricao'],
            quantidade=int(request.form['quantidade']),
            data_entrada=data_entrada  # ✅ Adiciona a data corretamente
        )
        db.session.add(novo_produto)
        db.session.commit()
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_produtos'))
    return render_template('produtos/cadastro.html')


def editar_produto(id):
    produto = Produto.query.get_or_404(id)

    if request.method == 'POST':
        produto.nome_produto = request.form['nome_produto']
        produto.descricao = request.form['descricao']
        produto.quantidade = int(request.form['quantidade'])
        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('listar_produtos'))

    return render_template('produtos/editar.html', produto=produto)