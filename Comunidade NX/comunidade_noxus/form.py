from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidade_noxus.models import Usuario
from flask_login import current_user

class FormCriarConta(FlaskForm):
    username= StringField('Nome de usuário', validators=[DataRequired()]) 
    email=StringField('Email', validators=[DataRequired(),Email() ])
    senha =PasswordField('Senha', validators=[DataRequired(), Length(6, 20 )])
    confirmacao=PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta=SubmitField('Criar conta')

    def validate_email(self, email):
        usuario=Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email já cadastrado, tente novamente!')
    
class FormLogin(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), Email()])
    senha =PasswordField('Senha', validators=[DataRequired(), Length(6, 20)]) 
    lembrar_dados= BooleanField('Lembrar Dados')
    botao_submit_logar=SubmitField('Login')

    
class FormEditarPerfil(FlaskForm):
    username= StringField('Nome de usuário', validators=[DataRequired()]) 
    email=StringField('Email', validators=[DataRequired(),Email() ])
    foto_perfil=FileField('Atualizar Foto de Perfil!', validators=[FileAllowed(['jpg', 'png'])])
    botao_submit_editarperfil=SubmitField('Salvar')
    
    def validate_email(self, email):
        if current_user.email != email.data:
            usuario=Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Email digitado já está em uso por outro usuário, tente outro!')
            
class FormCriarPost(FlaskForm):
    titulo = StringField('Titulo ', validators=[DataRequired(),  Length(2, 140)])
    corpo = TextAreaField('"Escreva seu post Aqui ', validators=[DataRequired()])
    botao_submit =  botao_submit_editarperfil=SubmitField('Salvar')