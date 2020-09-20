#!venv/bin/python3
# -*- code: utf-8 -*-
"""
    Módulo que define el comportamiento estandar de un dispositivo
"""
from flask_mail import Message

from PiHome import mail
from PiHome.device.model import Device, Action
from PiHome.user.model import User
from PiHome.utils.stack_switcher import StackSwitcher
from PiHome.utils.xbee import XBee

# Nombres de los comandos procesados
INIT = "INIT"
SHOUTING_DOWN = "SHOUTING_DOWN"
PING = 'PING'


class DeviceInstantiationException(Exception):
    def __init__(self, msg, **kwargs):
        super(DeviceInstantiationException, self).__init__(msg, kwargs)
        self.message = "No se puede dejar de informar el parámetro '{}', para instanciar la clase {}.".format(msg,
                                                                                                              "DeviceBase")


class DeviceConnectedException(Exception):

    def __init__(self, **kwargs) -> None:
        """
        @param id_device
        """
        super(DeviceConnectedException, self).__init__(kwargs)
        self.message = "El dispositivo {}, ha recibido la orden de activarse, y ya lo estaba.\nDebería revisar el estado del dispositivo".format(
            kwargs.get('id_device'))

    def __format__(self, format_spec: str) -> str:
        return self.message


class DeviceDisconnectedException(Exception):
    """
            @param id_device
            """

    def __init__(self, **kwargs) -> None:
        super(DeviceDisconnectedException, self).__init__(kwargs)
        self.message = "El dispositivo {}, ha recibido la orden para desactivarse, y ya lo estaba.\nDebería revisar el estado del dispositivo".format(
            kwargs.get('id_device'))


class DeviceBase:
    """Clase que representa el comportamiento básico de un dispositivo"""

    @property
    def thread(self):
        return self.__thread

    @thread.setter
    def thread(self, value):
        self.__thread = value

    @property
    def xbee(self):
        return self.__xbee

    @xbee.setter
    def xbee(self, value):
        self.__xbee = value

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, value):
        self._estado = value

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, value):
        self._logger = value

    def __init__(self, app, **kwargs) -> None:
        super().__init__()
        self.__thread = None
        self.estado = kwargs.get("estado") if kwargs.get("estado") else False
        modelo = kwargs.get("modelo")
        if modelo and isinstance(modelo, Device):
            self.modelo = modelo
        else:
            raise DeviceInstantiationException("mac")
        self.stack = StackSwitcher.get_instance(app)
        self.__xbee = XBee.get_instance(app)
        self.app = app
        self.logger = app.logger
        self.mail = mail.init_app(app)

    def __str__(self) -> str:
        return super().__str__()

    def get_action(self, action_id: int) -> Action:
        """Busca la acción entre las registradas para el dispositivo"""
        response = Action.get_executable_action(device=self.modelo, action=action_id)
        return response

    def do_init(self, actions):
        """El método comprueba que exista en el sistema, un dispositivo con la mac indicada y que tenga las acciones recibidas
        Si el dispositivo está inhabilitado, lo habilita"""
        self.logger.info(str(actions))

        #     Comprobamos las acciones que tiene el dispositivo asociadas
        ## Recuperamos las acciones del dispositivo
        acts = Action.get_executable_actions(device=self.modelo)
        for act in acts:
            if act.cmd not in actions:
                self.logger.warn(
                    "No se ha podido comprobar que el dispositivo {}, pueda realizar la acción de {}".format(
                        self.modelo.id_external, act.cmd))

        #     Comprobamos el estado del dispositivo, si está deshabilitado, lo habilitamos
        if self.modelo.enabled:
            raise DeviceConnectedException(id_device=self.modelo.id_external)
        else:
            self.modelo = Device.enable_device(device=self.modelo)

    def do_shout_down(self):
        #     Comprobamos el estado del dispositivo, si está deshabilitado, lo habilitamos
        if self.modelo.enabled:
            self.modelo = Device.disable_device(device=self.modelo)
        else:
            raise DeviceDisconnectedException(id_device=self.modelo.id_external)

    def def_listen(self, **kwargs):
        for key, command in kwargs.items():
            if key == "inc_order":
                for order, data in command.items():
                    try:
                        if order == INIT:
                            self.do_init(actions=data)
                        if order == SHOUTING_DOWN:
                            self.do_shout_down()
                    except Exception as error:
                        sbj = "Se ha encontrado un error al procesar el comando {} del dispositivo:\t{}".format(order,
                                                                                                                self.modelo.id_external)
                        self.send_email(recipients=User.get_mails_of_groups([2, 3]), subject=sbj, body=format(error))

    def send_email(self, **kwargs):
        """
        @param subject
        @param recipients
        @param body
        """
        subject = kwargs.get('subject')
        sender = self.mail.username
        recipients = kwargs.get('recipients')
        body = kwargs.get('body')

        msg = Message(subject=subject,
                      sender=sender,
                      recipients=recipients,
                      body=body)
        with self.app.app_context():
            try:
                self.mail.send(msg)
            except Exception as error:
                self.logger.warn(format(error))
