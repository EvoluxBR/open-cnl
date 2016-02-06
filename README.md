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

Vamos utilizar como exemplo os telefones das prefeituras municipais das
seguintes cidades:

- Natal/RN - (84) 3211-8243
- Parnamirim/RN - (84) 3644-8100
- Mossoró/RN - (84) 3315-4935
- São Paulo/SP - (11) 3124-5100

Nosso centro de custo será Natal/RN, que está na mesma região metropolitana de
Parnamirim/RN. Mossoró/RN, por sua vez, se localiza no interior do estado. Por
último, São Paulo, que fica em outro estado. Veja o código do arquivo
`exemplo.py`.

```python
from open_cnl.open_cnl import OpenCNL

# Inicializamos a classe especificando
# nosso centro de custo: Natal/RN
cnl = OpenCNL('./cnl_anatel.sqlite3', '843211', '8243')

# Ligando de Natal/RN para
# Parnamirim/RN - Área conurbada
# >>> 'VC1'
cnl.buscar_localidade('843644', '8100')

# Agora ligando de Natal/RN para
# Mossoró/RN - Mesmo estado
# >>> 'VC2'
cnl.buscar_localidade('843315', '4935')

# Ligando de Natal/RN para
# São Paulo/SP - Outro estado
# >>> 'VC3'
cnl.buscar_localidade('113124', '5100')

# Escolhendo outro centro de custo
# sem reiniciar a classe (apenas essa consulta)
# Ligando de Mossoró/RN para
# Parnamirim/RN - Mesmo estado
# >>> 'VC2'
cnl.buscar_localidade('843644', '8100', '843315', '4935')
```

## Autor

Victor Torres <vpaivatorres@gmail.com>

## Contribuidores

Stefan Yohansson <sy.fen0@gmail.com>
