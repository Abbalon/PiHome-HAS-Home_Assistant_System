#!venv/bin/python3
# -*- code: utf-8 -*-
"""
    Módulo que define el comportamiento estandar de un dispositivo
"""

from PiHome.device.model import Device, Action
from PiHome.utils.stack_switcher import StackSwitcher
from PiHome.utils.xbee import XBee

# Nombres de los comandos procesados
INIT = "INIT"
SHOUTING_DOWN = "SHOUTING_DOWN"
PING = 'PING'


class DeviceInstantiationException(Exception):
    def __init__(self, msg, *args):
        super().__init__(args)
        super().message = "No se puede dejar de informar el parámetro '{}', para instanciar la clase {}.".format(msg,
                                                                                                                 "DeviceBase")


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
        self.logger = app.logger

    def __str__(self) -> str:
        return super().__str__()

    def get_action(self, action_id: int) -> Action:
        """Busca la acción entre las registradas para el dispositivo"""
        response = Action.get_executable_action(device=self.modelo, action=action_id)
        return response

    @classmethod
    def do_init(cls, actions):
        """El método comprueba que exista en el sistema, un dispositivo con la mac indicada y que tenga las acciones recibidas
        Si el dispositivo está inhabilitado, lo habilita"""

        #     Recuperamos el dispositivo con la mac indicada
        dev = Device.get_device_by_mac("device_mac")
        #     Comprobamos las acciones que tiene el dispositivo asociadas

        #     Comprobamos el estado del dispositivo, si está deshabilitado, lo habilitamos

    def do_shout_down(self):
        print(self.modelo.id_external)
        return None

    def __listen(self, **kwargs):
        for order, data in kwargs.items():
            if order == INIT:
                self.do_init(actions=data)
            if order == SHOUTING_DOWN:
                self.do_shout_down()
