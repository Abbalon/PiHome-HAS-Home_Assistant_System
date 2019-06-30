# -*- code: utf-8 -*-
"""
This file contains configuration variables that shouldn’t be in version control. This includes things like API keys and
database URIs containing passwords. This also contains variables that are specific to this particular instance of your
application. For example, you might have DEBUG = False in default.py, but set DEBUG = True in instance/default.py on your
local machine for development. Since this file will be read in after default.py, it will override it and set DEBUG = True
"""
import os

DEBUG = True
# This is a secret key that is used by Flask to sign cookies. It’s also used by extensions like Flask-Bcrypt. You should
# define this in your instance folder to keep it out of version control. You can read more about instance folders
# in the next section.
SECRET_KEY = os.urandom(16)
# If you’re using Flask-Bcrypt to hash user passwords, you’ll need to specify the number of “rounds” that the algorithm
# executes in hashing a password. If you aren’t using Flask-Bcrypt, you should probably start. The more rounds used to
# hash a password, the longer it’ll take for an attacker to guess a password given the hash. The number of rounds should
# increase over time as computing power increases.
# BCRYPT_LOG_ROUNDS = ""

__debugURLAdmin = 'mysql+pymysql://PiHome_test:2ZtvzkiSTMYCDQ79@localhost:3306/PiHome_test'
__debugURLUser = 'mysql+pymysql://PiHome:oGTeQs7GunK7xXL7@localhost:3306/PiHome'

SQLALCHEMY_DATABASE_URI = __debugURLAdmin
SQLALCHEMY_ECHO = True

"""
    Parámetros para la conguración del WebMailServer
"""
MAIL_SERVER = 'smtp.gmail.com'
# MAIL_PORT = 465
# MAIL_USE_SSL = True
# MAIL_USE_TLS = False
MAIL_PORT = 587
MAIL_USE_SSL = False
MAIL_USE_TLS = True
MAIL_USERNAME = 'PiDomoticTFG@gmail.com'
DEFAULT_MAIL_SENDER = 'PiDomoticTFG+Bienvenida@gmail.com'
MAIL_PASSWORD = '#Clave de PiD@motic#'  # r'\xab\xeb\xf3\x0c\xeb\xe0\xf5\x96\xf0\xc0\xc7\xe6\x85\x98\xc3\x0b'  # os.environ.get('PASSWORD_EMAIL_DEBUG') # $ export PASSWORD_EMAIL_DEBUG = ''
MAIL_DEBUG = True
TEST_MAIL_SENDER = 'PiDomoticTFG+test@gmail.com'

# Use a secure, unique and absolutely secret key for
# signing the data.
# CSRF_SESSION_KEY = os.urandom(16)  # os.environ.get('PASSWORD_EMAIL_DEBUG') # $ export PASSWORD_EMAIL_DEBUG = ''

GITHUB_TOKEN = "210e096898ec6f58390694cf27cae145027d1893"
