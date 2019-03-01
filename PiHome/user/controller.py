from flask import render_template, Blueprint, session

from PiHome.group.model import Group
from PiHome.user.model import User

# Define the blueprint: 'user', set its url prefix: app.url/auth
user_ctr = Blueprint('user', __name__, url_prefix='/user')


@user_ctr.route('/all', methods=['GET'])
@user_ctr.route('/all/<int:page>', methods=['GET'])
def show(page=1):
    """
        Muestra la información de 'users'
    """
    per_page = 5
    users = User.query.join('group').add_columns(
        User.name,
        User.email,
        Group.category)  # .paginate(page,per_page,False)

    if 'name' in session:
        if session['name'] != '':
            nombre = session['name']
            category = session['category']

    return render_template('show.html',
                           title='Mostrando prueba de lista',
                           nombre=nombre,
                           category=category,
                           results=users,
                           table='users')
