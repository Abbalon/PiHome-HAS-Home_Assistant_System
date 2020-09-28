from flask_wtf import FlaskForm
from wtforms import SubmitField


class ValidateForm(FlaskForm):
    """
        Formulario para capturar que usuario hay que validar o descartar
    """
    # userId = CheckboxField()
    submit = SubmitField('Confirmar')


class UpgradeForm(FlaskForm):
    """
        Formulario para capturar que usuario hay que actualizar
    """

    submit = SubmitField('Confirmar')
