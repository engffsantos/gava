from flask import Blueprint, render_template
from app.models.pessoa import Pessoa
from app.models.produto import Produto
from app.models.doacao import Doacao
from app.models.evento import Evento
from sqlalchemy import func
from app import db

bp_dashboard = Blueprint('dashboard', __name__)

@bp_dashboard.route('/')
@bp_dashboard.route('/dashboard')
def dashboard():
    # Estatísticas
    total_pessoas = db.session.query(func.count(Pessoa.id)).scalar()
    total_produtos = db.session.query(func.count(Produto.id)).scalar()
    total_doacoes = db.session.query(func.count(Doacao.id)).scalar()

    # Produtos com estoque baixo (ex: < 5)
    produtos_baixo_estoque = db.session.query(Produto).filter(Produto.quantidade < 5).count()

    stats = {
        'total_pessoas': total_pessoas,
        'total_produtos': total_produtos,
        'total_doacoes': total_doacoes,
        'produtos_baixo_estoque': produtos_baixo_estoque
    }

    # Doações recentes
    # Doações recentes
    doacoes_raw = db.session.query(Doacao).join(Pessoa).join(Produto) \
        .order_by(Doacao.data_doacao.desc()).limit(5).all()

    doacoes_recentes = [
        {
            'pessoa': doacao.pessoa.nome,
            'produto': doacao.produto.nome_produto,
            'quantidade': doacao.quantidade,
            'data': doacao.data_doacao.strftime('%d/%m/%Y')
        }
        for doacao in doacoes_raw
    ]

    # Produtos mais doados
    produtos_raw = db.session.query(
        Produto.nome_produto,
        func.sum(Doacao.quantidade).label('total')
    ).join(Doacao).group_by(Produto.nome_produto) \
        .order_by(func.sum(Doacao.quantidade).desc()).limit(5).all()

    produtos_top = [
        {'nome': produto.nome_produto, 'total': produto.total}
        for produto in produtos_raw
    ]

    # Doadores mais ativos
    doadores_top = db.session.query(
        Pessoa.nome,
        func.count(Doacao.id).label('total')
    ).join(Doacao).group_by(Pessoa.nome)\
     .order_by(func.count(Doacao.id).desc()).limit(5).all()

    # Eventos mais próximos
    eventos_proximos = db.session.query(Evento).order_by(Evento.data.desc()).limit(5).all()

    return render_template('dashboard.html',
                           stats=stats,
                           doacoes_recentes=doacoes_recentes,
                           produtos_top=produtos_top,
                           doadores_top=doadores_top,
                           eventos_proximos=eventos_proximos)
