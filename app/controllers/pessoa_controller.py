from datetime import datetime

from flask import render_template, request, redirect, url_for, flash
from app.models.pessoa import Pessoa
from app.__init__ import db

def listar_pessoas():
    pessoas = Pessoa.query.all()
    return render_template('pessoas/lista.html', pessoas=pessoas)

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
