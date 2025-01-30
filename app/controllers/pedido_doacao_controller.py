from flask import render_template, request, redirect, url_for, flash, send_file
from app.models.pedido_doacao import PedidoDoacao
from app.models.pessoa import Pessoa
from app.models.produto import Produto
from app.__init__ import db
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def listar_pedidos():
    search_pessoa = request.args.get('search_pessoa', '').strip()
    search_produto = request.args.get('search_produto', '').strip()

    pedidos_query = PedidoDoacao.query.join(Pessoa, PedidoDoacao.pessoa_id == Pessoa.id).join(Produto, PedidoDoacao.produto_id == Produto.id)

    if search_pessoa:
        pedidos_query = pedidos_query.filter(Pessoa.nome.ilike(f"%{search_pessoa}%"))
    if search_produto:
        pedidos_query = pedidos_query.filter(Produto.nome_produto.ilike(f"%{search_produto}%"))

    pedidos = pedidos_query.all()

    return render_template('pedidos/lista.html', pedidos=pedidos)

def cadastrar_pedido():
    if request.method == 'POST':
        pessoa_id = request.form.get('pessoa_id')
        produto_id = request.form.get('produto_id')
        quantidade = request.form.get('quantidade')

        if not pessoa_id or not produto_id or not quantidade:
            flash('Todos os campos são obrigatórios!', 'danger')
            return redirect(url_for('cadastrar_pedido'))

        quantidade = int(quantidade)
        data_pedido = datetime.utcnow().date()

        novo_pedido = PedidoDoacao(
            pessoa_id=pessoa_id,
            produto_id=produto_id,
            quantidade=quantidade,
            data_pedido=data_pedido
        )
        db.session.add(novo_pedido)
        db.session.commit()
        flash('Pedido de doação cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_pedidos'))

    pessoas = Pessoa.query.all()
    produtos = Produto.query.all()
    return render_template('pedidos/cadastro.html', pessoas=pessoas, produtos=produtos)

def editar_pedido(id):
    pedido = PedidoDoacao.query.get_or_404(id)

    if request.method == 'POST':
        pessoa_id = request.form.get('pessoa_id')
        produto_id = request.form.get('produto_id')
        quantidade = request.form.get('quantidade')

        if not pessoa_id or not produto_id or not quantidade:
            flash('Todos os campos são obrigatórios!', 'danger')
            return redirect(url_for('editar_pedido', id=id))

        pedido.pessoa_id = pessoa_id
        pedido.produto_id = produto_id
        pedido.quantidade = int(quantidade)

        data_pedido = request.form.get('data_pedido')
        if data_pedido:
            pedido.data_pedido = datetime.strptime(data_pedido, "%Y-%m-%d").date()

        db.session.commit()
        flash('Pedido atualizado com sucesso!', 'success')
        return redirect(url_for('listar_pedidos'))

    pessoas = Pessoa.query.all()
    produtos = Produto.query.all()
    return render_template('pedidos/editar.html', pedido=pedido, pessoas=pessoas, produtos=produtos)

def gerar_relatorio_pdf():
    search_pessoa = request.args.get('search_pessoa', '').strip()
    search_produto = request.args.get('search_produto', '').strip()

    pedidos_query = PedidoDoacao.query.join(Pessoa, PedidoDoacao.pessoa_id == Pessoa.id).join(Produto, PedidoDoacao.produto_id == Produto.id)

    if search_pessoa:
        pedidos_query = pedidos_query.filter(Pessoa.nome.ilike(f"%{search_pessoa}%"))
    if search_produto:
        pedidos_query = pedidos_query.filter(Produto.nome_produto.ilike(f"%{search_produto}%"))

    pedidos = pedidos_query.all()

    if not pedidos:
        flash("Nenhum pedido de doação encontrado para gerar o relatório.", "warning")
        return redirect(url_for("listar_pedidos"))

    # **Cria o diretório 'app/static/' se ele não existir**
    pdf_dir = os.path.join("app", "static")
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)

    # Nome do arquivo PDF
    pdf_filename = f"relatorio_pedidos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf_path = os.path.join(pdf_dir, pdf_filename)

    # Criando o PDF com ReportLab
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 40, "Relatório de Pedidos de Doação")

    c.setFont("Helvetica", 12)
    y = height - 80  # Posição inicial

    c.drawString(30, y, "ID")
    c.drawString(70, y, "Pessoa")
    c.drawString(250, y, "Produto")
    c.drawString(400, y, "Quantidade")
    c.drawString(500, y, "Data")
    y -= 20  # Move para a próxima linha

    c.setFont("Helvetica", 10)
    for pedido in pedidos:
        c.drawString(30, y, str(pedido.id))
        c.drawString(70, y, pedido.pessoa.nome[:20])  # Limita para evitar quebra
        c.drawString(250, y, pedido.produto.nome_produto[:20])  # Limita tamanho
        c.drawString(400, y, str(pedido.quantidade))
        c.drawString(500, y, pedido.data_pedido.strftime("%d/%m/%Y"))
        y -= 20  # Move para a próxima linha

        if y < 40:  # Adiciona nova página se necessário
            c.showPage()
            y = height - 80

    c.save()

    # **Retorna a página que exibe o PDF**
    return render_template("pedidos/exibir_relatorio.html", pdf_filename=pdf_filename)
