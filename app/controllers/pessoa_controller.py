from flask import render_template, request, redirect, url_for, flash
from app.models.pessoa import Pessoa
from app.models.doacao import Doacao
from app.__init__ import db
from datetime import datetime
from flask import jsonify

def listar_pessoas():
    search = request.args.get('search', '').strip()  # Obtém o valor da busca
    if search:
        pessoas = Pessoa.query.filter(Pessoa.nome.ilike(f"%{search}%")).all()  # Filtra por nome
    else:
        pessoas = Pessoa.query.filter_by(ativo=True).all()  # Retorna todas as pessoas ativas
    for pessoa in pessoas:
        pessoa.doacoes = Doacao.query.filter_by(pessoa_id=pessoa.id).all()
    return render_template('pessoas/lista.html', pessoas=pessoas, search=search)

def cadastrar_pessoa():
    if request.method == 'POST':
        nome = request.form['nome']
        endereco = request.form['endereco']
        bairro = request.form['bairro']
        telefone = request.form['telefone']
        filhos = request.form['filhos']
        profissao = request.form['profissao']
        qtd_pessoas = request.form['qtd_pessoas']
        locomocao = request.form['locomocao']
        #data_cadastro = request.form['data_cadastro']
        data_cadastro = datetime.strptime(request.form['data_cadastro'], "%Y-%m-%d").date()

        nova_pessoa = Pessoa(nome=nome, endereco=endereco, bairro=bairro, telefone=telefone,
                             filhos=filhos, profissao=profissao, qtd_pessoas=qtd_pessoas,
                             locomocao=locomocao, data_cadastro=data_cadastro)

        db.session.add(nova_pessoa)
        db.session.commit()
        flash('Pessoa cadastrada com sucesso!', 'success')
        return redirect(url_for('listar_pessoas'))
    return render_template('pessoas/cadastro.html')

def editar_pessoa(id):
    pessoa = Pessoa.query.get_or_404(id)

    if request.method == 'POST':
        pessoa.nome = request.form['nome']
        pessoa.endereco = request.form['endereco']
        pessoa.bairro = request.form['bairro']
        pessoa.telefone = request.form['telefone']
        pessoa.filhos = request.form['filhos']
        pessoa.profissao = request.form['profissao']
        pessoa.qtd_pessoas = request.form['qtd_pessoas']
        pessoa.locomocao = request.form['locomocao']

        db.session.commit()
        flash('Pessoa atualizada com sucesso!', 'success')
        return redirect(url_for('listar_pessoas'))

    return render_template('pessoas/editar.html', pessoa=pessoa)

def desativar_pessoa(id):
    pessoa = Pessoa.query.get_or_404(id)
    if pessoa.ativo == False:
        pessoa.ativo = True
    else:
        pessoa.ativo = False
    db.session.commit()
    flash('Pessoa desativada com sucesso!', 'success')
    return redirect(url_for('listar_pessoas'))

def listar_pessoas_inativas():
    pessoas = Pessoa.query.filter_by(ativo=False).all()
    return render_template('pessoas/lista.html', pessoas=pessoas)


def buscar_pessoas():
    q = (request.args.get('q') or '').strip()
    if len(q) < 2:
        return jsonify([])

    termo = f"%{q}%"
    pessoas = (Pessoa.query
               .filter(Pessoa.ativo.is_(True))
               .filter(
                   (Pessoa.nome.ilike(termo)) |
                   (Pessoa.telefone.ilike(termo)) |
                   (Pessoa.bairro.ilike(termo))
               )
               .order_by(Pessoa.nome.asc())
               .limit(20)
               .all())

    payload = [{
        "id": p.id,
        "nome": p.nome,
        "telefone": p.telefone,
        "bairro": p.bairro,
        "ativo": p.ativo
    } for p in pessoas]
    return jsonify(payload)