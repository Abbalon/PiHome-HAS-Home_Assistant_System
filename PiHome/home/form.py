from wtforms import StringField, validators, TextAreaField, Form, PasswordField
from wtforms.fields.html5 import EmailField


class ContactForm(Form):
    """
        Formulario de contacto
    """

    name = StringField('Nombre', [
        validators.length(min=4, max=25, message="¡Huy! Este nombre parece muy raro.")
    ])
    email = EmailField('Email')
    subject = StringField('Asunto')
    message = TextAreaField('Cuerpo del correo')


class LogInForm(Form):
    """
        Formulario de acceso al site
    """
    name = StringField('Nombre')
    password = PasswordField('Contraseña')
