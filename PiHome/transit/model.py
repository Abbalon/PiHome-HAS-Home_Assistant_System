#!/usr/bin/env python3
# -*- code: utf-8 -*-
"""
	Clase que define la información que vamos a almacenar del transito de los ususarios del sistema
"""
import datetime

from PiHome import db
from PiHome.dataBase import BaseDB


class TransitLog(BaseDB):
    """
        Modelo de datos del transito que se registra
    """

    #: Nombre de tabla
    __tablename__ = 'transits_log'

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)

    #: False = fuera // True = Dentro
    action = db.Column(
        db.Boolean,
        default=False,
        nullable=False)

    ocurred = db.Column(
        db.DateTime,
        default=datetime.datetime.now)

    #: Establece la relación con la tabla 'groups'
    user = db.relationship(
        'User',
        lazy='select',
        backref='TransitLog')

    def __init__(self, category=None, definition=None, **kwargs):
        super(TransitLog, self).__init__(**kwargs)
        self.category = category
        self.definition = definition
