# -*- code: utf-8 -*-
"""
Fichero que maneja el comportamiento de las tarjetas
"""
from time import sleep

from flask import Blueprint, session, render_template, request, jsonify, redirect, url_for, flash

from PiHome import device_list
from PiHome.device.cerradura import ABRIR, CERRAR
from PiHome.device.form import AddDeviceForm
from PiHome.device.model import Device, Action, Family, FamilyDevice
from PiHome.utils.base import Home, ShowData

device_ctr = Blueprint('device', __name__, url_prefix='/device')

home = Home()


@device_ctr.route('/list', methods=['GET'])
def get_device():
    """
    Recupera la lista de dispositivos disponibles y sus capacidades
    @return:
    """

    if 'name' in session and session['name'] != '':
        if session['category'] in (3, 2):
            base = home.get_base_params(_title="Dispositivos")
            body = ShowData(_header="Dispositivos disponibles")
            body.data = get_devices_list()
            return render_template('devices.html',
                                   base=base,
                                   body=body)
    else:
        return render_template('error.html'), 404


def get_devices_list():
    """Retorna un mapa con los dispositivos activos y sus acciones ejecutables"""
    # Diccionario son los dispositivos registrados
    devices_dic = {}

    devices_list = Device.get_active_devices()
    for device in devices_list:
        actions_list = Action.get_executable_actions(device)
        devices_dic[device] = actions_list

    return devices_dic


@device_ctr.route('/do_action', methods=['GET'])
def do_action():
    """
    Ejecuta las acción recibida para el dispositivo indicado

    ---

    @param dev Id del dispositivo que realizará la acción
    @param act Id de la acción que deberá reañlizar el dispositivo
    @return:
    """
    response_dict = {}
    response = None
    _status = 200

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
        response = render_template('error.html'), 404

    return response


@device_ctr.route('/unlock_door', methods=['GET'])
def unlock_door():
    """Abrirá la cerradura durante 15seg y la volverá a cerrar
    Tras la acción, redirijira a la página de home y mostrará el resultado de la acción
    """

    response = render_template('error.html'), 404

    if 'name' in session and session['name'] != '':
        if session['category'] in (3, 2):
            devs = FamilyDevice.get_devices_by_family(['Cerradura'])
            dev = None
            if devs:
                dev = devs[0].id

            act_abrir = Action.get_by_cmd(ABRIR).id
            act_cerrar = Action.get_by_cmd(CERRAR).id
            try:
                device_list.get(dev).do_action(act_abrir)
                sleep(15)
                device_list.get(dev).do_action(act_cerrar)
                flash("Puerta '{}', abierta y cerrada tras 15 seg".format(devs[0].name))
            except Exception as error:
                flash('No se ha podido realizar la petición', category='error')
                for e in error.args:
                    flash(format(e), category='error')

            response = redirect(url_for('home.index'))

    else:
        response = render_template('error.html'), 404

    return response


def save(name: str, iface: str, mac: str, remote: str = None, fam: list = None):
    """Guarda un nuevo dispositivo

    :rtype: Device

    :param name: Nombre del dispositivo
    :param iface: Interface del dispositivo
    :param mac: Dirección del dispositivo
    :param remote: Punto de enlace del dispositivo
    :param fam: Familias del dispositivo. Default [1]
    """
    device = None

    if fam is None:
        fam = [1]
    elif 1 not in fam:
        fam.append(1)

    families = []
    for f in fam:
        families.append(Family.get_by_id(f))

    device = Device(name=name, id_external=mac, id_remote=remote, interface=iface)
    device.save()

    for f in families:
        if f:
            FamilyDevice(device=device, family=f).save()

    return device


@device_ctr.route('/new_device', methods=['GET', 'POST'])
def new_device():
    """
    Muestra la vista para dar de alta un nuevo dispositivo (get) y lo guarda en la base de datos (post)

    ---

    :return:
    """

    title = "Alta de dispositivos"
    _base = home.get_base_params(_title=title, _header=title)

    response = render_template('error.html'), 404
    flash_msg = None

    if 'name' in session and session['name'] != '':
        if session['category'] == 3:
            form = AddDeviceForm(request.form)

            if request.method == 'POST' and form.validate() and form.validate_on_submit():
                name = form.device_name.data
                iface = form.device_iface.data
                mac = form.device_id.data
                remote = form.device_remote.data
                fam = form.device_fam.data

                try:
                    #     Guardamos el nuevo dispositivo
                    dev = save(name, iface, mac, remote, fam)
                    if dev:
                        device_list[dev.id] = dev
                        flash_msg = "Se ha añadido el  nuevo dispositivo '{}', satisfactoriamente".format(dev.name)
                except Exception as e:
                    if e.orig and e.orig.args[0] == 1062:
                        flash_msg = "Se ha detectado un problema al añadir el dispositivo:\n\t{}".format(e.orig.args[1])
                    else:
                        flash_msg = format(e)
                    flash(flash_msg, category='error')
                    response = render_template('newDevice.html',
                                               base=_base,
                                               form=form)
                else:
                    flash(flash_msg)
                    flash("Recuerde que el dispositivo se inicializa deshabilitado")

                    response = redirect(url_for('device.get_device'))

            else:
                # if request.method == 'GET':
                response = render_template('newDevice.html',
                                           base=_base,
                                           form=form)

    return response
