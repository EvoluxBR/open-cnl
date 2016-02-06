# -*- coding: utf-8 -*-
import unittest
from open_cnl.open_cnl import (OpenCNL, LocalidadeNaoEncontrada,
                               ErroAoLerDoBancoDeDados)

caminho_da_base = './cnl_anatel.sqlite3'

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
        # Iniciando Open CNL
        cls.cnl = OpenCNL(caminho_da_base, prefixo_natal, sufixo_natal)

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

    def test_localidade_nao_encontrada(self):
        with self.assertRaises(LocalidadeNaoEncontrada):
            tarifa = self.cnl.buscar_localidade('9977777', '545454')

    def test_erro_ao_ler_do_banco_de_dados(self):
        with self.assertRaises(ErroAoLerDoBancoDeDados):
            OpenCNL('nao_existe.sqlite3', prefixo_natal, sufixo_natal)


if __name__ == '__main__':
    unittest.main()
