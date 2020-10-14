#!venv/bin/python3
# -*- code: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError

from PiHome.device.model import Family, Device


class AddDeviceForm(FlaskForm):
    """Formulario para dar de alta un nuevo dispositivo

    ---

    :keyword device_name: Nombre del dispositivo
    :keyword device_iface: Interface por la que operará el dispositivo
    :keyword device_id: Dirección a la que se referirá el dispositivo
    :keyword device_remote Dirrección con la que se comunicará el dispositivo
    :keyword device_fam: Familias que definirán el comportamiento del dispositivo
    :keyword guardar_btn: Botón de submit

    """
    __device_name_id = "device_name"
    __device_name_ph_text = "Nombre del nuevo dispositivo"
    device_name = StringField(id=__device_name_id, description=__device_name_ph_text,
                              render_kw={"placeholder": __device_name_ph_text})

    __device_iface_id = "device_iface"
    __device_iface_ph_text = "Interface del nuevo dispositivo"
    __iface_list = (('', __device_iface_ph_text), ('XBee', 'XBee'))
    device_iface = SelectField(id=__device_iface_id, description=__device_iface_ph_text,
                               choices=__iface_list)

    __device_id_id = "device_id"
    __device_id_tit_text = "Dirección del nuevo dispositivo. No ha de superar los 64 caracteres"
    __device_id_ph_text = "Dirección del dispositivo"
    device_id = StringField(id=__device_id_id, description=__device_id_tit_text,
                            render_kw={"placeholder": __device_id_ph_text})

    __device_remote_id = "device_remote"
    __device_remote_ph_text = "Dirección remota del dispositivo"
    __device_remote_tit_text = "Dirección remota del nuevo dispositivo. No ha de superar los 64 caracteres. Opcional"
    device_remote = StringField(id=__device_remote_id, description=__device_remote_tit_text,
                                render_kw={"placeholder": __device_remote_ph_text})

    __device_fam_id = "device_fam"
    __device_fam_ph_text = "Familia del nuevo dispositivo"
    __device_fam_list = []
    try:
        __device_fam_list = Family.get_list()
    except:
        pass
    device_fam = SelectMultipleField([DataRequired()], id=__device_fam_id, description=__device_fam_ph_text,
                                     choices=__device_fam_list, render_kw={"size": 2}, coerce=int)

    guardar_btn = SubmitField(label="Guardar")

    def validate_device_name(self, field):
        max_size = 32
        if not field.data or len(field.data) == 0:
            raise ValidationError("No se puede crear un dispositivo sin asignarle un nombre")

        if len(field.data) > max_size:
            raise ValidationError("El nombre del dispositivo no puede exceder los {} caráctres".format(max_size))

    def validate_device_iface(self, field):
        if not field.data or len(field.data) == 0:
            raise ValidationError("No se puede crear un dispositivo sin asignarle una interface")

        keys = [key for key, value in self.__iface_list]
        if field.data not in keys:
            raise ValidationError("El valor introducido no es un valor aceptado")

    def validate_device_id(self, field):
        max_size = 64
        if not field.data or len(field.data) == 0:
            raise ValidationError("No se puede crear un dispositivo sin asignarle su id")

        if len(field.data) > max_size:
            raise ValidationError("El id del dispositivo no puede exceder los {} caráctres".format(max_size))

        if Device.get_device_by_mac(field.data):
            raise ValidationError("Ya existe un dispositivo asociado a esa dirección")

    def validate_device_remote(self, field):
        max_size = 64

        if len(field.data) > max_size:
            raise ValidationError("El id remoto del dispositivo no puede exceder los {} caráctres".format(max_size))

    def validate_device_fam(self, field):
        if not field.data or len(field.data) == 0:
            raise ValidationError("No se puede crear un dispositivo sin asignarle, al menos, una familia")

        keys = [key for key, value in self.__device_fam_list]
        for option in field.data:
            if option not in keys or option == 0:
                raise ValidationError("Algún valor introducido no es un valor aceptado")
