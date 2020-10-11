#!venv/bin/python3
# -*- code: utf-8 -*-
"""
Fichero que maneja el comportamiento de las tarjetas
"""
from flask import Blueprint, request, session, render_template, flash, redirect, url_for

from PiHome.card.form import AddCardForm
from PiHome.card.model import Card
from PiHome.user import controller as UserDAO
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


@card_ctr.route('/new_card', methods=['GET', 'POST'])
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

    title = "Alta de tarjetas"
    _base = home.get_base_params(_title=title, _header=title)

    response = render_template('error.html'), 404
    flash_msg = None

    if 'name' in session and session['name'] != '':
        if session['category'] in (3, 2):
            form = AddCardForm(request.form)

            if request.method == 'GET':
                users = UserDAO.get_user_lite_list()
                form.user_select.choices = users

                response = render_template('newCard.html',
                                           base=_base,
                                           form=form)

            if request.method == 'POST':
                response = None
                id_tag = form.card_id.data
                id_usr = form.user_select.data

                try:
                    if form.guardar_btn.data and form.validate():
                        card_saved = save(id_tag=id_tag, id_usr=id_usr)
                        if card_saved:
                            flash_msg = "Se ha asignado la tarjeta '{}' al usuario '{}'".format(id_tag,
                                                                                                card_saved.user.name)
                    if form.leer_btn.data:
                        print("Leer")
                except Exception as e:
                    flash_msg = format(e)
                    flash(flash_msg, category='error')
                else:
                    flash(flash_msg)

                response = redirect(url_for('card.new_card'))

    return response


def save(**kwargs):
    """Guarda la nueva tag asociadad a un usuario

    ---

    :return La tarjeta creada o None si ha ocurrido algún problema
    :rtype: Card
    :param \**kwargs:  Ver abajo
    :type kwargs: dict

    :keyword id_tag: id de la targeta RFID que identifica al usuario. No puede existir en el sistema
    :keyword id_usr: id del usuario al que se le va a asignar la tarjeta nueva"""

    response = None

    card = None

    id_tag = kwargs.get("id_tag")
    id_usr = kwargs.get("id_usr")

    user = User.is_validated(id_usr)
    if id_tag and id_usr and user:
        card = None
        if user.Card:
            card = user.Card[0]
            card.ref = id_tag
        else:
            card = Card(user=user, ref=id_tag)

        card.save()
        response = card

    return response
