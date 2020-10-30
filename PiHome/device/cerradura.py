# -*- code: utf-8 -*-
"""
Fichero que define la clase Cerradura
"""
import re
import time
from time import sleep

from datetime import datetime
from threading import Thread

from PiHome.card.model import Card
from PiHome.device import DeviceBase, PING
from PiHome.transit.model import TransitLog

ABIERTO = "ABIERTO"

CERRADO = "CERRADO"

ATTRIBUTE_USER = "'NoneType' object has no attribute 'user'"

# Nombres de los comandos procesados
TOC_TOC = "TOC_TOC"
READ_TAG = "READ_TAG"

CMD = "CMD:"
# Output commands
APAGAR = "APAGAR"
ABRIR = "ABRIR"
CERRAR = "CERRAR"
ECHO = "ECHO"

# Expresion regular que recupera el estado de la puerta de la información enviada por la cerradura
state_regex = "Cerradura\[(\D*)\]"


class Cerradura(DeviceBase):
    """controla el comportamiento de una SmartLock"""

    @property
    def pause(self):
        return self.__pause

    @pause.setter
    def pause(self, value):
        self.__pause = value

    def __init__(self, app, **kwargs):
        super(Cerradura, self).__init__(app, **kwargs)
        self.thread = Thread(target=self._listen, name=self.__class__.__name__)
        # Este flag, determinará si el ciclo normal del hilo, tiene validez o no
        self.pause = False

    def do_action(self, action: int):

        response_dict = {}

        action = self.get_action(action_id=action)
        cmd = "CMD:" + action.cmd
        dest = self.modelo.id_external

        try:
            result = self.xbee.mandar_mensage(dest, cmd)
            if action.response_needed:
                if action.cmd == READ_TAG:
                    found = self.catch_id_tag()
                    response_dict['status'] = "Id de la tarjeta leida:\t{}".format(found)
                if action.cmd == ECHO:
                    self.request_lock_state()
                    response_dict['status'] = "Estado de la puerta:\t{}".format(self.estado)
            if result and result.transmit_status:
                response_dict['code'] = result.transmit_status.code
                response_dict['description'] = result.transmit_status.description

        except Exception as error:
            response_dict['code'] = -1
            response_dict['description'] = [str(e) for e in error.args]

        return response_dict

    def request_lock_state(self):
        # Establecemos el tiempo máximo de espera para la respuesta
        timeout = time.time() + 10  # Establecemos 10s de límite
        cmd = "CMD:" + self.get_action(2).cmd
        addr = self.modelo.id_external
        self.xbee.mandar_mensage(addr, cmd)
        estado = None
        # Anulamos las lecturas del hilo
        self.pause = True
        while time.time() < timeout and not estado:
            estado = self.stack.get_last_stack(device=self.modelo, cmd=PING)
        # Devolvemos la lectura al hilo
        self.pause = False
        if (time.time() - timeout) > 0 and not estado:
            print("TIMEOUT")
            raise RuntimeWarning("Se ha agotado el tiempo de espera, sin haber recibido respuesta desde el dispositivo")
        if estado:
            estado = estado.get(PING)
            self.estado = re.search(state_regex, estado).group(1)

    def catch_id_tag(self):
        # Establecemos el tiempo máximo de espera para la respuesta
        timeout = time.time() + 10  # Establecemos 10s de límite

        estado = None
        # Anulamos las lecturas del hilo
        self.pause = True
        while time.time() < timeout and not estado:
            estado = self.stack.get_last_stack(device=self.modelo, cmd=READ_TAG)
        # Devolvemos la lectura al hilo
        self.pause = False
        if (time.time() - timeout) > 0 and not estado:
            print("TIMEOUT")
            raise RuntimeWarning("Se ha agotado el tiempo de espera, sin haber recibido respuesta desde el dispositivo")
        if estado:
            return estado.get(READ_TAG)

    def _listen(self, **kwargs):
        while True:
            try:
                if not self.pause:
                    # Se espera recibir un dict con {orden:valor}
                    inc_order = self.stack.get_last_stack(device=self.modelo)
                    if inc_order:
                        print(inc_order)
                        found = None
                        for order, value in inc_order.items():
                            if order == READ_TAG:
                                found = True
                                break
                            if order == TOC_TOC:
                                self.toc_toc(id_tag=value)
                                found = True
                                break
                            if order == PING:
                                self.estado = re.search(state_regex, value).group(1)
                                found = True
                                break
                        if not found:
                            self.def_listen(inc_order=inc_order)
            except Exception as error:
                self.logger.warn(str(error))

    def toc_toc(self, id_tag):
        try:
            # Recuperamos el usuario asignado al la targeta
            user = Card.get_user_from_tag(id_tag=id_tag)
            # Si el usuario está registrado
            if user:
                msg = None
                # if self.estado == ABIERTO:
                #     # Cerramos la puerta
                #     msg = CMD + CERRAR
                # # if self.estado == CERRADO:
                # else:
                #     # Abrimos la puerta
                #     msg = CMD + ABRIR
                msg = CMD + ABRIR

                # Mandamos mensaje al watchdog
                try:
                    self.xbee.mandar_mensage(self.modelo.id_external, msg=msg)
                    sleep(15)
                    msg = CMD + CERRAR
                    self.xbee.mandar_mensage(self.modelo.id_external, msg=msg)
                except Exception as e:
                    self.logger.info("Encontrado un error al mandar el mensage{} \n {}".format(msg, e))
                # if self.estado == ABIERTO:
                #     self.estado = CERRADO
                # else:
                #     self.estado = ABIERTO
                # Registramos el hecho
                try:
                    Cerradura.registrar_transito(user.id)
                except Exception as e:
                    self.logger.info("Encontrado un error al guardar el tránsito {}".format(e))
                else:
                    self.logger.info("Registrado el tránsito del usuario {}".format(user.name))
        except Exception as error:
            if str(error) == ATTRIBUTE_USER:
                self.logger.warn("No hay ningún usuario registrado con la siguiente targeta:\t{}".format(id_tag))
            else:
                raise error

    @classmethod
    def registrar_transito(cls, user_id):
        user_log = TransitLog.get_last_move_by_id_user(user_id)
        last_action = 0
        if user_log:
            last_action = (user_log.action + 1) % 2

        new_user_log = TransitLog(user_id=user_id,
                                  action=last_action,
                                  ocurred=datetime.now())
        new_user_log.save()
