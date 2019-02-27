from PiHome import db
from PiHome.user.model import User


def validate_user(user_id):
    """
        Valida el acceso al sistema del usuario con id='user_id'
    """

    user = User.query.filter_by(id=user_id).first()
    user.validated = True

    db.session.commit()


def upgrade_user(user_id, group_id):
    """
        Cambia la categoría del usuario con id='user_id'
    """

    user = User.query.filter_by(id=user_id).first()
    user.group_Id = group_id

    db.session.commit()


def delete_user(user_id):
    """
        Borra del sistema al usuario con id='user_id'
    """

    user = User.query.filter_by(id=user_id).first()

    db.session.delete(user)
    db.session.commit()
