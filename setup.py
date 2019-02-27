# -*- code: utf-8 -*-
"""
    Módulo que establece la metainformación del sistema

    export FLASK_APP="/.../__init__.py"
    flask run
"""

from setuptools import setup, find_packages

setup(
    name='PiDomotic',
    version='0.1',
    description='TFG by (BF0002) for UPM-ETSISI',
    author='Adrián Alonso del Peso',
    author_email='a.alonsod@alumnos.upm.es',
    license='GPL',
    url='',
    packages=find_packages(),  # ['PiDomotic'],
    include_package_data=True,
    install_requires=[i.strip() for i in open("requirements.txt").readlines()],
)
