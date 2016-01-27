# OpenCNL

Biblioteca para ler e consultar o banco de dados CNL (Código Nacional de Localidade) seguindo especificações da ANATEL (Agência Nacional de Telecomunicações).

## Exemplo

- Prefeitura Municipal de Natal/RN - (84) 3211-8243
- Prefeitura Municipal de Parnamirim/RN - (84) 3644-8100
- Prefeitura Municipal de Mossoró/RN - (84) 3315-4935
- Prefeitura Municipal de São Paulo/SP - (11) 3124-5100

```python
from open_cnl.open_cnl import OpenCNL

# Natal/RN - Centro de custo
cnl = OpenCNL('~/CE_F_130250.TXT', '8432118243')

# Parnamirim/RN - Área conurbada
# >>> 'VC1'
cnl.buscar_numero('8436448100')

# Mossoró/RN - Mesmo estado
# >>> 'VC2'
cnl.buscar_numero('8433154935')

# Parnamirim/RN - Área conurbada
# >>> 'VC3'
cnl.buscar_numero('1131245100')
```

## Como funciona

O código processa a base de dados em TXT para um banco de dados SQLite3 em memória RAM. O programa ocupa em média 35MB de RAM e apresenta resultados bastante rápidos, aproximadamente 39 consultas por segundo.

## Autor

Victor Torres <vpaivatorres@gmail.com>
