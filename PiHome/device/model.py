#!/usr/bin/env python3
# -*- code: utf-8 -*-
"""
Clase que define la información que vamos a almacenar de los dispositivos implementados y sus funciones
"""

from PiHome import db
from PiHome.dataBase import BaseDB


class Device(BaseDB):
    """
    Modelo que recogera la información relativa a un dispositivo
    """

    #: Nombre de la tabla
    __tablename__ = 'devices'

    name = db.Column(
        db.String(32),
        nullable=False,
        unique=True
    )

    interface = db.Column(
        db.String(32)
    )

    id_external = db.Column(
        db.String(64),
        nullable=False,
        unique=True
    )

    id_remote = db.Column(
        db.String(64),
        nullable=False,
        unique=True
    )

    enabled = db.Column(
        db.Boolean,
        default=False)

    def __init__(self, name, id_external, id_remote, enabled, interface=None, **kwargs):
        super(Device, self).__init__(**kwargs)
        if name:
            self.name = name
        if interface:
            self.interface = interface
        if enabled:
            self.enabled = enabled
        self.id_external = id_external
        self.id_remote = id_remote

    @staticmethod
    def get_active_device_by_id(id: int):
        """Retorna el dispositivo si estaá habilitado"""
        return Device.query.filter_by(id=id, enabled=1).first()

    @staticmethod
    def get_active_devices():
        """Retorna los dispositivos que estén habilitados"""
        return Device.query.filter_by(enabled=1).all()


class Action(BaseDB):
    """
    Modelo que recoge las acciones que tiene definidas un dispositivo
    """
    #: Nombre de la tabla
    __tablename__ = 'actions'

    id_device = db.Column(
        db.Integer,
        db.ForeignKey('devices.id'),
        nullable=False)

    device = db.relationship(
        'Device',
        lazy='select',
        backref='Action'
    )

    name = db.Column(
        db.String(32),
        nullable=False
    )

    description = db.Column(
        db.String(255))

    #: Define el nombre del comando a realizar
    cmd = db.Column(
        db.String(64),
        nullable=False)

    #: Define si es un comando de entrada
    is_executable = db.Column(
        db.Boolean,
        nullable=False)

    def __init__(self, device, name, cmd, way, description=None, **kwargs):
        super(Action, self).__init__(**kwargs)
        if name:
            self.name = name
        if device:
            self.id_device = device
        if cmd:
            self.cmd = cmd
        if way:
            self.is_executable = way
        self.description = description

    @staticmethod
    def get_executable_action(action, device: Device = None):
        if device:
            return Action.query.filter_by(id=action, id_device=device.id, is_executable=1).first()
        else:
            return Action.query.filter_by(id=action, is_executable=1).first()

    @staticmethod
    def get_executable_actions(device: Device = None):
        if device:
            return Action.query.filter_by(id_device=device.id, is_executable=1).all()
        else:
            return Action.query.filter_by(is_executable=1).all()
