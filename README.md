# OpenCNL

[![Build Status](https://travis-ci.org/EvoluxBR/open-cnl.svg?branch=master)](https://travis-ci.org/EvoluxBR/open-cnl)
[![PyPI version](https://badge.fury.io/py/open-cnl.svg)](https://badge.fury.io/py/open-cnl)

Biblioteca para ler e consultar o banco de dados CNL (Código Nacional de Localidade) seguindo especificações da ANATEL (Agência Nacional de Telecomunicações).

## Instalação

```shell
pip install open-cnl
```

## Importando a base da ANATEL

Você pode fazer o download do banco de dados atualizado do site da ANATEL
e importar para um banco de dados SQLite3.

### Terminal

```shell
python -m open_cnl.open_cnl_importer ./cnl_anatel.sqlite3
```

### Python

```python
from open_cnl.open_cnl_importer import OpenCNLImporter

open_cnl_importer = OpenCNLImporter('./cnl_anatel.sqlite3')
open_cnl_importer.importar_base()
```

## Exemplo prático

Vamos utilizar como exemplo o telefone da prefeitura municipal de Natal/RN:
(84) 3211-8243. Veja este código no arquivo `exemplo.py`.

```python
from open_cnl.open_cnl import OpenCNL

# Inicializamos a classe que se
# conecta ao banco de dados
cnl = OpenCNL('./cnl_anatel.sqlite3')

# Pesquisando por um número de Natal/RN
localidade = cnl.pesquisar_localidade('843211', '8243')
```

Os dados retornados estarão num dicionário no seguinte formato:

```python
{
    'prestadora': u'TELEMAR NORTE LESTE S.A.',
    'nome_da_localidade': u'NATAL',
    'hemisferio': u'S',
    'numero_da_faixa_final': u'8999',
    'sigla_cnl_da_area_local': u'NTL',
    'numero_da_faixa_inicial': u'8000',
    'longitude': u'351232',
    'prefixo': u'843211',
    'codigo_da_area_de_tarifacao': u'842',
    'latitude': u'547419',
    'codigo_cnl': u'84000',
    'sigla_uf': u'RN',
    'nome_do_municipio': u'NATAL',
    'sigla_cnl': u'NTL'
}
```

Caso uma localidade não seja encontrada será retornado o valor `None`.

### JSON

Na inicialização da classe podemos definir o parâmetro `as_json` como `True`.
O padrão desse argumento é `False` e quando verdadeiro, permite que os dados
sejam retornados em uma string no formato JSON.

```python
from open_cnl.open_cnl import OpenCNL

cnl = OpenCNL('./cnl_anatel.sqlite3')
cnl.pesquisar_localidade('843211', '8243', as_json=True)
```

## Autor

Victor Torres <vpaivatorres@gmail.com>

## Contribuidores

Stefan Yohansson <sy.fen0@gmail.com>
João Vitor Gomes <vitorjoaofg@gmail.com>
