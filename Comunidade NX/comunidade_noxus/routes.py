from flask import render_template, redirect, url_for, flash, request, abort
from comunidade_noxus import app, database, bcrypt
from comunidade_noxus.form import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from comunidade_noxus.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os 
from PIL import Image 

@app.route('/')
def homepage():
    posts= Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)

@app.route('/usuarios')
@login_required
def usuarios():
    return render_template('usuarios.html')

@app.route('/contatos')
@login_required
def contatos():
    return render_template('contatos.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login=FormLogin()
    form_criarconta=FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_logar' in request.form:
        usuario=Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f"Você está logado no email: {form_login.email.data}", "alert-success")
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for("homepage"))
        else:
            flash("Email ou senha incorretos, tente novamente")

    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript=bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario=Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        flash(f"Você criou o email: {form_login.email.data}", 'alert-success')

        return redirect(url_for("homepage"))

    return render_template('login.html',  form_login=form_login,  form_criarconta=form_criarconta)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash("Logout feito com sucesso!")
    return redirect(url_for('homepage'))

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil=url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)

@app.route('/post/criar', methods=['GET', 'POST'] )
@login_required
def criar_post():
    form_criarpost=FormCriarPost()
    if form_criarpost.validate_on_submit():
        post=Post(titulo=form_criarpost.titulo.data, corpo=form_criarpost.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash("Post criado com sucesso")
        return redirect(url_for('homepage'))
    return render_template('criarpost.html', form_criarpost=form_criarpost, autor=current_user)


def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extesao = os.path.splitext(imagem.filename)
    nome_arquivo=nome + codigo + extesao
    caminho_completo=os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    
    tamanho=(200, 200)
    imagem_reduzida=Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form_editarperfil=FormEditarPerfil()
    if form_editarperfil.validate_on_submit():
        current_user.email=form_editarperfil.email.data
        current_user.username=form_editarperfil.username.data
        
        if form_editarperfil.foto_perfil.data:
            nome_imagem=salvar_imagem(form_editarperfil.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        database.session.commit()
        flash("Atualizado com sucesso!")
        return redirect(url_for('perfil'))
    
    elif request.method == 'GET':
        form_editarperfil.email.data=current_user.email
        form_editarperfil.username.data=current_user.username

    foto_perfil=url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editar_perfil.html', foto_perfil=foto_perfil, form_editarperfil=form_editarperfil)

@login_required
@app.route('/post/<post_id>', methods=['GET', 'POST'])
def exibir_post(post_id):
    post=Post.query.get(post_id)
    if current_user == post.autor:
        form_criarpost=FormCriarPost()
        
        if request.method == 'GET':
            form_criarpost.titulo.data = post.titulo
            form_criarpost.corpo.data = post.corpo
            
        elif form_criarpost.validate_on_submit:
            post.titulo=form_criarpost.titulo.data
            post.corpo=form_criarpost.corpo.data
            database.session.commit()
            flash('Post atualizado !')
            return redirect(url_for('homepage'))
    else:
        form_criarpost=None
        
    return render_template( 'post.html', post=post, form_criarpost=form_criarpost)


@login_required
@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
def excluir_post(post_id):
    post=Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluido com Sucesso !', '  alert-danger')
        return redirect(url_for('homepage'))
    
    else:
        abort(403)