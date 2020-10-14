#!venv/bin/python3
# -*- code: utf-8 -*-
"""Formulario para el filtro del tránsito registrado"""
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.fields import Label
from wtforms.fields.html5 import DateField


class TransitFilter(FlaskForm):
    user = "Usuario"
    user_name_lb = Label(field_id="user_name", text=user)
    user_name = SelectField(user)

    f_desde = "Fecha desde"
    f_inicio_lb = Label(field_id="f_inicio", text=f_desde)
    f_inicio = DateField(f_desde, format='%d/%m/%Y')

    f_hasta = "Fecha hasta"
    f_fin_lb = Label(field_id="f_fin", text=f_hasta)
    f_fin = DateField(f_hasta, format='%d/%m/%Y')
    # submit = SubmitField('Filtar')
