from wtforms import StringField, validators, PasswordField, Form, BooleanField
from wtforms.fields.html5 import EmailField

from PiHome.user.model import User


class SignUpForm(Form):
    """
        Formulario de registro en el site

        Datos requeridos al usuario:
        :name:
        :email:
        :password:
    """

    name = StringField('Nombre', [
        validators.length(min=4, max=25, message="¡Huy! Este nombre parece muy raro."),
        validators.DataRequired(message='¡Ups!. Valoramos tu intimidad como él que más, pero ¡tendrás algún nombre!')
    ])
    password = PasswordField('Contraseña', [
        validators.length(min=4, message="Una contraseña segura debe de tener, al menos, 8 caracteres."),
        validators.DataRequired(message='¡Es indispensable para tu seguridad tener una contraseña!'),
        validators.EqualTo('confirm',
                           message='Para estar seguros de lo que has puesto, tus contraseñas deben coincidir.')
    ])
    confirm = PasswordField('Repite la contraseña', [
        validators.EqualTo('password',
                           message='Para estar seguros de lo que has puesto, tus contraseñas deben coincidir.')
    ])
    email = EmailField('Email', [
        validators.length(max=56, message="¡Huy! No esperábamos un correo tan largo."),
        validators.DataRequired(message="Necesitamos conocer un email, por favor.")
    ])
    accept_tyc = BooleanField('Acepto los TYC', [
        validators.DataRequired()
    ])

    @staticmethod
    def validate_email(self, field):
        """
            Comprueba que el correo introduccido no se encuentre en el sistema
            :param field:
        """

        user = User.query.filter_by(email=field.data).first()
        if user is not None:
            raise validators.ValidationError('Email ya registrado en el sistema.')

    @staticmethod
    def validate_name(self, field):
        """
            Comprueba que el nombre introduccido no se encuentre en el sistema
            :param self:
            :param field:
        """

        user = User.query.filter_by(name=field.data).first()
        if user is not None:
            raise validators.ValidationError('Nombre ya registrado en el sistema.')
