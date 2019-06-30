#!/usr/bin/env python3
# -*- code: utf-8 -*-
"""
	Clase que define la información que vamos a almacenar de las tarjetas RFID
"""

from PiHome import db
from PiHome.dataBase import BaseDB


class Card(BaseDB):
    # Nombre de la tabla
    __tablename__ = 'cards'

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        default=None
    )

    ref = db.Column(
        db.String(256),
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
