#!venv/bin/python3
# -*- code: utf-8 -*-
"""
	Clase que define la información que vamos a almacenar del transito de los ususarios del sistema
"""
import datetime

from sqlalchemy import desc

from PiHome import db
from PiHome.dataBase import BaseDB

date_format = '%Y-%m-%d %H:%M:%S'


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

    @staticmethod
    def record_move(**kwargs):
        user = kwargs.get('user')
        action = kwargs.get('action')
        now = datetime.datetime.now()

        move = TransitLog(user=user,
                          action=action,
                          ocurred=now)
        db.session.add(move)
        db.session.commit()

    @staticmethod
    def get_last_move_by_id_user(id_user):
        return TransitLog.query.filter_by(user_id=id_user).order_by(desc(TransitLog.ocurred)).first()
