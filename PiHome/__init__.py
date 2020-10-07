#!venv/bin/python3
# Import flask and template operators
import sys
import threading

from flasgger import Swagger
from flask import Flask, render_template
# Import SQLAlchemy
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
# Define the WSGI application object
from flask_wtf import CSRFProtect

from PiHome.swagger import specs
from PiHome.utils.stack_switcher import StackSwitcher
from PiHome.utils.xbee import XBee, XBeeInstanceException

app = Flask(__name__, instance_relative_config=True)

mail = Mail()

# Carga de la configuración por defecto
app.config.from_object('config.default.DevelopmentConfig')

# Carga de los valor desde instance
app.config.from_pyfile('config.py')

app.config['SWAGGER'] = {
    'title': 'My API',
    'uiversion': 3,
    "specs_route": "/swagger/"
}
swagger = Swagger(app, template=specs)

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Creamos el objeto que recojera los mensajes entrantes al sistema
try:
    stack = StackSwitcher.get_instance(app)
except Exception as e:
    app.logger.error("Error en la creacción de la pila de llamadas.\n{}".format(e))
    raise e

thread_list = []

# Definimos la interface xbee
xbee = None
xbee_thread = threading.Thread
try:
    # xbee = XBee.get_instance(stack, app)
    xbee = XBee.get_instance(app)
    xbee_thread = threading.Thread(name="XBee listener", target=xbee.esperar_hasta_recibir_orden)
except XBeeInstanceException as xie:
    app.logger.warning(str(xie))
except Exception as e:
    app.logger.error(str(e))

# elemento que guardará los dispositivos almacenados
device_list = {}

# Import a module / component using its blueprint handler variable (mod_auth)
from PiHome.user.controller import user_ctr
from PiHome.group.controller import group_ctr
from PiHome.admin.controller import admin_ctr
from PiHome.home.controller import home_ctr
from PiHome.transit.controller import transit_ctr
from PiHome.card.controller import card_ctr
from PiHome.device.controller import device_ctr
from PiHome.swagger import swagger_ctr
from PiHome.utils.db_setUp import __create_foreign_keys


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Register blueprint(s)
app.register_blueprint(admin_ctr)
app.register_blueprint(user_ctr)
app.register_blueprint(home_ctr)
app.register_blueprint(group_ctr)
app.register_blueprint(transit_ctr)
app.register_blueprint(card_ctr)
app.register_blueprint(device_ctr)
app.register_blueprint(swagger_ctr)

"""
Prevención de XSS & XSRF
"""
csrf = CSRFProtect()

"""
Función que carga los dispositivos dados de alta en la bbdd como elementos interoperables
"""
from PiHome.utils.db_setUp import __load_devices
from PiHome.device.model import Device
from PiHome.device.cerradura import Cerradura


def load_devices():
    devices = Device.get_devices()
    modelo = None
    for dev in devices:
        for fam in dev.Family:
            if fam.family.name == "Cerradura":
                modelo = Cerradura(app, modelo=dev)

        device_list[dev.id] = modelo


def start_devices_join():
    for dev in device_list.values():
        dev.thread.start()
        thread_list.append(dev.thread)


"""
Inicializa la aplicación y arranca los servicios necesarios
"""
if __name__ == "PiHome":
    try:
        csrf.init_app(app)  # Inicia la aplicación con la cofiguración establecida
        db.init_app(app)  # Carga la configuración de la bd
        mail.init_app(app)  # Arranca el servidor de correo
        # mail.init_mail()
        xbee.init_app(xbee_thread)  # Iniciamos el funcionamiento de la antena XB
        thread_list.append(xbee_thread)

        with app.app_context():
            # db.drop_all()  # Borra la BD
            db.create_all()  # Crea las tablas que no existan
            # __create_foreign_keys()  # Crea los datos básicos de la la bbdd
            # __load_devices() # Crea los dispositivos standart
            load_devices()  # Crea un controlador para cada dispositivo de la bbdd
            start_devices_join()
            app.logger.info("Inicializada la aplicación.")
            # for thread in thread_list:
            #     thread.join()

    except KeyboardInterrupt:
        app.logger.warning("Proceso abortado por el usuario")
        sys.exit(0)
    except Exception as e:
        app.logger.error(str(e))
        sys.exit(1)
