#!/usr/bin/env python3
# -*- code: utf-8 -*-
from flask import flash
from wtforms import Form, StringField, validators, SubmitField

from PiHome.card.model import Card


class AddCard(Form):
    """Formulario para dar de alta las tarjetas de acceso"""

    user_id = StringField('Usuario', [
        validators.NumberRange(
            min=1,
            max=None,
            message='Ha de ser un usuario del sistema.'),
        validators.optional
    ])

    card_id = StringField('Tarjeta', [
        validators.length(min=16,
                          max=256,
                          message='No parece que la lonjitud del identificador de la tarjeta sea correcto.'),
        validators.InputRequired(
            message='¡Oh! Una tarjeta no puede existir sin su id.')
    ])

    guardar = SubmitField(True)

    @staticmethod
    def non_duplicate_card(self, ref, user=None):
        """Comprobamos que la rajeta que se trata de guardar, no exista ya
        :param ref id ref de la tarjeta
        :param user usuario al que le vamos a asignar la tarjeta
        """

        card = Card.query.filter_by(ref=ref.data).first()
        if card is not None:
            raise validators.ValidationError(
                message='Ya existe una tarjeta con esta id.')

        user_q = Card.query.filter_by(user_id=user.data).first()
        if user_q is not None:
            flash(
                message='Este usuario ya tiene asignadas más tarjetas',
                category='warning')
