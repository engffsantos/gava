from flask import render_template, request, redirect, url_for, flash
from app.models.doacao import Doacao
from app.models.pessoa import Pessoa
from app.models.produto import Produto
from app.__init__ import db
from datetime import datetime
from datetime import date
from flask import send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def listar_doacoes():
    search_pessoa = request.args.get('search_pessoa', '').strip()
    search_produto = request.args.get('search_produto', '').strip()
    ano = request.args.get('ano', '').strip()
    data_inicio = request.args.get('data_inicio', '').strip()
    data_fim = request.args.get('data_fim', '').strip()

    query = Doacao.query.join(Pessoa).join(Produto)

    if search_pessoa:
        query = query.filter(Pessoa.nome.ilike(f"%{search_pessoa}%"))

    if search_produto:
        query = query.filter(Produto.nome_produto.ilike(f"%{search_produto}%"))

    if ano:
        query = query.filter(func.extract('year', Doacao.data_doacao) == int(ano))

    if data_inicio and data_fim:
        query = query.filter(Doacao.data_doacao.between(data_inicio, data_fim))

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
def gerar_relatorio_pdf():
    search_pessoa = request.args.get('search_pessoa', '').strip()
    search_produto = request.args.get('search_produto', '').strip()

    # Construção da query com joins e filtros
    doacoes_query = Doacao.query.join(Pessoa, Doacao.pessoa_id == Pessoa.id).join(Produto, Doacao.produto_id == Produto.id)

    if search_pessoa:
        doacoes_query = doacoes_query.filter(Pessoa.nome.ilike(f"%{search_pessoa}%"))

    if search_produto:
        doacoes_query = doacoes_query.filter(Produto.nome_produto.ilike(f"%{search_produto}%"))

    doacoes = doacoes_query.all()

    if not doacoes:
        flash("Nenhuma doação encontrada para gerar o relatório.", "warning")
        return redirect(url_for("relatorio_doacoes"))

    pdf_dir = os.path.join("app", "static")
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)

    pdf_filename = f"relatorio_doacoes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf_path = os.path.join(pdf_dir, pdf_filename)

    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 40, "Relatório de Doações")

    c.setFont("Helvetica", 12)
    y = height - 80
    c.drawString(30, y, "ID")
    c.drawString(70, y, "Pessoa")
    c.drawString(250, y, "Produto")
    c.drawString(400, y, "Qtd")
    c.drawString(450, y, "Data")
    y -= 20

    c.setFont("Helvetica", 10)
    for d in doacoes:
        c.drawString(30, y, str(d.id))
        c.drawString(70, y, d.pessoa.nome[:20])
        c.drawString(250, y, d.produto.nome_produto[:20])
        c.drawString(400, y, str(d.quantidade))
        c.drawString(450, y, d.data_doacao.strftime("%d/%m/%Y"))
        y -= 20
        if y < 40:
            c.showPage()
            y = height - 80

    c.save()

    return render_template("doacoes/exibir_relatorio.html", pdf_filename=pdf_filename)
