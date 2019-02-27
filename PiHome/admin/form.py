from flask_wtf import Form
from wtforms import SubmitField


class ValidateForm(Form):
    """
        Formulario para capturar que usuario hay que validar o descartar
    """
    # userId = CheckboxField()
    submit = SubmitField('Confirmar')


class UpgradeForm(Form):
    """
        Formulario para capturar que usuario hay que actualizar
    """

    submit = SubmitField('Confirmar')
