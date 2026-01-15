# Criar routas
from flask import render_template, url_for, redirect, flash, abort
from fekepinterest import*
from fekepinterest.models import*
from flask_login import login_required, login_user, logout_user, current_user
from fekepinterest.forms import*
import os
from werkzeug.utils import secure_filename


@app.route("/", methods=["GET", "POST"])
def homepage():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrytp.check_password_hash(usuario.senha, form_login.senha.data):
            usuario = Usuario.query.filter_by(email=form_login.email.data).first()
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("homepage.html", form_login=form_login)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

@app.route("/perfil/<id_usuario>", methods=["POST", "GET"])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            # Salvar o Arquivo na pasta
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"], nome_seguro)
            arquivo.save(caminho)
            # Registar o arquivo no banco de dados
            foto = Fotos(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
        return render_template("perfil.html", usuario=current_user, form=form_foto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
    return render_template("perfil.html", usuario=usuario, form=None)

@app.route("/foto/<id_foto>/excluir", methods=["GET", "POST"])
@login_required
def excluir_foto(id_foto):
    foto = Fotos.query.get(id_foto)
    if current_user == foto.imagem:
        database.session.delete(foto)
        database.session.commit()
        flash('A foto excluido com sucesso', 'alert-danger')
        return redirect(url_for('perfil'))
    else:
        abort(405)


@app.route("/criarconta", methods=["GET", "POST"])
def criar_conta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():
        senha = bcrytp.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data, senha=senha, email=form_criarconta.email.data)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("criarconta.html", form=form_criarconta)

@app.route("/feed")
@login_required
def feed():
    fotos = Fotos.query.order_by(Fotos.data_criacao.desc()).all()
    return render_template("feed.html", fotos=fotos)