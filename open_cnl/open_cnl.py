# -*- coding: utf-8 -*-
import sqlite3


class OpenCNL(object):
    """
    Biblioteca para ler e consultar banco de dados CNL (Código Nacional de
    Localidade) seguindo especificações da ANATEL (Agência Nacional de
    Telecomunicações).
    """

    def __init__(self, base_path, base_number):
        """
        Lê o arquivo da base e guarda na memória e salva o número de referência.
        """
        base_file = open(base_path, 'r')
        self.lines = list()
        for line in base_file.readlines():
            processed = self.process_line(line.decode('latin-1'))
            self.lines.append(processed)

        base_file.close()

        conn = sqlite3.connect(':memory:')
        c = conn.cursor()

    def process_complete_line(self, line):
        """
        Processa uma linha em um dicionário de acordo com as especificações.
        """
        processed_line = dict(
            sigla_uf=line[:2].strip(),
            sigla_cnl=line[2:6].strip(),
            codigo_cnl=line[6:11].strip(),
            nome_da_localidade=line[11:61].strip().replace('  ', ''),
            nome_do_municipio=line[61:111].strip(),
            codigo_da_area_de_tarifacao=line[111:116].strip(),
            prefixo=line[116:123].strip(),
            prestadora=line[123:153].strip(),
            numero_da_faixa_inicial=line[153:157].strip(),
            numero_da_faixa_final=line[157:161].strip(),
            latitude=self.process_coordinate(line[161:169].strip()),
            hemisferio=line[169:174].strip(),
            longitude=self.process_coordinate(line[174:182].strip()),
            sigla_cnl_da_area_local=line[182:186].strip()
        )
        return processed_line

    def process_incomplete_line(self, line):
        """
        Processa uma linha em um dicionário de acordo com as especificações.
        """
        processed_line = dict(
            sigla_uf=line[:2].strip(),
            sigla_cnl=line[2:6].strip(),
            codigo_cnl=line[6:11].strip(),
            nome_da_localidade=line[11:61].strip().replace('  ', ''),
            nome_do_municipio=line[61:111].strip(),
            codigo_da_area_de_tarifacao=line[111:116].strip(),
            prefixo=line[116:123].strip(),
            prestadora=line[123:153].strip(),
            numero_da_faixa_inicial=line[153:157].strip(),
            numero_da_faixa_final=line[157:161].strip(),
            sigla_cnl_da_area_local=line[161:164].strip()
        )
        return processed_line

    def process_line(self, line):
        """
        Processa uma linha em um dicionário de acordo com as especificações.
        """
        processed_line = dict(
            sigla_uf=line[:2].strip(),
            sigla_cnl=line[2:6].strip(),
            codigo_cnl=line[6:11].strip(),
            nome_da_localidade=line[11:61].strip().replace('  ', ''),
            nome_do_municipio=line[61:111].strip(),
            codigo_da_area_de_tarifacao=line[111:116].strip(),
            prefixo=line[116:123].strip(),
            prestadora=line[123:153].strip(),
            numero_da_faixa_inicial=line[153:157].strip(),
            numero_da_faixa_final=line[157:161].strip(),
            sigla_cnl_da_area_local=line[161:164].strip()
        )
        return processed_line

    def process_coordinate(self, coordinate):
        """
        Latitude e Longitude foram alterados para o formato GGMMSSCC, onde:
        GG = Grau,
        MM = Minuto,
        SS = Segundo e
        CC = Centésimos de segundo.
        Estamos ignorando centésimos de segundo e retornando GG.MMSS (float).
        """
        return float('%s.%s' % (coordinate[:2], coordinate[2:6]))

    def eval_number(self, target_number):
        """Searchs for target number in the base which is stored in memory."""
        pass
