#!venv/bin/python
from PiHome import db, app
from PiHome.card.model import Card
from PiHome.device.model import Family, Action, Device, FamilyDevice
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

        family = Family(
            name='Generica',
            description='Familia a la que pertenecerán todos los dispositivos'
        )

        sleep_action = Action(
            family=family,
            name='Dormir',
            description='Desconecta el dispositivo',
            cmd='APAGAR'
        )

        verbose_action = Action(
            family=family,
            name='Verbose',
            description='Retorna la información del dispositivo',
            cmd='ECHO',
            response_needed=1
        )

        lock = Family(
            name='Cerradura',
            description='Familia que recogerá las funcionalidades comunes a todas las cerraduras'
        )

        open_action = Action(
            family=lock,
            name='Abrir',
            description='Desbloquea la cerradura de la puerta',
            cmd='ABRIR',
            response_needed=1
        )

        close_action = Action(
            family=lock,
            name='Cerrar',
            description='Bloquea la cerradura de la puerta',
            cmd='CERRAR',
            response_needed=1
        )

        watch_dog = Family(
            name='Control de acceso',
            description='Familia que recogerá las funcionalidades comunes a los controles de acceso'
        )

        sniff_action = Action(
            family=watch_dog,
            name='Leer tarjeta',
            description='Lee una tarjeta y retorna su id',
            cmd='READ_TAG',
            response_needed=1
        )

        access_door = Device(
            name='Puerta principal',
            interface='XBee',
            id_external='0013A20041513615',
            id_remote='0013A200415135C7',
            enabled=1
        )

        fd_acc_fam = FamilyDevice(device=access_door, family=family)
        fd_acc_wat = FamilyDevice(device=access_door, family=watch_dog)
        fd_acc_loc = FamilyDevice(device=access_door, family=lock)

        db.session.add(family)
        db.session.add(sleep_action)
        db.session.add(verbose_action)
        db.session.add(watch_dog)
        db.session.add(sniff_action)
        db.session.add(lock)
        db.session.add(open_action)
        db.session.add(close_action)
        db.session.add(access_door)
        db.session.add(fd_acc_fam)
        db.session.add(fd_acc_wat)
        db.session.add(fd_acc_loc)

        print("Commit")
        db.session.commit()
