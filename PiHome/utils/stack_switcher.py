#!venv/bin/python3
"""En este fichero se confeccionarán la acciones que realizará el sistema cuando reciva una orden externa"""
import re

from flask import Flask

IS_NOT_SUBSCRIPTABLE = "'NoneType' object is not subscriptable"


class StackSwitcherException(Exception):
    def __init__(self, msg: str = None, *args):
        super().__init__(args)
        super().message = "Error encontrado en la clase {}.\n\t{}".format("StackSwitcher", msg)


class StackInstanceException(Exception):
    def __init__(self, msg: str = None, *args):
        super().__init__(args)
        super().message = "No se puede crear más de una instancia de la clase StackSwitcher.\n" + msg


class StackSwitcher:
    # Expresiones regulares que nos permitirán procesar las ordenes entrantes
    cmd_extractor_regex = "CMD:(.*)\?(.*)"
    param_extractor_regex = "\?(.*)"

    # Nombres de los campos a extraer de la configuración
    __SYSTEM_INTERFACES = 'SYSTEM_INTERFACES'
    __INCOMING_ORDERS = '_INCOMING_ORDERS'

    @property
    def incoming_orders(self) -> dict:
        return self.__incoming_orders

    @incoming_orders.setter
    def incoming_orders(self, value):
        for key, data in value.items():
            self.__incoming_orders[key] = data

    @property
    def stack(self):
        return self.__stack

    @stack.setter
    def stack(self, value):
        self.__stack = value

    @property
    def logger(self):
        return self.__logger

    @logger.setter
    def logger(self, value):
        self.__logger = value

    __instance = None

    @staticmethod
    def get_instance(app: Flask = None):
        if StackSwitcher.__instance is None:
            if not app:
                raise StackInstanceException()
            StackSwitcher.__instance = StackSwitcher(app=app)
        return StackSwitcher.__instance

    def __init__(self, **kwargs):

        if not StackSwitcher.__instance:
            for key, value in kwargs.items():
                if key == 'app':
                    # Extraemos las ordenes que se esperan recibir de cada interface
                    incom_orders = {}
                    for interface in value.config[StackSwitcher.__SYSTEM_INTERFACES]:
                        incom_orders[interface] = value.config[interface + StackSwitcher.__INCOMING_ORDERS]
                    self.__incoming_orders = incom_orders

                    # Recuperamos el logger
                    self.__logger = value.logger

            # Iniciamos la cola de ordenes recibidas
            self.__stack = {}

    def get_last_stack(self, **kwargs):
        """Devuelve la ultima orden recibida el dispositivo con la mac indicada.
        None si el el stack está vacio
        @param device (Type: Device): dispositivo del que se extraerá su mac
        @param device_mac: mac del dispositivo
        """
        device_mac = kwargs.get('device_mac')
        if not device_mac:
            try:
                device_mac = kwargs.get('device').id_external
            except Exception as e:
                raise StackSwitcherException(format(e))

        if device_mac:
            order = self.stack.get(device_mac)
            if not order:
                return None
            cmd = re.search(StackSwitcher.cmd_extractor_regex, order)[1]
            data = re.search(StackSwitcher.cmd_extractor_regex, order)[2]

            return {cmd: data}
        else:
            raise StackSwitcherException("No se ha indicado la diracción mac del dispositivo")

    def append_order(self, mac, cmd, iface):
        """
        Este método gestionará el acceso de escritura a la pila de mensajes recibidos
        
        @param mac: dirección mac desde la que se ha recibido el mensaje
        @param cmd: mensaje o comando recibido
        @param iface: interface desde la que se ha recibido el mensaje"""
        try:
            order = re.search(StackSwitcher.cmd_extractor_regex, cmd)[1]
            data = re.search(StackSwitcher.cmd_extractor_regex, cmd)[2]
            if order in self.incoming_orders.get(iface):
                msg = "Encontrada orden desde el dispositivo {} por la inteface {}:\t{}".format(mac, iface, order)
                if data:
                    msg += "\n\tParámetro:\t{}".format(data)
                self.logger.info(msg)
            else:
                msg = "Orden no encontrada desde el dispositivo {} por la inteface {}:\t{}".format(mac, iface, order)
                if data:
                    msg += "\n\tParámetro:\t{}".format(data)
                self.logger.warn(msg)
        except Exception as error:
            try:
                if str(error) == IS_NOT_SUBSCRIPTABLE:
                    device = self.stack.get(mac)
                    if not device:
                        self.stack[mac] = [cmd]
                    else:
                        self.stack.get(mac).append(cmd)
                else:
                    raise error
            except:
                return False
        return True
