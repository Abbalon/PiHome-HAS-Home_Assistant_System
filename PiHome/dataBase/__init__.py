#!venv/bin/python3
# -*- code: utf-8 -*-
"""
Clase que declara e instancia la conexión con la base de datos
"""

from PiHome import db


class BaseDB(db.Model):
    """
    Define los elementos comunes a todas las tablas que lo heredarán
    """
    __abstract__ = True

    id = db.Column(
        db.Integer,
        primary_key=True)

    date_created = db.Column(
        db.DateTime,
        default=db.func.current_timestamp())

    date_modified = db.Column(
        db.DateTime,
        onupdate=db.func.current_timestamp())

    def save(self):
        """
        Guarda el objeto en la BBDD
        """
        db.session.add(self)
        db.session.commit()
