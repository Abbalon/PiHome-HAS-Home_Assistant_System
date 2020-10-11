#!venv/bin/python3
# -*- code: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators, SubmitField

from PiHome.device.model import Family


class AddDeviceForm(FlaskForm):
    device_name_id = "device_name"
    device_name_ph_text = "Nombre del nuevo dispositivo"
    device_name = StringField(
        [validators.Length(max=32, message="El nombre del dispositivo no puede exceder los 32 caráctres"),
         validators.required],
        id=device_name_id, description=device_name_ph_text, render_kw={"placeholder": device_name_ph_text})

    device_iface_id = "device_iface"
    device_iface_ph_text = "Interface del nuevo dispositivo"
    device_iface = SelectField([validators.required], id=device_iface_id, description=device_iface_ph_text,
                               choices=(('', device_iface_ph_text), ('XBee', 'XBee')))

    device_id_id = "device_id"
    device_id_tit_text = "Dirección del nuevo dispositivo. No ha de superar los 64 caracteres"
    device_id_ph_text = "Dirección del dispositivo"
    device_id = StringField(
        [validators.Length(max=64, message="El nombre del dispositivo no puede exceder los 64 caráctres"),
         validators.required],
        id=device_id_id, description=device_id_tit_text, render_kw={"placeholder": device_id_ph_text})

    device_remote_id = "device_remote"
    device_remote_ph_text = "Dirección remota del dispositivo"
    device_remote_tit_text = "Dirección remota del nuevo dispositivo. No ha de superar los 64 caracteres. Opcional"
    device_remote = StringField(
        [validators.Length(max=64, message="El nombre del dispositivo no puede exceder los 64 caráctres"),
         validators.optional],
        id=device_remote_id, description=device_remote_tit_text, render_kw={"placeholder": device_remote_ph_text})

    device_fam_id = "device_fam"
    device_fam_ph_text = "Familia del nuevo dispositivo"
    device_fam = SelectField([validators.required], id=device_fam_id, description=device_fam_ph_text,
                             choices=Family.get_list())

    guardar_btn = SubmitField(label="Guardar")
