# Import flask and template operators
from flask import Flask, render_template
# Import SQLAlchemy
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
# Define the WSGI application object
from flask_wtf import CSRFProtect

app = Flask(__name__, instance_relative_config=True)
mail = Mail()

# Carga de la configuración por defecto
app.config.from_object('config.default')

# Carga de los valor desde instance
app.config.from_pyfile('config.py')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Import a module / component using its blueprint handler variable (mod_auth)
from PiHome.user.controller import user_ctr
from PiHome.group.controller import group_ctr
from PiHome.admin.controller import admin_ctr
from PiHome.home.controller import home_ctr
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

"""
Prevención de XSS & XSRF
"""
csrf = CSRFProtect()

"""
Inicializa la aplicación y arranca los servicios necesarios
"""

if __name__ == "PiHome":
    csrf.init_app(app)  # Inicia la aplicación con la cofiguración establecida
    db.init_app(app)  # Carga la configuración de la bd
    mail.init_app(app)  # Arranca el servidor de correo

    with app.app_context():
        # db.drop_all()  # Borra la BD
        db.create_all()  # Crea las tablas que no existan
        __create_foreign_keys()
        print("Inicializada la aplicación.")
