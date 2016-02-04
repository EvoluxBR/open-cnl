# -*- coding: utf-8 -*-
from datetime import datetime
from open_cnl.open_cnl import OpenCNL


# Natal/RN - Centro de custo
cnl = OpenCNL('banco.sqlite3', '843211', '8243')

# Parnamirim/RN - Área conurbada
# >>> 'VC1'
print cnl.buscar_localidade('843644', '8100')

# Mossoró/RN - Mesmo estado
# >>> 'VC2'
print cnl.buscar_localidade('843315', '4768')

# São Paulo/SP - Outro estado
# >>> 'VC3'
print cnl.buscar_localidade('113124', '5100')

def teste(cnl):
    # Parnamirim/RN - Área conurbada
    # >>> 'VC1'
    cnl.buscar_localidade('843644', '8100')

    # Mossoró/RN - Mesmo estado
    # >>> 'VC2'
    cnl.buscar_localidade('843315', '4768')

    # São Paulo/SP - Outro estado
    # >>> 'VC3'
    cnl.buscar_localidade('113124', '5100')

inicio = datetime.now()
quantidade = 100
for i in range(quantidade):
    teste(cnl)

fim = datetime.now()
print 'Testes (%s)' % (3 * quantidade)
print 'Tempo de execução -->', fim - inicio
