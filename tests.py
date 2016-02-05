# -*- coding: utf-8 -*-
import os
import unittest
from datetime import datetime
from open_cnl.open_cnl import OpenCNL, OpenCNLImporter

caminho_da_base_original = 'base.txt'
caminho_da_base = 'banco.sqlite3'

# Prefeitura Municipal de Natal/RN
prefixo_natal, sufixo_natal = '843211', '8243'

# Prefeitura Municipal de Parnamirim/RN
prefixo_parnamirim, sufixo_parnamirim = '843644', '8100'

# Prefeitura Municipal de Mossoró/RN
prefixo_mossoro, sufixo_mossoro = '843315', '4768'

# Prefeitura Municipal de São Paulo/SP
prefixo_sao_paulo, sufixo_sao_paulo = '113124', '5100'

class TestOpenCNL(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('Carregando base...')
        inicio = datetime.now()

        # Removendo base caso ela já exista (SQLite3, não a original em TXT)
        try:
            os.remove(caminho_da_base)
        except OSError:
            print('Não foi possível remover o banco de dados.')
            print('Provavelmente ele não existe.')

        # Importando a base (só precisa ser feito uma vez)
        cnl_importer = OpenCNLImporter(
            caminho_da_base_original, caminho_da_base)
        cnl_importer.importar_base()

        # Iniciando Open CNL
        cls.cnl = OpenCNL(caminho_da_base, prefixo_natal, sufixo_natal)
        fim = datetime.now()
        print('Base carregada em %s' % (fim - inicio))

    def test_vc1(self):
        # Natal/RN -> Parnamirim/RN - Área conurbada - VC1
        tarifa = self.cnl.buscar_localidade(
            prefixo_parnamirim, sufixo_parnamirim)
        self.assertEqual(tarifa, 'VC1')

    def test_vc2(self):
        # Natal/RN -> Mossoró/RN - Mesmo estado - VC2
        tarifa = self.cnl.buscar_localidade(prefixo_mossoro, sufixo_mossoro)
        self.assertEqual(tarifa, 'VC2')

    def test_vc3(self):
        # Natal/RN -> São Paulo/SP - Outro estado - VC3
        tarifa = self.cnl.buscar_localidade(prefixo_sao_paulo, sufixo_sao_paulo)
        self.assertEqual(tarifa, 'VC3')

    def test_vc2_outro_prefixo(self):
        # Mossoró/RN -> Parnamirim/RN - Mesmo estado - VC2
        tarifa = self.cnl.buscar_localidade(
            prefixo_parnamirim, sufixo_parnamirim,
            prefixo_mossoro, sufixo_mossoro)
        self.assertEqual(tarifa, 'VC2')

if __name__ == '__main__':
    unittest.main()
