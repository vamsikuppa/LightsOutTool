#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from setuptools import setup

setup(
    name='LightsOutTool',
    version='1.0',
    packages=['my_app', 'my_app.product'],
    url='',
    license='GNU General Public License v3',
    author='Vamsi Kuppa',
    author_email='',
    description='',
    platforms='any',
    install_requires=[
        'Flask',
        'Flask-Login',
        'Flask-Migrate',
        'Flask-SQLAlchemy',
        'Flask-Script',
        'Flask-WTF',
        'PyMySQL',
        'SQlAlchemy',
        'WTForms',
        'paramiko',
        'requests',
    ],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
