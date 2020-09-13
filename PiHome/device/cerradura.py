# -*- code: utf-8 -*-
"""
Fichero que define la clase Cerradura
"""
import re
import time

from digi.xbee.packets.common import TransmitStatusPacket

from PiHome import xbee
from PiHome.device.model import Device, Action


class Cerradura:
    """controla el comportamiento de una SmartLock"""

    # Expresion regular que recupera el estado de la puerta d ela información enviada por la cerradura
    state_regex = "Cerradura\[(\D*)\]"

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, value):
        self._estado = value

    def __init__(self):
        self.estado = "Abierto"

    def do_action(self, id_device: int,
                  action: int):

        response_dict = {}
        result: TransmitStatusPacket

        device = Device.get_active_device_by_id(id_device)
        action = Action.get_executable_action(action, device)
        cmd = "CMD:" + action.cmd
        dest = device.id_external

        try:
            result = xbee.mandar_mensage(dest, cmd)
            if action.response_needed:
                self.estado = self.request_lock_state(device)
            response_dict['code'] = result.transmit_status.code
            response_dict['description'] = result.transmit_status.description
            response_dict['status'] = "Estado de la puerta:\t{}".format(self.estado)
        except Exception as error:
            response_dict['code'] = -1
            response_dict['description'] = [str(e) for e in error.args]

        return response_dict

    def request_lock_state(self, device):
        # Establecemos el tiempo máximo de espera para la respuesta
        timeout = time.time() + 10  # Establecemos 5s de límite
        cmd = "CMD:" + Action.get_executable_action(2, device).cmd
        addr = device.id_external
        xbee.mandar_mensage(addr, cmd)
        estado = None
        while time.time() < timeout and not estado:
            estado = xbee.stack_input.get_last_stack(device=device)
        print("TIMEOUT")
        print(format(time.time() - timeout))
        if estado:
            self.estado = re.search(Cerradura.state_regex, estado)[1]
        return self.estado
