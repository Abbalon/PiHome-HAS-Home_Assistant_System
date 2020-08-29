# -*- code: utf-8 -*-
"""
Fichero que maneja el comportamiento de las tarjetas
"""
from flask import Blueprint, session, render_template

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
            __body = ShowData(__header="Dispositivos disponibles")
            __body.data = Action.query.filter(
                Action.is_executable == True).join('device').add_columns(
                Device.name,
                Action.name).all()
            return render_template(__html,
                                   base=__base,
                                   body=__body)
    else:
        return render_template('error.html')
