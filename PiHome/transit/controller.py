#!/usr/bin/env python3
# -*- code: utf-8 -*-
"""
Fichero que maneja la extración de datos del tránsito de usuarios
"""
from flask import Blueprint, session, render_template, request
# Define the blueprint: 'transit', set its url prefix: app.url/auth
from flask_wtf import FlaskForm
from sqlalchemy import func, and_

from PiHome.transit.form import TransitFilter
from PiHome.transit.model import TransitLog
from PiHome.user import controller as UserDAO
from PiHome.utils.base import Home, ShowData

transit_ctr = Blueprint('transit', __name__, url_prefix='/transit')

home = Home()


def ejecutar_busqueda(filter_form: FlaskForm):
    _user = filter_form.user_name.data
    _f_ini = filter_form.f_inicio.raw_data
    _f_fin = filter_form.f_fin.raw_data

    body = None

    #     111
    if _user and _f_ini and _f_fin:
        # Aplicamos los tres filtros
        body = TransitLog.query.filter(
            and_(TransitLog.user_id == _user,
                 TransitLog.ocurred.between(func.date(_f_ini), func.date(_f_fin)))).all()
    #     110
    if _user and _f_ini and not _f_fin:
        # Buscamos fechas mayores a la fecha de inicio
        body = TransitLog.query.filter(
            and_(TransitLog.user_id == _user,
                 TransitLog.ocurred >= func.date(_f_ini))).all()
    #     101
    if _user and not _f_ini and _f_fin:
        # Buscamos fechas menores a la fecha fin
        body = TransitLog.query.filter(
            and_(TransitLog.user_id == _user,
                 TransitLog.ocurred <= func.date(_f_fin))).all()
    #     100
    if _user and not _f_ini and not _f_fin:
        # Buscamos fechas menores a la fecha fin
        body = TransitLog.query.filter(TransitLog.user_id == _user).all()
    #     011
    if not _user and _f_ini and _f_fin:
        # Aplicamos los tres filtros
        body = TransitLog.query.filter(TransitLog.ocurred.between(func.date(_f_ini), func.date(_f_fin))).all()
    #     010
    if not _user and _f_ini and not _f_fin:
        # Buscamos fechas mayores a la fecha de inicio
        body = TransitLog.query.filter(TransitLog.ocurred >= func.date(_f_ini)).all()
    #     001
    if not _user and not _f_ini and _f_fin:
        # Buscamos fechas menores a la fecha fin
        body = TransitLog.query.filter(TransitLog.ocurred <= func.date(_f_fin)).all()
    #     000
    if not _user and not _f_ini and not _f_fin:
        # Recuperamos los movimientos de un usuario
        body = TransitLog.query.all()

    if not body:
        body = [TransitLog()]

    return body


@transit_ctr.route('/get', methods=['GET', 'POST'])
def get(**filtro):
    """
    REST que nos devuelve los datos de transito
    :type filtro:
    ['user']        -> Usuario del que nos interesa saber sus tránsitos
    ['fecha_ini']   -> Desde que fecha queremos mostrar
    ['fecha_fin']   -> Hasta que fecha queremos mostrar
    """
    _base = home.get_base_params(_title="Listado del tránsito registrado")
    title = "Accesos registrados"
    header = None
    body = None
    filter_form = None

    if 'name' in session and session['name'] != '':
        header = ["Usuario", "Acción", "Fecha"]
        filter_form = TransitFilter(request.form)
        filter_form.user_name.choices = UserDAO.get_user_lite_list()
        if session['category'] in (3, 2):
            if not request.method == 'POST':
                _base = home.get_base_params(_title="Mostrando prueba de lista", _dynamic=0)
            else:
                body = ejecutar_busqueda(filter_form)

        try:
            transit = ShowData(title, header, body)
        except:
            transit = None

        return render_template('showTransit.html',
                               base=_base,
                               results=transit,
                               table='Tránsito registrado',
                               form=filter_form)

    else:
        return render_template('error.html')
