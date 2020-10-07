#!venv/bin/python3
# -*- code: utf-8 -*-
"""
Fichero que maneja el comportamiento de las tarjetas
"""
from flask import Blueprint, request, session, render_template

from PiHome.card.model import Card
from PiHome.user.model import User
from PiHome.utils.base import Home, ShowData

card_ctr = Blueprint('card', __name__, url_prefix='/card')

home = Home()


@card_ctr.route('/show_card', methods=['GET'])
def show_card():
    """
    Método que muestra las tarjetas que están dadas de alta en el sistema
    ---
    tags:
        - Cards actions
    parameters:
        - name: id
          description: Si se desea mostrar información específica de esa tarjeta
          in: path
          type: integer
          required: false
    responses:
        500:
          description: Error The number is not integer!
        200:
          description: Render page with a list of cards
          schema:
            $ref: '/cards.html'
    """

    id_card = request.args.get('id')
    _base = home.get_base_params(_title="Listado de las tarjetas registradas")
    title = "Tarjetas registradas"
    header = None
    body = None

    if 'name' in session and session['name'] != '':
        if session['category'] in (3, 2):

            header = ["Usuario", "Tarjeta", "Último registro"]

            if id_card is None:
                body = Card.query.join('user').add_columns(
                    User.name,
                    Card.ref).all()
            else:
                body = Card.query.filer_by(id=id_card).join('user').add_columns(
                    User.name,
                    Card.ref).all()
        else:
            _base = home.get_base_params(_title="Mostrando prueba de lista", _dynamic=0)

        cards = ShowData(title, header, body)

        return render_template('cards.html',
                               base=_base,
                               results=cards,
                               table='Tarjetas de acceso')
    else:
        return render_template('error.html')


@card_ctr.route('/new_card', methods=['GET'])
def new_card():
    """Metodo que devuelve la información de todas las tarjetas
    o la que se le indique por parámetro
    ---
    tags:
        - Cards actions
    parameters:
        - name: id
          description: Si se desea mostrar información específica de esa tarjeta
          in: path
          type: integer
          required: false
    responses:
        500:
          description: Error The number is not integer!
        200:
          description: Render page with a list of cards
          schema:
            $ref: '/cards.html'
    """

    id_card = request.args.get('id')
    _base = home.get_base_params(_title="Listado de las tarjetas registradas")

    if 'name' in session and session['name'] != '':
        if session['category'] in (3, 2):

            if id_card is not None:
                cards = Card.query.join('user').add_columns(
                    User.name,
                    Card.ref)
            else:
                cards = Card.query.filter_by(id=id_card).join('User').add_columns(
                    User.name,
                    Card.ref)
        else:
            _base = home.get_base_params(_title="Mostrando prueba de lista", _dynamic=0)
