from flask import render_template, request, redirect, url_for, flash
from app.models.pedido_doacao import PedidoDoacao
from app.models.pessoa import Pessoa
from app.models.produto import Produto
from app.__init__ import db
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

# ----------------------------
# Helpers de filtro e ordenação
# ----------------------------

def _aplicar_filtros_basicos(query, search_pessoa: str = "", search_produto: str = ""):
    if search_pessoa:
        query = query.filter(Pessoa.nome.ilike(f"%{search_pessoa}%"))
    if search_produto:
        query = query.filter(Produto.nome_produto.ilike(f"%{search_produto}%"))
    return query

def _aplicar_filtro_datas(query, data_inicial: str = None, data_final: str = None):
    """
    Aplica filtro por intervalo em PedidoDoacao.data_pedido (DateTime).
    - data_inicial e data_final: 'YYYY-MM-DD'
    - Se apenas uma for informada, aplica filtro aberto do outro lado.
    - data_final inclui o dia inteiro (23:59:59).
    """
    if not data_inicial and not data_final:
        return query

    ini_dt = None
    fim_dt = None
    try:
        if data_inicial:
            ini_dt = datetime.strptime(data_inicial, "%Y-%m-%d")
        if data_final:
            fim_dt = datetime.strptime(data_final, "%Y-%m-%d") + timedelta(hours=23, minutes=59, seconds=59)
    except ValueError:
        flash('Formato de data inválido. Use AAAA-MM-DD.', 'warning')
        return query

    if ini_dt and fim_dt:
        return query.filter(PedidoDoacao.data_pedido.between(ini_dt, fim_dt))
    if ini_dt:
        return query.filter(PedidoDoacao.data_pedido >= ini_dt)
    if fim_dt:
        return query.filter(PedidoDoacao.data_pedido <= fim_dt)
    return query

def _aplicar_ordenacao(query, order_by: str):
    """
    Opções:
      - data_desc (padrão), data_asc
      - pessoa_asc, pessoa_desc
      - produto_asc, produto_desc
    """
    if order_by == 'data_asc':
        return query.order_by(PedidoDoacao.data_pedido.asc())
    if order_by == 'pessoa_asc':
        return query.order_by(Pessoa.nome.asc(), PedidoDoacao.data_pedido.desc())
    if order_by == 'pessoa_desc':
        return query.order_by(Pessoa.nome.desc(), PedidoDoacao.data_pedido.desc())
    if order_by == 'produto_asc':
        return query.order_by(Produto.nome_produto.asc(), PedidoDoacao.data_pedido.desc())
    if order_by == 'produto_desc':
        return query.order_by(Produto.nome_produto.desc(), PedidoDoacao.data_pedido.desc())
    # Padrão
    return query.order_by(PedidoDoacao.data_pedido.desc())

# ----------------------------
# CRUD / Listagem
# ----------------------------

def listar_pedidos():
    search_pessoa  = request.args.get('search_pessoa', '').strip()
    search_produto = request.args.get('search_produto', '').strip()
    data_inicial   = request.args.get('data_inicial')
    data_final     = request.args.get('data_final')
    order_by       = request.args.get('order_by', 'data_desc')

    pedidos_query = (PedidoDoacao.query
                     .join(Pessoa, PedidoDoacao.pessoa_id == Pessoa.id)
                     .join(Produto, PedidoDoacao.produto_id == Produto.id))

    pedidos_query = _aplicar_filtros_basicos(pedidos_query, search_pessoa, search_produto)
    pedidos_query = _aplicar_filtro_datas(pedidos_query, data_inicial, data_final)
    pedidos_query = _aplicar_ordenacao(pedidos_query, order_by)

    pedidos = pedidos_query.all()
    return render_template('pedidos/lista.html', pedidos=pedidos)

def cadastrar_pedido():
    if request.method == 'POST':
        pessoa_id  = request.form.get('pessoa_id')
        produto_id = request.form.get('produto_id')
        quantidade = request.form.get('quantidade', type=int)

        if not pessoa_id or not produto_id or not quantidade:
            flash('Todos os campos são obrigatórios!', 'danger')
            return redirect(url_for('cadastrar_pedido'))

        pessoa = Pessoa.query.get(pessoa_id)
        if not pessoa or not pessoa.ativo:
            flash('Pessoa inválida ou inativa.', 'danger')
            return redirect(url_for('cadastrar_pedido'))

        produto = Produto.query.get(produto_id)
        if not produto:
            flash('Produto inválido.', 'danger')
            return redirect(url_for('cadastrar_pedido'))

        novo_pedido = PedidoDoacao(
            pessoa_id=pessoa.id,
            produto_id=produto.id,
            quantidade=quantidade,
            data_pedido=datetime.utcnow()
        )
        db.session.add(novo_pedido)
        db.session.commit()
        flash('Pedido de doação cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_pedidos'))

    # GET: se o template já busca pessoa via autocomplete, você pode
    # reduzir a carga e enviar apenas os produtos:
    produtos = Produto.query.order_by(Produto.nome_produto.asc()).all()
    return render_template('pedidos/cadastro.html', produtos=produtos)
def editar_pedido(id):
    pedido = PedidoDoacao.query.get_or_404(id)

    if request.method == 'POST':
        pessoa_id  = request.form.get('pessoa_id')
        produto_id = request.form.get('produto_id')
        quantidade = request.form.get('quantidade')

        if not pessoa_id or not produto_id or not quantidade:
            flash('Todos os campos são obrigatórios!', 'danger')
            return redirect(url_for('editar_pedido', id=id))

        pedido.pessoa_id  = pessoa_id
        pedido.produto_id = produto_id
        pedido.quantidade = int(quantidade)

        data_pedido = request.form.get('data_pedido')
        if data_pedido:
            # Interpreta como 00:00 local; mantém DateTime no banco
            pedido.data_pedido = datetime.strptime(data_pedido, "%Y-%m-%d")

        db.session.commit()
        flash('Pedido atualizado com sucesso!', 'success')
        return redirect(url_for('listar_pedidos'))

    pessoas = Pessoa.query.all()
    produtos = Produto.query.all()
    return render_template('pedidos/editar.html', pedido=pedido, pessoas=pessoas, produtos=produtos)

