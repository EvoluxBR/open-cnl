# -*- coding: utf-8 -*-
from datetime import datetime
from open_cnl.open_cnl import OpenCNL

# Inicializamos a classe que se
# conecta ao banco de dados
cnl = OpenCNL('./cnl_anatel.sqlite3')

# Pesquisando por um número de Natal/RN
print(cnl.pesquisar_localidade('843211', '8243'))
# Parnamirim/RN - Área conurbada
print(cnl.pesquisar_localidade('843644', '8100'))
# Mossoró/RN - Mesmo estado
print(cnl.pesquisar_localidade('843315', '4768'))
# São Paulo/SP - Outro estado
print(cnl.pesquisar_localidade('113124', '5100'))

def teste(cnl):
    # Parnamirim/RN - Área conurbada
    cnl.pesquisar_localidade('843644', '8100')

    # Mossoró/RN - Mesmo estado
    cnl.pesquisar_localidade('843315', '4768')

    # São Paulo/SP - Outro estado
    cnl.pesquisar_localidade('113124', '5100')

inicio = datetime.now()
quantidade = 100
for i in range(quantidade):
    teste(cnl)

fim = datetime.now()
print 'Testes (%s)' % (3 * quantidade)
print 'Tempo de execução -->', fim - inicio
