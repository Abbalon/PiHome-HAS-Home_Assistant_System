# Define the blueprint: 'user', set its url prefix: app.url/auth
import threading

from flask import Blueprint, session, flash, render_template, redirect, url_for, copy_current_request_context, request

from PiHome import db
from PiHome.home import Home
from PiHome.home.form import LogInForm, ContactForm
from PiHome.user.form import SignUpForm
from PiHome.user.model import User

home_ctr = Blueprint('home', __name__, url_prefix='')

home = Home()


@home_ctr.route('/')
@home_ctr.route('/index')
def index():
    """
        Gestión de la llamada a la página principal
    """
    home_status = home.get_base_params("TFG", 0)

    if 'name' in session:
        if session['name'] != '':
            home_status = home.get_base_params("Bienvenido " + session['name'], 0)
            flash('Estás logeado')
    else:
        home_status = home.get_base_params("TFG", 0)
        flash('No estás logeado')

    return render_template('index.html',
                           base=home_status)


@home_ctr.route('/logIn', methods=['GET', 'POST'])
def log_in():
    """
        Enrutamiento y control del acceso al sistema
    """
    error = None
    log_in_form = LogInForm(request.form)
    for data in log_in_form:
        print(data)

    if request.method == 'POST':
        form_name = log_in_form.name.data
        form_pass = log_in_form.password.data

        user = User.query.filter_by(name=form_name).first()
        if user is not None and user.verificar_hash(form_pass) and user.validated:
            session['name'] = form_name
            session['logged_in'] = True
            session['category'] = user.group_Id

            flash('Te has logeado correctamente')
            return redirect(url_for('home.index'))

        else:
            session['logged_in'] = False
            error = 'Nombre y/o contraseña erroneos.'
            flash('¡El nombre o la contraseña parecen no ser correctas!')

    return render_template('logIn.html',
                           base=home.get_base_params("Who are you?", 0),
                           error=error,
                           form=log_in_form)


@home_ctr.route('/logOut')
def log_out():
    """
        Salida del sistema
    """

    if 'name' in session:
        # Elimina el 'username' de la sesión si es que estaba logeado
        session.pop('name', None)
        session.pop('category', None)

    if 'logged_in' in session:
        # Elimina el estado de la sesión si es que estaba logeado
        session.pop('logged_in', None)

    flash('Te has deslogeado correctamente')

    return redirect(url_for('home.index'))


@home_ctr.route('/signUp', methods=['GET', 'POST'])
def sign_up():
    """
        Enrutamiento y control del registro al sistema.

        Datos a insertar por el usuario:

        name, email, password
    """

    sign_up_form = SignUpForm(request.form)

    if request.method == 'POST' and \
            sign_up_form.validate():
        user = User(
            name=sign_up_form.name.data,
            email=sign_up_form.email.data,
            password=sign_up_form.password.data
        )

        for value in sign_up_form:
            print(value.data)

        flash('Gracias por registrarte')

        subject = 'Gracias por registrarte '
        body = 'El registro se ha producido correctamente'

        @copy_current_request_context
        def send_notification(email, subject, body):
            send_email(email, subject, body)

        sender = threading.Thread(
            name='mail_sender',
            target=send_notification,
            args=[user.email, subject, body])

        sender.start()

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('logIn',
                                name=sign_up_form.name.data))

    return render_template('signUp.html',
                           title="Let's Sign Up",
                           form=sign_up_form)


@home_ctr.route('/elements')
def elements():
    dynamic = 0
    if 'category' in session:
        category = session['category']
        dynamic = 1
    else:
        category = 0


    return render_template('elements.html',
                           base=home.get_base_params("Ejemplos de Elementos", dynamic))


@home_ctr.route('/contact', methods=['GET', 'POST'])
def contact():
    email_contact = ContactForm(request.form)

    if request.method == 'POST' and email_contact.validate():
        for dato in email_contact:
            print(dato.data)

    return render_template('contact.html', form=email_contact)


@home_ctr.route('/Anteproyecto')
def ante():
    return render_template('Anteproyecto_TFG.html')
