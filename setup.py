# -*- coding: utf-8 -*-
from distutils.core import setup


setup(
    name = 'open_cnl',
    packages = ['open_cnl'],
    version = '0.8',
    description = 'Biblioteca para ler e consultar banco de dados CNL (Código Nacional de Localidade) seguindo especificações da ANATEL (Agência Nacional de Telecomunicações).',
    author = 'Victor Torres',
    author_email = 'vpaivatorres@gmail.com',
    url = 'https://github.com/evoluxbr/open-cnl',
    download_url = 'https://github.com/evoluxbr/open-cnl/tarball/0.8',
    keywords = ['anatel', 'cnl', 'base'],
    classifiers = [],
    install_requires=['requests'],
)
