#!venv/bin/python3
# -*- code: utf-8 -*-
"""
Clase que define la información que vamos a almacenar de los dispositivos implementados y sus funciones
"""
from sqlalchemy import desc

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
        unique=False
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

    @staticmethod
    def get_device_by_mac(device_mac):
        return Device.query.filter_by(id_external=device_mac).all()


class Family(BaseDB):
    """
    Modelo que recoge las acciones que tiene definidas un dispositivo
    """
    #: Nombre de la tabla
    __tablename__ = 'family'

    name = db.Column(
        db.String(32),
        nullable=False
    )

    description = db.Column(
        db.String(255)
    )

    def __init__(self, name, description, **kwargs):
        super(Family, self).__init__(**kwargs)
        self.name = name
        self.description = description


class Action(BaseDB):
    """
    Modelo que recoge las acciones que puede tener definidas un dispositivo
    """
    #: Nombre de la tabla
    __tablename__ = 'actions'

    id_family = db.Column(
        db.Integer,
        db.ForeignKey('family.id'),
        nullable=False)

    family = db.relationship(
        'Family',
        lazy='select',
        backref='Action'
    )

    name = db.Column(
        db.String(32),
        nullable=False
    )

    description = db.Column(
        db.String(255)
    )

    #: Define el nombre del comando a realizar
    cmd = db.Column(
        db.String(64),
        nullable=False)

    #: Define si es un comando de entrada
    is_executable = db.Column(
        db.Boolean,
        nullable=False,
        default=1
    )

    response_needed = db.Column(
        db.Boolean,
        nullable=False,
        default=0
    )

    def __init__(self, **kwargs):
        super(Action, self).__init__(**kwargs)
        for key, value in kwargs.items():
            if key == 'family':
                self.family = value
            if key == 'name':
                self.name = value
            if key == 'cmd':
                self.cmd = value
            if key == 'way':
                self.is_executable = value
            if key == 'response_needed':
                self.response_needed = value

    @staticmethod
    def get_executable_action(action, device: Device):
        """@param action id de la acciona a ejecutar
        @param device type:Device Dispositivo que realizará la acción
        @raise Exception Si la acciona a realizar no está especificada para el dispositivo"""
        if device:
            family_list = FamilyDevice.get_familys(device)
            actions = []
            for family in family_list:
                for _action in family.Action:
                    actions.append(_action.id)
            if action in actions:
                return Action.query.filter_by(id=action, is_executable=1).first()
        else:
            return None

    @staticmethod
    def get_executable_actions(device: Device = None):
        if device:
            familys = FamilyDevice.get_familys(device)
            actions = []
            for family in familys:
                for action in family.Action:
                    actions.append(action)
            return actions
        else:
            return Action.query.filter_by(is_executable=1).all()

    @staticmethod
    def get_actions_from_family(family: Family):
        """Devuelve las acciones de una familia"""
        return Action.query.filter_by(id_family=family.id, is_executable=1).all().order_by(desc(Action.id))


class FamilyDevice(BaseDB):
    """
        Modelo que recoge las familias a las que está relacionado un dispositivo
        """
    #: Nombre de la tabla
    __tablename__ = 'family_device'

    id_device = db.Column(
        db.Integer,
        db.ForeignKey('devices.id'),
        nullable=False)

    device = db.relationship(
        'Device',
        lazy='select',
        backref='Family'
    )

    id_family = db.Column(
        db.Integer,
        db.ForeignKey('family.id'),
        nullable=False)

    family = db.relationship(
        'Family',
        lazy='select',
        backref='Device'
    )

    def __init__(self, **kwargs):
        super(FamilyDevice, self).__init__(**kwargs)
        for key, value in kwargs.items():
            if key == 'device':
                self.device = value
            if key == 'family':
                self.family = value

    @staticmethod
    def get_familys(device: Device):
        """Retorna las familias a las que pertenece un dispositivo"""

        rels = FamilyDevice.query.filter_by(id_device=device.id).order_by(desc(FamilyDevice.id_family)).all()
        return [rel.family for rel in rels]