def delete_pedido(id):
    pedido = PedidoDoacao.query.get_or_404(id)
    db.session.delete(pedido)
    db.session.commit()
    flash('Pedido excluído com sucesso!', 'success')
    return redirect(url_for('listar_pedidos'))

# ----------------------------
# Relatórios (HTML e PDF)
# ----------------------------

def relatorio_pedidos():
    """
    Exibe página de relatório (HTML) opcional, caso exista template 'relatorio_pedidos.html'.
    Usa os mesmos filtros/ordenação.
    """
    search_pessoa  = request.args.get('search_pessoa', '').strip()
    search_produto = request.args.get('search_produto', '').strip()
    data_inicial   = request.args.get('data_inicial')
    data_final     = request.args.get('data_final')
    order_by       = request.args.get('order_by', 'data_desc')

    pedidos_query = (PedidoDoacao.query
                     .join(Pessoa, PedidoDoacao.pessoa_id == Pessoa.id)
                     .join(Produto, PedidoDoacao.produto_id == Produto.id))

    pedidos_query = _aplicar_filtros_basicos(pedidos_query, search_pessoa, search_produto)
    pedidos_query = _aplicar_filtro_datas(pedidos_query, data_inicial, data_final)
    pedidos_query = _aplicar_ordenacao(pedidos_query, order_by)

    pedidos = pedidos_query.all()
    return render_template('relatorio_pedidos.html', pedidos=pedidos)

def gerar_relatorio_pdf():
    """
    Compat: nome legado. Gera PDF respeitando filtros e ordenação.
    """
    return relatorio_pedidos_pdf()

def relatorio_pedidos_pdf():
    """
    Gera PDF respeitando filtros de pessoa/produto, intervalo de datas e ordenação.
    Endpoint recomendado para as rotas/templates: 'relatorio_pedidos_pdf'.
    """
    search_pessoa  = request.args.get('search_pessoa', '').strip()
    search_produto = request.args.get('search_produto', '').strip()
    data_inicial   = request.args.get('data_inicial')
    data_final     = request.args.get('data_final')
    order_by       = request.args.get('order_by', 'data_desc')

    pedidos_query = (PedidoDoacao.query
                     .join(Pessoa, PedidoDoacao.pessoa_id == Pessoa.id)
                     .join(Produto, PedidoDoacao.produto_id == Produto.id))

    pedidos_query = _aplicar_filtros_basicos(pedidos_query, search_pessoa, search_produto)
    pedidos_query = _aplicar_filtro_datas(pedidos_query, data_inicial, data_final)
    pedidos_query = _aplicar_ordenacao(pedidos_query, order_by)

    pedidos = pedidos_query.all()

    if not pedidos:
        flash("Nenhum pedido de doação encontrado para gerar o relatório.", "warning")
        return redirect(url_for("listar_pedidos"))

    # Garante diretório do PDF
    pdf_dir = os.path.join("app", "static")
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)

    pdf_filename = f"relatorio_pedidos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf_path = os.path.join(pdf_dir, pdf_filename)

    # Monta PDF (ReportLab)
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(170, height - 40, "Relatório de Pedidos de Doação")

    # Filtros no topo
    c.setFont("Helvetica", 10)
    filtro_y = height - 60
    filtros_txt = []
    if search_pessoa:  filtros_txt.append(f"Pessoa contém: {search_pessoa}")
    if search_produto: filtros_txt.append(f"Produto contém: {search_produto}")
    if data_inicial:   filtros_txt.append(f"De: {data_inicial}")
    if data_final:     filtros_txt.append(f"Até: {data_final}")
    mapa_ob = {
        'data_desc': 'Data (mais recente)',
        'data_asc': 'Data (mais antiga)',
        'pessoa_asc': 'Pessoa (A→Z)',
        'pessoa_desc': 'Pessoa (Z→A)',
        'produto_asc': 'Produto (A→Z)',
        'produto_desc': 'Produto (Z→A)',
    }
    filtros_txt.append(f"Ordenação: {mapa_ob.get(order_by, 'Data (mais recente)')}")
    c.drawString(30, filtro_y, "Filtros: " + " | ".join(filtros_txt))

    # Cabeçalho
    c.setFont("Helvetica-Bold", 12)
    y = height - 90
    c.drawString(30,  y, "ID")
    c.drawString(70,  y, "Pessoa")
    c.drawString(250, y, "Produto")
    c.drawString(400, y, "Qtd")
    c.drawString(450, y, "Data")
    y -= 18

    # Linhas
    c.setFont("Helvetica", 10)
    for pedido in pedidos:
        c.drawString(30,  y, str(pedido.id))
        c.drawString(70,  y, (pedido.pessoa.nome or "")[:28])
        c.drawString(250, y, (pedido.produto.nome_produto or "")[:28])
        c.drawString(400, y, str(pedido.quantidade))
        c.drawString(450, y, pedido.data_pedido.strftime("%d/%m/%Y") if pedido.data_pedido else "")
        y -= 16
        if y < 40:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = height - 40

    c.save()
    return render_template("pedidos/exibir_relatorio.html", pdf_filename=pdf_filename)
