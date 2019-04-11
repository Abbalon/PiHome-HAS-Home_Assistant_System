#!/usr/bin/env python3
# -*- code: utf-8 -*-
"""
Fichero que maneja el comportamiento de las tarjetas
"""
from flask import Blueprint, request, session

from PiHome.card.model import Card
from PiHome.home import Home
from PiHome.user.model import User

card_ctr = Blueprint('card', __name__, url_prefix='/card')

home = Home()


@card_ctr.route('/get', methods=['GET'])
def get():
    """Metodo que devuelve la información de todas las tarjetas
    o la que se le indique por parámetro"""

    id_card = request.args.get('id')
    _base = home.get_base_params("Listado de las tarjetas registradas")

    if 'name' in session and session['name'] != '':
        if session['category'] in (3, 2):

            if id_card != None:
                cards = Card.query.join('User').add_columns(
                    User.name,
                    Card.codigo)
            else:
                cards = Card.query.filer_by(id=id_card).join('User').add_columns(
                    User.name,
                    Card.codigo)
        else:
            _base = home.get_base_params("Mostrando prueba de lista", 0)
