from flask import Blueprint, request, session, render_template

from PiHome.admin.form import ValidateForm, UpgradeForm
from PiHome.admin.utils import validate_user, delete_user
from PiHome.group.model import Group
from PiHome.home import Home
from PiHome.user.model import User

admin_ctr = Blueprint('admin', __name__, url_prefix='/admin')

home = Home()


@admin_ctr.route('/validate', methods=['GET', 'POST'])
# @app.route('/validate/<int:userId>', methods = ['GET', 'POST'])
def validate():
    """Muestra la información de los usuarios sin validar en el sistema"""

    validate_form = ValidateForm(request.form)

    if request.method == 'POST':
        selected_users = request.form.getlist("verified")
        dropped_users = request.form.getlist("denied")

        for selected_id in selected_users:
            #: validate_user(<int>) Confirma el acceso al sistema al usuario con la id pasada por parámetro
            validate_user(selected_id)

        for dropped_id in dropped_users:
            #: deleteUser(<int>) Anula el acceso al sistema al usuario con la id pasada por parámetro
            delete_user(dropped_id)

    #: Si se ha creado alguna sesion
    if 'category' in session and session['category'] == 3:
        #: Si la sesión creada es la adecuada
        per_page = 5
        user = User.query.filter_by(validated=0).join('group').add_columns(
            User.id,
            User.name,
            User.email,
            Group.category)  # .paginate(page,per_page,False)
        return render_template('validate.html',
                               base=home.get_base_params('Usuarios sin confirmar'),
                               results=user,
                               form=validate_form)

    #: Si no, retorna la página de error
    return render_template('error.html')


@admin_ctr.route('/update_category', methods=['GET', 'POST'])
def update_category():
    """
        Muestra la información de los usuarios sin validar en el sistema
    """

    upgrade_from = UpgradeForm(request.form)

    if request.method == 'POST':
        selected_users = request.form.getlist('category')

        for user in selected_users:
            user = user.split(',')
            if user != ['']:
                upgrade_user(int(user[0]), int(user[1]))

    #: Si se ha creado alguna sesion
    if 'category' in session and session['category'] == 3:
        #: Si la sesión creada es la adecuada

        per_page = 5
        users = User.query.filter_by(validated=1).join('group').add_columns(
            User.id,
            User.name,
            User.email,
            Group.category)  # .paginate(page,per_page,False)

        categories = Group.query.all()

        return render_template('updateCategory.html',
                               base=home.get_base_params('Actualizar categoria'),
                               results=users,
                               form=upgrade_from,
                               groups=categories,
                               category=session['category'])

    #: Si no, retorna la página de error
    return render_template('error.html')
