#!venv/bin/python3
# -*- code: utf-8 -*-
"""
	Clase que define la información que vamos a almacenar de las tarjetas RFID
"""

from PiHome import db
from PiHome.dataBase import BaseDB
from PiHome.user.model import User


class Card(BaseDB):
    # Nombre de la tabla
    __tablename__ = 'cards'

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        default=None
    )

    ref = db.Column(
        db.String(150),
        unique=True,
        default=None
    )

    user = db.relationship(
        'User',
        lazy='select',
        backref='Card'
    )

    def __init__(self, **kwargs):
        """ Inicializa los datos de una tarjeta RFID

        @:param user el usuario al que va a estar asignada
        @:param ref numeración de la tarjeta
        """
        super(Card, self).__init__(**kwargs)

        for key, value in kwargs.items():
            if key == 'user':
                self.user_id = value

            if key == 'ref':
                self.ref = value

    @classmethod
    def get_user_from_tag(cls, **kwargs):
        """Devuelve el usuario a quién corresponda la tarjeta recibida por parámetro
        @param id_tag: id d ela targeta RFID que identifica al usuario. None si no está habilitado o no existe"""
        response = None
        id_tag = kwargs.get("id_tag")
        if id_tag:
            card = Card.query.filter_by(ref=id_tag).first()
            if card:
                user = card.user
                if user.validated:
                    response = user
        return response
