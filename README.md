# OpenCNL

Biblioteca para ler e consultar o banco de dados CNL (Código Nacional de Localidade) seguindo especificações da ANATEL (Agência Nacional de Telecomunicações).

## Instalação

```shell
pip install open-cnl
```

## Exemplo

- Prefeitura Municipal de Natal/RN - (84) 3211-8243
- Prefeitura Municipal de Parnamirim/RN - (84) 3644-8100
- Prefeitura Municipal de Mossoró/RN - (84) 3315-4935
- Prefeitura Municipal de São Paulo/SP - (11) 3124-5100

```python
from open_cnl.open_cnl import OpenCNL

# Natal/RN - Centro de custo
cnl = OpenCNL('~/cnl_anatel.sqlite3', '843211', '8243')

# Parnamirim/RN - Área conurbada
# >>> 'VC1'
cnl.buscar_localidade('843644', '8100')

# Mossoró/RN - Mesmo estado
# >>> 'VC2'
cnl.buscar_localidade('843315', '4935')

# Parnamirim/RN - Área conurbada
# >>> 'VC3'
cnl.buscar_localidade('113124', '5100')
```

## Como funciona

O código processa a base de dados em TXT para um banco de dados SQLite3.


## Importando a base atualizada da ANATEL

```python
from open_cnl.open_cnl import OpenCNLImporter

cnl_importer = OpenCNLImporter('~/CE_F_130250.TXT', '~/cnl_anatel.sqlite3')
cnl_importer.importar_base()
```

## Autor

Victor Torres <vpaivatorres@gmail.com>
