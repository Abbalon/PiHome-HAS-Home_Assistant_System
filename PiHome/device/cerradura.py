# -*- code: utf-8 -*-
"""
Fichero que define la clase Cerradura
"""
import re

from digi.xbee.packets.common import TransmitStatusPacket

from PiHome import xbee
from PiHome.device.model import Device, Action


class Cerradura:
    """controla el comportamiento de una SmartLock"""

    state_regex = "Cerradura\[(\D*)\]"

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, value):
        self._estado = value

    def __init__(self):
        self.estado = False

    def do_action(self, id_device: int,
                  action: int):

        response_dict = {}
        result: TransmitStatusPacket

        device = Device.get_active_device_by_id(id_device)
        cmd = "CMD:" + Action.get_executable_action(action, device).cmd
        dest = device.id_external

        try:
            result = xbee.mandar_mensage(dest, cmd)
            self.estado = self.request_lock_state(device)
            response_dict['code'] = result.transmit_status.code
            response_dict['description'] = result.transmit_status.description
            response_dict['status'] = self.estado
        except Exception as error:
            response_dict['code'] = -1
            response_dict['description'] = [str(e) for e in error.args]

        return response_dict

    def request_lock_state(self, device):
        cmd = "CMD:" + Action.get_executable_action(4, device).cmd
        addr = device.id_external
        xbee.mandar_mensage(addr, cmd)
        # Mientras no se reciba respuesta del dipositivo esperado
        while addr not in xbee.stack_input:
            pass
        while not len(xbee.stack_input.get(addr)) > 0:
            pass

        estado = xbee.stack_input.get(addr).pop()
        return re.search(Cerradura.state_regex, estado)[1]
