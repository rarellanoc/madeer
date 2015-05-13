from flask.ext.wtf import Form, fields, validators, Required, Email, ValidationError, Length, Regexp
from wtforms import widgets
from models import User, ListaUsuarios
from app import db


def validate_login(form, field):
    user = form.get_user()
    if user is None:
        raise validators.ValidationError('Usuario no valido')
    if user.password != form.password.data:
        raise validators.ValidationError('Clave no valida')


class InscripcionUserForm(Form):
    email = fields.TextField('', validators=[Required(), Email(), Regexp('[\w|.|-]*@\w*\.[\w|.]*', message=('No es un correo valido'))])

    def validate_email(self, field):
        if db.session.query(ListaUsuarios).filter_by(email=self.email.data).count() > 0:
            raise validators.ValidationError('Correo duplicado')




class LoginForm(Form):
    email = fields.TextField('Correo', validators=[Required(), Email()])
    password = fields.PasswordField('Clave', validators=[Required(), validate_login])

    def get_user(self):
        return db.session.query(User).filter_by(email=self.email.data).first()


class ForgotPasswordForm(Form):
    email = fields.TextField(validators=['Correo', Required(), Email()])

    def get_user(self):
        return db.session.query(User).filter_by(email=self.email.data).first()


class RegistrationForm(Form):
    email = fields.TextField('Correo', validators=[Required(), Email(), Regexp('[^@]+@[a-z]+\.[a-z]+', message=('No pertenece a inacapmail'))])
    consent = fields.BooleanField(validators=[Required()])
    password = fields.PasswordField('Nueva Clave', [
        validators.Required(), validators.Length(min=8, max=20),
        validators.EqualTo('confirm', message='La clave debe coincidir')
    ])
    confirm = fields.PasswordField('Confirmar',validators=[Required()])

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=self.email.data).count() > 0:
            raise validators.ValidationError('Correo duplicado')


class NewPass(Form):
    password = fields.PasswordField('Nueva Clave', [
        validators.Required(), validators.Length(min=8, max=20),
        validators.EqualTo('confirm', message='La clave debe coincidir')
    ])
    confirm = fields.PasswordField('Confirmar',validators=[Required()])





class MetaForm(Form):
	navbar = fields.TextField('Navbar')
	titulo = fields.TextField('Titulo')
	subtitulo = fields.TextField('Subtitulo')
	motd = fields.TextField('MOTD')
	fecha_motd = fields.TextField('fecha')
	



