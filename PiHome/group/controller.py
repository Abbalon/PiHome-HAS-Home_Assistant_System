from flask import render_template, Blueprint, session

from PiHome.group.model import Group
from PiHome.user.model import User

# Define the blueprint: 'user', set its url prefix: app.url/auth
group_ctr = Blueprint('group', __name__, url_prefix='/group')


@group_ctr.route('/show', methods=['GET'])
@group_ctr.route('/show/<int:page>', methods=['GET'])
def show(page=1):
    """
        Muestra la información de 'users'
    """
    per_page = 5
    users = User.query.join('group').add_columns(
        User.name,
        User.email,
        Group.category)  # .paginate(page,per_page,False)
    return render_template('showUsers.html',
                           title='Mostrando prueba de lista',
                           results=users,
                           table='users',
                           category=session['category'])
