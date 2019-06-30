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
