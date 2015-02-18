#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='ppp_datamodel',
    version='0.6.8',
    description='Data model for the Projet Pensées Profondes.',
    url='https://github.com/ProjetPP/PPP-datamodel-Python',
    author='Valentin Lorentz',
    author_email='valentin.lorentz+ppp@ens-lyon.org',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries',
    ],
    install_requires=[
    ],
    packages=[
        'ppp_datamodel',
        'ppp_datamodel.nodes',
        'ppp_datamodel.communication',
    ],
)


