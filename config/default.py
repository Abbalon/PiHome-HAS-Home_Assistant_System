#!venv/bin/python
# -*- code: utf-8 -*-
"""
	Módulo que establece la configuracion del sistema
	This file contains most of the configuration variables that your app needs.
"""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """docstring for Config"""

    # Secret key for signing cookies
    # SECRET_KEY = os.urandom(16)

    def __init__(self, arg):
        super(Config, self).__init__()
        self.arg = arg


class DevelopmentConfig(Config):
    PROJECT_NAME = "PiHome"
    # SERVER_NAME = "PiHome.tfg"

    # Todo: Modificar los parámetros necesarios para adaptarlos a tu proyecto

    # Las direcciones de verdad se encuentran en instace/config
    __debugURLUser = 'mysql+pymysql://test:test@localhost/debug'
    __mailUserName = 'name@domain.com'
    __defaultUserName = 'name+surname@domain.com'
    __mailPassword = 'password'

    """
        Parámetros de conexión a la BD
    """

    # Statement for enabling the development environment
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = __debugURLUser
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_CONNECT_OPTIONS = {}

    MAIL_USERNAME = __mailUserName
    DEFAULT_MAIL_SENDER = __defaultUserName
    MAIL_PASSWORD = __mailPassword  # os.environ.get('PASSWORD_EMAIL_DEBUG') # $ export PASSWORD_EMAIL_DEBUG = ''

    """
        Parámetros de conexión del módulo ZigBee
    """
    # XBEE_PORT = '/dev/ttyUSB0'  # Puerto en el que se encuentra el ZigBee
    XBEE_PORT = ['/dev/ttyUSB0']
    XBEE_BAUDRATE = 9600  # Frecuencia de emisión

    """docstring for DevelopmentConfig"""

    def __init__(self, arg):
        super(DevelopmentConfig, self).__init__()
        self.arg = arg


# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

TEST = None
