from PiHome import db, app
from PiHome.card.model import Card
from PiHome.group.model import Group
from PiHome.user.model import User


def __create_foreign_keys():
    """
        Establece el estado básico de la BD
    """

    group = Group.query.filter_by(id='1').first()
    if group is None:
        std_group = Group(
            category='Estandar',
            definition='Usuario estándar, puede hacer uso del sistema de control de acceso.'
        )

        wd_group = Group(
            category='WatchDog',
            definition='Usuario vigilante, usuario estándar con permisos remotos y visualización de logs.'
        )

        adm_group = Group(
            category='Admin',
            definition='Admin'
        )

        admin = User(
            name='admin',
            password='admin',
            email='PiDomoticTFG+admin@gmail.com',
            group=adm_group,
            validated=True
        )

        card = Card(
            user=admin,
            ref=app.config['GITHUB_TOKEN']
        )

        db.session.add(std_group)
        db.session.add(wd_group)
        db.session.add(adm_group)
        db.session.add(admin)
        db.session.add(card)

        print("Commit")
        db.session.commit()
