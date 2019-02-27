from werkzeug.security import generate_password_hash, check_password_hash

from PiHome import db
from PiHome.dataBase import BaseDB


class User(BaseDB):
    """
        Modelo de datos del usuario
    """

    #: Nombre de tabla
    __tablename__ = 'users'

    group_Id = db.Column(
        db.Integer,
        db.ForeignKey('groups.id'),
        nullable=False)
    name = db.Column(
        db.String(25),
        unique=True)
    label = db.Column(
        db.String(25))
    email = db.Column(
        db.String(56),
        unique=True)
    password = db.Column(
        db.String(93),
        nullable=False)
    validated = db.Column(
        db.Boolean,
        default=False,
        nullable=False)
    # signedIn = db.Column(
    #     db.DateTime,
    #     default=datetime.datetime.now)

    #: Establece la relación con la tabla 'groups'
    group = db.relationship(
        'Group',
        lazy='select',
        backref='User')

    def __init__(self, name, email, password, label=None, group_id=1, validated=False, **kwargs):
        """
            Inicializa un usuario

            Por defecto:
                - Tiene que contener los datos requeridos del formulario 'log_in':
                    - Nombre
                    - Email
                    - Password
                - No tiene ningún 'label' asignado
                - Pertenece al grupo 'Estandar'
        """

        super(User, self).__init__(**kwargs)

        _hash_str = self.__hash_pwd(password)

        self.group_Id = group_id
        self.name = name
        self.label = label
        self.password = _hash_str
        self.validated = validated
        self.email = email

    @staticmethod
    def __hash_pwd(password):
        """
            Metodo privado para generar el 'hash' del usuario
        """
        return generate_password_hash(password)

    def verificar_hash(self, password):
        """
            Metodo público para contrastar los 'hash´s' de las pwd
        """
        return check_password_hash(self.password, password)
