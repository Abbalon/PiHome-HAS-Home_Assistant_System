# -*- code: utf-8 -*-
"""
Fichero que maneja el comportamiento de las tarjetas
"""
from flask import Blueprint, session, render_template, request, jsonify

from PiHome import device_list
from PiHome.device.model import Device, Action
from PiHome.utils.base import Home, ShowData

device_ctr = Blueprint('device', __name__, url_prefix='/device')

__home = Home()
__base = None
__title = None
__header = None
__body = None

__html = 'devices.html'


@device_ctr.route('/list', methods=['GET'])
def get_device():
    """
    Recupera la lista de dispositivos disponibles y sus capacidades
    @return:
    """

    if 'name' in session and session['name'] != '':
        if session['category'] in (3, 2):
            __base = __home.get_base_params("Dispositivos")
            __body = ShowData(_header="Dispositivos disponibles")
            __body.data = get_devices_list()
            return render_template(__html,
                                   base=__base,
                                   body=__body)
    else:
        return render_template('error.html')


def get_devices_list():
    """Retorna un mapa con los dispositivos activos y sus acciones ejecutables"""
    # Diccionario son los dispositivos registrados
    devices_dic = {}
    devices_list = None
    actions_list = None

    devices_list = Device.get_active_devices()
    for device in devices_list:
        actions_list = Action.get_executable_actions(device)
        devices_dic[device] = actions_list

    return devices_dic


@device_ctr.route('/do_action', methods=['GET'])
def do_action():
    """
    Ejecuta las acción recibida para el dispositivo indicado
    @param dev Id del dispositivo que realizará la acción
    @param act Id de la acción que deberá reañlizar el dispositivo
    @return:
    """
    response_dict = {}
    response = None
    _status: int = 200

    if 'name' in session and session['name'] != '':
        if session['category'] in (3, 2):
            dev = request.args.get('dev', 0, type=int)
            act = request.args.get('act', 0, type=int)
            result = None  # TransmitStatusPacket

            try:
                result = device_list.get(dev).do_action(act)
                if result:
                    response_dict = result
            except Exception as error:
                response_dict = {'error': 'No se ha podido realizar la petición',
                                 'description': [str(e) for e in error.args]}
                _status = 500

            response = jsonify(response_dict)
            response.status_code = _status

    else:
        response = render_template('error.html')

    return response
