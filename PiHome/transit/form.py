#!/usr/bin/env python3
# -*- code: utf-8 -*-
"""Formulario para el filtro del tránsito registrado"""
from flask_wtf import Form
from wtforms import StringField, DateField


class TransitFilter(Form):
    user_name = StringField("Usuario")
    f_inicio = DateField("Fecha desde")
    f_fin = DateField("Fecha hasta")
