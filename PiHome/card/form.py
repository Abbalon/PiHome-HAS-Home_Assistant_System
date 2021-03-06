#!venv/bin/python3
# -*- code: utf-8 -*-
from wtforms import Form, StringField, validators, SelectField, Label
from wtforms.fields import SubmitField

from PiHome.card.model import Card


class AddCardForm(Form):
    """Formulario para dar de alta las tarjetas de acceso"""

    user = "Usuario"
    user_name_lb = Label(field_id="user_select", text=user)
    user_select = SelectField(user, coerce=int, validate_choice=False)

    tag = "Tarjeta"
    tag_lb = Label(field_id="card_id", text=tag)
    card_id = StringField(tag, [
        validators.length(min=12,
                          max=256,
                          message='No parece que la lonjitud del identificador de la tarjeta sea correcto.')
    ])

    guardar_btn = SubmitField(label="Registrar")
    leer_btn = SubmitField(label="Leer")

    def validate_card_id(self, field):
        """Comprobamos que la rajeta que se trata de guardar, no exista ya

        ---

        :param ref id ref de la tarjeta
        :param user usuario al que le vamos a asignar la tarjeta
        """

        if not field.data or len(field.data) == 0:
            raise validators.ValidationError("No se puede crear una tarjeta sin asignarle una id")

        card = Card.query.filter_by(ref=field.data).first()
        if card is not None:
            raise validators.ValidationError(
                message='Ya existe una tarjeta con esta id.')
