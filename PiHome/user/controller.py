from flask import render_template, Blueprint, session

from PiHome.group.model import Group
from PiHome.user.model import User
from PiHome.utils.base import Home

# Define the blueprint: 'user', set its url prefix: app.url/auth
user_ctr = Blueprint('user', __name__, url_prefix='/user')

home = Home()


@user_ctr.route('/all', methods=['GET'])
@user_ctr.route('/all/<int:page>', methods=['GET'])
def show(page=1):
    """
        Muestra la información de 'users'
    """

    _base = home.get_base_params()
    users = None

    per_page = 5

    if 'name' in session and session['name'] != '':
        if session['category'] == 3:
            _base = home.get_base_params("Mostrando prueba de lista", 0)

            users = User.query.join('group').add_columns(
                User.name,
                User.email,
                Group.category)  # .paginate(page,per_page,False)
        else:
            _base = home.get_base_params("Mostrando prueba de lista", 0)

    return render_template('showUsers.html',
                           base=_base,
                           results=users,
                           table='users')


def get_user_lite_list() -> list:
    """
Método que devolverá un listado de la tupla (id, nombre), de los usuarios validados
    """
    user_list = [(u.id, u.name) for u in User.query.filter(User.validated == True).all()]
    user_list.insert(0, ("", "Selecciona un usuario para filtrar"))
    return user_list
