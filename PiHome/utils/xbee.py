#!venv/bin/python
"""Paquete encargado de la gestión y representación de un dispositivo ZigBee/Xbee"""
from threading import Thread

import serial.tools.list_ports
from digi.xbee.devices import ZigBeeDevice, RemoteZigBeeDevice
from digi.xbee.exception import XBeeException
from digi.xbee.models.address import XBee64BitAddress, XBee16BitAddress
from digi.xbee.models.message import XBeeMessage
from digi.xbee.models.status import TransmitStatus
from digi.xbee.packets.common import TransmitStatusPacket
from flask import Flask

from PiHome.utils.stack_switcher import StackSwitcher

"""Lista de palabras que podría contener un shield con una antena xbee"""
xbeeAntenaWhiteList = ['FT232R', 'UART']
PING = "CMD:PING"

DEVICE_CLOSED_ERROR_MSG = 'XBee family\'s serial port closed.'
DEVICE_OPENED_ERROR_MSG = 'XBee family already open.'


class XBee(ZigBeeDevice):
    """Clase que representa las antenas xbee que serán la principàl interface de comunicación del dispositivo
    WatchDog
    @see https://xbplib.readthedocs.io/en/stable/index.html"""

    _instance = None

    @classmethod
    # def get_instance(self, stack, app: Flask = None):
    def get_instance(self, app: Flask = None):
        """Metódo que devuelve una instancia de la antena creada"""
        if XBee._instance is None:
            if not app:
                raise XBeeInstanceException("No se han informado los parámetros necesarios.")
            # XBee._instance = XBee(stack, app)
            XBee._instance = XBee(app)
        return XBee._instance

    @staticmethod
    def encontrar_rutas() -> []:
        """Método que retorna una lista de posibles rutas donde se encontrará un dispositivo compatible con una antena
         XBEE conectada mediante un shield USB"""

        ports = serial.tools.list_ports.comports()
        filtered = []
        for port, desc, hwid in sorted(ports):
            for word in desc.split(' '):
                if word in xbeeAntenaWhiteList:
                    filtered.append(port)
                    break
        return filtered

    @property
    def logger(self):
        """

        @return:
        """
        return self._logger

    @logger.setter
    def logger(self, value):
        self._logger = value

    @property
    def remote_zigbee(self) -> RemoteZigBeeDevice:
        """
        @return Retorna el dispositivo remoto al que se encuentra conectado la antena
        @rtype: RemoteZigBeeDevice
        """
        return self.__remote

    @remote_zigbee.setter
    def remote_zigbee(self, mac):
        self.__remote = RemoteZigBeeDevice(self, XBee64BitAddress.from_hex_string(mac))

    @property
    def port(self) -> str:
        return self.__port

    @port.setter
    def port(self, value):
        self.__port = value

    @property
    def baudrate(self) -> str:
        return self.__baudrate

    @baudrate.setter
    def baudrate(self, value):
        self.__baudrate = str(value)

    # Define el tipo de interface que se empleará
    IFACE = 'XBEE'

    # def __init__(self, stack, app: Flask = None):
    def __init__(self, app: Flask = None):
        """Constructor con la cofiguración seteada de la app
        Es necesario llamar a init_app, para iniciar la antena
        @param app: {XBEE_PORT, XBEE_BAUDRATE }"""

        if XBee._instance is None and app is not None:
            self.extract_parameters(app)
            self.logger.info("Creando la antena")
            # self.stack = stack
            self.stack = StackSwitcher.get_instance(app)
            """De la lista de posibles puertos a la que pueda estár conectada la antena
            nos conectamos a la primera y lo notificamos"""
            self.logger.info("Puertos encontrados: " + str(self.port))
            self.logger.info("Frecuencia de trabajo: " + self.baudrate)
            if len(self.port) > 0:
                for port in self.port:
                    super().__init__(port, self.baudrate)
            else:
                self.logger.warning("No se ha informado de ningún puerto disponible para el XBee")
        else:
            raise XBeeInstanceException("Esta clase ya está creada, obtenga una instancia para su uso")

        # Si no se ha creado nunca ningun objeto del tipo XBee y se han informado los parámetros necesarios
        # XBee.__instance = self

    def extract_parameters(self, app):
        try:
            self.logger = app.logger
            port = app.config['XBEE_PORT']
            if not port:
                port = self.encontrar_rutas()
            self.port = port

            baudrate = str(app.config['XBEE_BAUDRATE'])
            if not baudrate:
                baudrate = 9600
            self.baudrate = baudrate
        except Exception as e:
            msg = "ERROR: No se han podido precargar los valores del XB\n " + str(e)
            e.message = msg
            raise e

    def __del__(self):
        self.logger.debug("Eliminando el ZigBee")
        try:
            if self:
                super().del_data_received_callback(self.__tratar_entrada)
        except Exception as e:
            self.logger.error("No se ha cerrado la conexíón de la antena\n\t" + str(e))

    def __str__(self):
        atr = {'Opened': self.is_open(), 'Name': self.get_node_id(), 'Dir': str(self.get_64bit_addr()),
                     'Remote_dir': str(self.remote_zigbee.get_64bit_addr())}

        return format(atr)

    def mandar_mensage(self, dir_64, msg=PING, dir_16=None) -> TransmitStatusPacket:

        """
        Manda el mensaje al destinatario por defecto.
        """
        ack = None
        # Transformamos el mensaje recibido en un string tratable
        msg = str(msg)
        # Recuperamos la dirección del dispositivo remoto en formato de 64 bits
        high = None
        try:
            dir_64 = XBee64BitAddress.from_hex_string(dir_64)
            high = dir_64 or self.remote_zigbee.get_64bit_addr()
        except:
            high = XBee64BitAddress.UNKNOWN_ADDRESS

        # Recuperamos la dirección del dispositivo remoto en 16 bits o la marcamos como desconocida
        low = None
        try:
            low = XBee16BitAddress.from_hex_string(dir_16) or self.remote_zigbee.get_16bit_addr()
        except:
            low = XBee16BitAddress.UNKNOWN_ADDRESS

        try:
            # Intentamos mandar el mensaje
            ## Versión fragmentando el paquete

            ## Versión sin fragmentar el paquete
            ack = super().send_data_64_16(high, low, msg)
            # self.logger.debug(format(ack))
            if ack.transmit_status is not TransmitStatus.SUCCESS:
                self.logger.warning("Algo no fue bien mandando el mensaje:\n{}\nError:\t{}".format(msg, ack))

        except Exception as e:
            self.logger.error("Se ha encontrado un error al mandar el mensaje\n\t" + str(e))
            ack = super().send_data_64_16(high, low, msg)
            # Añadir código para el reintento
        else:
            # TODO Borrar esta traza de control
            self.logger.debug("Mandado mensaje:\t" + msg)
        return ack

    def __tratar_entrada(self, recived_msg: XBeeMessage):
        """
            Tratamos la información que recibamos
        @param recived_msg:
        """
        msg = recived_msg.data.decode("utf8")
        self.logger.debug(msg)
        super().close()

    def escuchar_medio(self) -> str:
        """
        Escucha por si enlace le manda algún mensaje
        @return: El mensaje recibido si hay algo, None eoc
        """
        recived_msg = None
        if self.is_open:
            recived_order = self.read_data()
            if recived_order is not None:
                recived_msg = str(recived_order.data.decode("utf8"))

        return recived_msg

    def esperar_hasta_recibir_orden(self):
        """
            Bucle que no finaliza hasta que se recibe un mensaje
            @return El mensaje recibido, None si la antena está cerrada
        """
        recived_msg = None
        if self.is_open():
            recived_order = None
            while True:
                try:
                    recived_order = self.read_data()
                except XBeeException as ebe:
                    if DEVICE_CLOSED_ERROR_MSG in ebe.args[0] and not self.is_open():
                        self.open()
                        self.logger.warning(ebe.args[0])
                if recived_order is not None:
                    recived_msg = recived_order.data.decode("utf8")
                    msg_origin_addr = str(recived_order.remote_device.get_64bit_addr())
                    self.logger.info("Mensage recibidio de {}:\n{}".format(msg_origin_addr, recived_msg))
                    # TODO Revisar el punto de guardado en el stack
                    if not self.stack.append_order(msg_origin_addr, recived_msg, XBee.IFACE):
                        self.logger.warning("No se ha podido guardar el mensaje")

    def init_app(self, xbee_thread: Thread):
        """Instanciamos una antena XBeee a partir de un dispositivo ZigBeeDevice
                @param app: {XBEE_PORT, XBEE_BAUDRATE [, XBEE_REMOTE_ADDRESS] }"""

        for port in self.port:
            self.logger.info("Probando el puerto: " + port)
            try:
                if XBee._instance:
                    try:
                        if not self.is_open():
                            self.open()
                    except XBeeException as e:
                        msg = "No se ha podido conectar con la antena XBee.\n\t" + str(e)
                        self.logger.error(msg)
                        self.close()
                        raise e
                    else:
                        antena = str(super().get_node_id() + "(" + str(super().get_64bit_addr()) + ")")
                        self.logger.info("Conectada la antena '" + antena + "' al puerto " + port + "\n")
                        xbee_thread.start()
                        break
            except Exception as e:
                self.close()
                self.logger.error("Encontrado un error al inicializar el dispositivo ZigBeeDevice\n" + str(e))
                raise e


class XBeeInstanceException(Exception):
    """Esta exceptción será lanzada si se trata de instanciar varias veces el objeto XBEE"""

    def __init__(self, msg: str = None, *args):
        super().__init__(args)
        super().message = "No se puede crear más de una instancia de la clase XBee.\n" + msg
