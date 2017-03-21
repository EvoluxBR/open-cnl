# -*- coding: utf-8 -*-
import unittest
import json
from open_cnl.open_cnl import OpenCNL, ErroAoLerDoBancoDeDados

caminho_da_base = './cnl_anatel.sqlite3'

class TestOpenCNL(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Iniciando Open CNL
        cls.cnl = OpenCNL(caminho_da_base)

    def teste_natal_rn(self):
        # Prefeitura Municipal de Natal/RN - (84) 3211-8243
        localidade = self.cnl.pesquisar_localidade('843211', '8243')
        self.assertEqual(localidade, {
            'prestadora': u'TELEMAR NORTE LESTE S.A.',
            'nome_da_localidade': u'NATAL',
            'hemisferio': u'S',
            'numero_da_faixa_final': u'8999',
            'sigla_cnl_da_area_local': u'NTL',
            'numero_da_faixa_inicial': u'8000',
            'longitude': u'35123203',
            'prefixo': u'843211',
            'codigo_da_area_de_tarifacao': u'842',
            'latitude': u'5474199',
            'codigo_cnl': u'84000',
            'sigla_uf': u'RN',
            'nome_do_municipio': u'NATAL',
            'sigla_cnl': u'NTL'
        })

    def teste_parnamirim_rn(self):
        # Prefeitura Municipal de Parnamirim/RN - (84) 3644-8100
        localidade = self.cnl.pesquisar_localidade('843644', '8100')
        self.assertEqual(localidade, {
            'prestadora': u'TELEMAR NORTE LESTE S.A.',
            'nome_da_localidade': u'PARNAMIRIM',
            'hemisferio': u'S',
            'numero_da_faixa_final': u'8999',
            'sigla_cnl_da_area_local': u'NTL',
            'numero_da_faixa_inicial': u'8000',
            'longitude': u'35154607',
            'prefixo': u'843644',
            'codigo_da_area_de_tarifacao': u'842',
            'latitude': u'5545608',
            'codigo_cnl': u'84024',
            'sigla_uf': u'RN',
            'nome_do_municipio': u'PARNAMIRIM',
            'sigla_cnl': u'PWM'
        })

    def teste_mossoro_rn(self):
        # Prefeitura Municipal de Mossoró/RN - (84) 3315-4768
        localidade = self.cnl.pesquisar_localidade('843315', '4768')
        self.assertEqual(localidade, {
            'prestadora': u'TELEMAR NORTE LESTE S.A.',
            'nome_da_localidade': u'MOSSOR\xd3',
            'hemisferio': u'S',
            'numero_da_faixa_final': u'4999',
            'sigla_cnl_da_area_local': u'MRO',
            'numero_da_faixa_inicial': u'4000',
            'longitude': u'37205064',
            'prefixo': u'843315',
            'codigo_da_area_de_tarifacao': u'843',
            'latitude': u'5110146',
            'codigo_cnl': u'84049',
            'sigla_uf': u'RN',
            'nome_do_municipio': u'MOSSOR\xd3',
            'sigla_cnl': u'MRO'
        })

    def teste_sao_paulo_sp(self):
        # Prefeitura Municipal de São Paulo/SP - (11) 3124-5100
        localidade = self.cnl.pesquisar_localidade('113124', '5100')
        self.assertEqual(localidade, {
            'prestadora': u'TELEF\xd4NICA-TELESP',
            'nome_da_localidade': u'S\xc3O PAULO',
            'hemisferio': u'S',
            'numero_da_faixa_final': u'5999',
            'sigla_cnl_da_area_local': u'SPO',
            'numero_da_faixa_inicial': u'5000',
            'longitude': u'46380203',
            'prefixo': u'113124',
            'codigo_da_area_de_tarifacao': u'011',
            'latitude': u'23330143',
            'codigo_cnl': u'11000',
            'sigla_uf': u'SP',
            'nome_do_municipio': u'S\xc3O PAULO',
            'sigla_cnl': u'SPO'
        })

    def teste_localidade_json(self):
        # Prefeitura Municipal de Natal/RN - (84) 3211-8243
        localidade = self.cnl.pesquisar_localidade('843211', '8243', True)
        localidade = json.loads(localidade)
        self.assertEqual(localidade, {
            'prestadora': u'TELEMAR NORTE LESTE S.A.',
            'nome_da_localidade': u'NATAL',
            'hemisferio': u'S',
            'numero_da_faixa_final': u'8999',
            'sigla_cnl_da_area_local': u'NTL',
            'numero_da_faixa_inicial': u'8000',
            'longitude': u'35123203',
            'prefixo': u'843211',
            'codigo_da_area_de_tarifacao': u'842',
            'latitude': u'5474199',
            'codigo_cnl': u'84000',
            'sigla_uf': u'RN',
            'nome_do_municipio': u'NATAL',
            'sigla_cnl': u'NTL'
        })

    def teste_localidade_nao_encontrada(self):
        localidade = self.cnl.pesquisar_localidade('9977777', '545454')
        self.assertEqual(localidade, None)

    def teste_erro_ao_ler_do_banco_de_dados(self):
        with self.assertRaises(ErroAoLerDoBancoDeDados):
            cnl = OpenCNL('nao_existe.sqlite3')
            cnl.pesquisar_localidade('9977777', '545454')


if __name__ == '__main__':
    unittest.main()
