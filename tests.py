# -*- coding: utf-8 -*-
import unittest
from datetime import datetime
from open_cnl.open_cnl import OpenCNL

caminho_da_base = 'CE_F_130250.TXT'
prefixo_natal = '843211' # Prefeitura Municipal de Natal/RN
prefixo_parnamirim = '843644' # Prefeitura Municipal de Parnamirim/RN
prefixo_mossoro = '843315' # Prefeitura Municipal de Mossoró/RN
prefixo_sao_paulo = '113124' # Prefeitura Municipal de São Paulo/SP

class TestOpenCNL(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print 'Carregando base...'
        inicio = datetime.now()
        cls.cnl = OpenCNL(caminho_da_base, prefixo_natal)
        fim = datetime.now()
        print 'Base carregada em %s' % (fim - inicio)

    def test_vc1(self):
        # Natal/RN -> Parnamirim/RN - Área conurbada - VC1
        tarifa = self.cnl.buscar_prefixo(prefixo_parnamirim)
        self.assertEqual(tarifa, 'VC1')

    def test_vc2(self):
        # Natal/RN -> Mossoró/RN - Mesmo estado - VC2
        tarifa = self.cnl.buscar_prefixo(prefixo_mossoro)
        self.assertEqual(tarifa, 'VC2')

    def test_vc3(self):
        # Natal/RN -> São Paulo/SP - Outro estado - VC3
        tarifa = self.cnl.buscar_prefixo(prefixo_sao_paulo)
        self.assertEqual(tarifa, 'VC3')

    def test_vc2_outro_prefixo(self):
        # Mossoró/RN -> Parnamirim/RN - Mesmo estado - VC2
        tarifa = self.cnl.buscar_prefixo(prefixo_parnamirim, prefixo_mossoro)
        self.assertEqual(tarifa, 'VC2')

if __name__ == '__main__':
    unittest.main()
