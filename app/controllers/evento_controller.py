from flask import render_template, request, redirect, url_for, flash
from app.__init__ import db
from app.models.evento import Evento


def listar_eventos():
    eventos = Evento.query.order_by(Evento.data.desc()).all()
    return render_template('eventos/lista.html', eventos=eventos)


def cadastrar_evento():
    if request.method == 'POST':
        nome = request.form['nome']
        local = request.form['local']
        data = request.form['data']
        doacao_para = request.form['doacao_para']
        doacao = request.form['doacao']

        novo_evento = Evento(
            nome=nome,
            local=local,
            data=data,
            doacao_para=doacao_para,
            doacao=doacao
        )
        db.session.add(novo_evento)
        db.session.commit()
        flash('Evento cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_eventos'))

    return render_template('eventos/cadastro.html')


def editar_evento(id):
    evento = Evento.query.get_or_404(id)

    if request.method == 'POST':
        evento.nome = request.form['nome']
        evento.local = request.form['local']
        evento.data = request.form['data']
        evento.doacao_para = request.form['doacao_para']
        evento.doacao = request.form['doacao']

        db.session.commit()
        flash('Evento atualizado com sucesso!', 'success')
        return redirect(url_for('listar_eventos'))

    return render_template('eventos/editar.html', evento=evento)


def excluir_evento(id):
    evento = Evento.query.get_or_404(id)
    db.session.delete(evento)
    db.session.commit()
    flash('Evento excluído com sucesso!', 'success')
    return redirect(url_for('listar_eventos'))
