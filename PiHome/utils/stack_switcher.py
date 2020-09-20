#!venv/bin/python3
"""En este fichero se confeccionarán la acciones que realizará el sistema cuando reciva una orden externa"""
import re
import threading

UNKNOWN = "UNKNOWN"

IS_NOT_SUBSCRIPTABLE = "'NoneType' object is not subscriptable"


class StackSwitcherException(Exception):
    def __init__(self, msg: str = None, *args):
        super().__init__(args)
        super().message = "Error encontrado en la clase {}.\n\t{}".format("StackSwitcher", msg)


class StackInstanceException(Exception):
    def __init__(self, msg: str = None, *args):
        super().__init__(args)
        self.args = ("No se puede crear más de una instancia de la clase StackSwitcher.\n{}".format(msg),)


class StackSwitcher:
    # Expresiones regulares que nos permitirán procesar las ordenes entrantes
    # cmd_extractor_regex = "CMD:(.*)\?(.*)"
    cmd_extractor_regex = "CMD:(\w*)(\?(.*))?"
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
    def logger(self):
        return self.__logger

    @logger.setter
    def logger(self, value):
        self.__logger = value

    __instance = None

    @classmethod
    def get_instance(self, app):
        if StackSwitcher.__instance is None:
            if not app:
                raise StackInstanceException("Falta el atributo 'app' con la configuración.")
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
                    self.logger = value.logger

                    # Iniciamos la cola de ordenes recibidas
                    self.__stack = dict()
                    self.__locked = threading.Lock()
        else:
            self.logger.warn("El stack ya está inicializado")

    def get_last_stack(self, **kwargs):
        """Devuelve la ultima orden recibida el dispositivo con la mac indicada.
        None si el el stack está vacio
        @param device (Type: Device): dispositivo del que se extraerá su mac
        @param device_mac: mac del dispositivo
        @param cmd: el comando específico que se esta buscando
        @raise Exception: Si hay algún error al procesar la cola de mensajes
        @return {cmd:data}:
            cmd -> el último comando almacenado (UNKNOWN: si no está registrado)
            data -> el valor almacenado para ese comando
        """

        # Recuperamos la mac del dispositivo, si bien está indicada directamente o si no, desde el dispositivo pasado
        # por parámetro
        device_mac = kwargs.get('device_mac')
        if not device_mac:
            try:
                device_mac = kwargs.get('device').id_external
            except Exception as e:
                raise StackSwitcherException(format(e))

        # Solo si tenemos la mac del dispositivo a buscar
        if device_mac:
            # Extraemos el dato del comando esperado
            cmd = kwargs.get('cmd')

            # Si se ha indicado un comando específico a buscar
            if cmd:
                # Devolvemos el contenido del stack
                return self.__read_stack(device_mac, cmd=cmd)
            # Si no se ha indicado ningún comando en concreto
            else:
                return self.__read_stack(device_mac)
        else:
            raise StackSwitcherException("No se ha indicado la diracción mac del dispositivo")

    def append_order(self, mac, cmd, iface):
        """
        Este método gestionará el acceso de escritura a la pila de mensajes recibidos
        
        @param mac: dirección mac desde la que se ha recibido el mensaje
        @param cmd: mensaje o comando recibido
        @param iface: interface desde la que se ha recibido el mensaje"""
        try:
            regex_found = re.search(StackSwitcher.cmd_extractor_regex, cmd)
            if regex_found:
                order = regex_found.group(1)
                data = regex_found.group(3)
                if order in self.incoming_orders.get(iface):
                    msg = "Recibida orden desde el dispositivo {} por la inteface {}:\t{}".format(mac, iface, order)
                else:
                    msg = "Orden no encontrada desde el dispositivo {} por la inteface {}:\t{}".format(mac, iface, order)
                if data:
                    msg += "\n\tParámetro:\t{}".format(data)
                self.logger.warn(msg)
                self.__write_stack(cmd, mac)
        except Exception as error:
            try:
                if str(error) == IS_NOT_SUBSCRIPTABLE:
                    self.__write_stack(cmd, mac)
                else:
                    raise error
            except:
                return False
        return True

    def __write_stack(self, cmd, mac):
        """Método sincronizado para escribir en el stack
        @param mac: Dirección mac del dispositivo del que se quiere recuperar el primer comando almacenado
        @param cmd: Comando específico del dispositivo indicado, del que se quiere obterner su contenido
        @raise StackSwitcherException: Si ocurre algún problema durante la escritura en el stack"""

        with self.__locked:
            excep = None
            try:
                device = self.__stack.get(mac)
                if not device:
                    self.__stack[mac] = [cmd]
                else:
                    self.__stack.get(mac).append(cmd)
            except Exception as e:
                excep = e
            else:
                if excep:
                    raise StackSwitcherException("Error mientras se escribia en el stack:\n\t{}".format(excep))

    def __read_stack(self, mac, **kwargs):
        """Método sincronizado para leer del stack
        @param mac: Dirección mac del dispositivo del que se quiere recuperar el primer comando almacenado
        @param cmd: Comando específico del dispositivo indicado, del que se quiere obterner su contenido
        @return {cmd : param}: Devolverá un diccionario con el comando recuperado y su valor su lo tuviera o None si la pila esta vacia
        @raise StackSwitcherException: Si ocurre algún problema durante la lectura en el stack"""

        with self.__locked:
            excep = None
            command = UNKNOWN
            data = None

            try:
                # Extraemos el dato del comando esperado
                cmd = kwargs.get('cmd')

                # Extraemos su listado de mensajes sin tratar
                device_stack = self.__stack.get(mac)
                # Si no hemos recuperado nada, retornamos None
                if not device_stack:
                    return None

                if cmd:
                    found = False
                    # Por cada elemento de la lista de comandos
                    for i_cmd in range(len(device_stack)):
                        # Extaemos cada orden y la parseamos
                        order = device_stack[i_cmd]
                        f_regex = re.search(StackSwitcher.cmd_extractor_regex, order)
                        if f_regex:
                            command = f_regex.group(1)
                            data = f_regex.group(3)
                            # Si el comando es el que se quería
                            if command == cmd:
                                # Lo borramos de la lista
                                del self.__stack.get(mac)[i_cmd]
                                found = True
                                break
                    # Si no se ha encontrado el comando esperado
                    if not found:
                        return None
                else:
                    # Cogemos el primer cmonado insertado
                    order = self.__stack.get(mac).pop(0)
                    f_regex = re.search(StackSwitcher.cmd_extractor_regex, order)
                    if f_regex:
                        command = f_regex.group(1)
                        data = f_regex.group(3)
                    else:
                        command = UNKNOWN
                        data = order
            except Exception as e:
                excep = e
            else:
                if excep:
                    raise StackSwitcherException("Error mientras se escribía en el stack:\n\t{}".format(excep))

            return {command: data}
