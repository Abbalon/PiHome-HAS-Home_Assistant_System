# Define the blueprint: 'user', set its url prefix: app.url/auth
import threading
from PiHome import db
from PiHome import mail, app
from PiHome.home.form import LogInForm, ContactForm
from PiHome.user.form import SignUpForm
from PiHome.user.model import User
from PiHome.utils.base import Home
from PiHome.utils.mail import send_email
from flask import Blueprint, session, flash, render_template, redirect, url_for, copy_current_request_context, request
from flask_mail import Message

home_ctr = Blueprint('home', __name__, url_prefix='')

home = Home()


@home_ctr.route('/')
@home_ctr.route('/index')
def index():
    """
        Gestión de la llamada a la página principal
    """

    _base = home.get_base_params(_dynamic=1)

    if 'name' in session:
        if session['name'] != '':
            _base = home.get_base_params(_title="Bienvenido " + session['name'], _dynamic=1)
            flash('Estás logeado')
    else:
        flash('No estás logeado')

    return render_template('index.html',
                           base=_base)


@home_ctr.route('/logIn', methods=['GET', 'POST'])
def log_in():
    """
        Enrutamiento y control del acceso al sistema
    """
    _base = home.get_base_params()

    error = None
    log_in_form = LogInForm(request.form)

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
                           base=home.get_base_params(_title="Who are you?", _header="Datos de acceso"),
                           error=error,
                           form=log_in_form)


@home_ctr.route('/logOut')
def log_out():
    """
        Salida del sistema
    """

    if 'logged_in' in session:
        # Elimina el estado de la sesión si es que estaba logeado
        reset_session()

    flash('Te has deslogeado correctamente')

    return redirect(url_for('home.index'))


def reset_session():
    session.pop('name', None)
    session.pop('logged_in', False)
    session.pop('category', None)
    home.set_default()


@home_ctr.route('/signUp', methods=['GET', 'POST'])
def sign_up():
    """
        Enrutamiento y control del registro al sistema.

        Datos a insertar por el usuario:
        :param name
        :param email
        :param password

        :see PiHome.user.form.SignUpForm
    """

    _base = home.get_base_params()

    sign_up_form = SignUpForm(request.form)

    if request.method == 'POST' and \
            sign_up_form.validate():
        user = User(
            name=sign_up_form.name.data,
            email=sign_up_form.email.data,
            password=sign_up_form.password.data
        )

        # for value in sign_up_form:
        #     print(value.data)

        flash('Gracias por registrarte')

        subject = 'Gracias por registrarte '
        body = 'El registro se ha producido correctamente'

        @copy_current_request_context
        def send_notification(email, subject, body):
            send_email([email], subject, body)
            # Advertimos a los admin y Gruardianes que tiene que validar un usuario nuevo
            mails = User.get_mails_of_groups(id_groups=[2, 3])
            subject = 'Usuario pendiente de validar'
            body = 'Hay un usuario pendiente de validar.\nAcceda a la ruta ' + url_for('admin.validate')
            send_email(mails, subject, body)

        sender = threading.Thread(
            name='mail_sender',
            target=send_notification,
            args=[user.email, subject, body])

        sender.start()

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('home.log_in',
                                name=sign_up_form.name.data))

    return render_template('signUp.html',
                           base=home.get_base_params(_title="Let's Sign Up", _header="Formulario de ingreso"),
                           form=sign_up_form)


@home_ctr.route('/elements')
def elements():
    dynamic = 0
    if 'category' in session:
        category = session['category']
        dynamic = 0
    else:
        category = 0

    return render_template('elements.html',
                           base=home.get_base_params(_title="Ejemplos de Elementos", _dynamic=dynamic))


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


@home_ctr.route('/TestEmail')
def test_email():
    msg = Message(subject="Envio de email de prueba",
                  sender=app.config['DEFAULT_MAIL_SENDER'],
                  recipients=[app.config['TEST_MAIL_SENDER']],
                  body="Te ha llegado un correo")

    mail.send(msg)

    return redirect(url_for('home.index',
                            message="That's ok"))
