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
        self.conn = sqlite3.connect(':memory:')
        c = self.conn.cursor()
        c.execute("""
            CREATE TABLE `open_cnl` (
                sigla_uf TEXT,
                sigla_cnl TEXT,
                codigo_cnl TEXT,
                nome_da_localidade TEXT,
                nome_do_municipio TEXT,
                codigo_da_area_de_tarifacao TEXT,
                prefixo TEXT,
                prestadora TEXT,
                numero_da_faixa_inicial TEXT,
                numero_da_faixa_final TEXT,
                latitude TEXT,
                hemisferio TEXT,
                longitude TEXT,
                sigla_cnl_da_area_local TEXT
            );
        """)

        base_file = open(base_path, 'r')
        for line in base_file.readlines():
            processed_line = self.process_line(line.decode('latin-1'))
            c.execute("""
                INSERT INTO open_cnl VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                );
            """, processed_line)

        base_file.close()
        prefix = base_number[:-4]
        self.number_info = c.execute(
            """SELECT * FROM open_cnl WHERE prefixo = ?;""", (prefix,)).fetchone()

    def process_complete_line(self, line):
        """
        Processa uma linha em uma tupla de acordo com as especificações.
        """
        processed_line = (
            line[:2].strip(), # sigla_uf
            line[2:6].strip(), # sigla_cnl
            line[6:11].strip(), # codigo_cnl
            line[11:61].strip().replace('  ', ''), # nome_da_localidade
            line[61:111].strip(), # nome_do_municipio
            line[111:116].strip(), # codigo_da_area_de_tarifacao
            line[116:123].strip(), # prefixo
            line[123:153].strip(), # prestadora
            line[153:157].strip(), # numero_da_faixa_inicial
            line[157:161].strip(), # numero_da_faixa_final
            self.process_coordinate(line[161:169].strip()), # latitude
            line[169:174].strip(), # hemisferio
            self.process_coordinate(line[174:182].strip()), # longitude
            line[182:186].strip() # sigla_cnl_da_area_local
        )
        return processed_line

    def process_incomplete_line(self, line):
        """
        Processa uma linha em uma tupla de acordo com as especificações.
        """
        processed_line = (
            line[:2].strip(), # sigla_uf
            line[2:6].strip(), # sigla_cnl
            line[6:11].strip(), # codigo_cnl
            line[11:61].strip().replace('  ', ''), # nome_da_localidade
            line[61:111].strip(), # nome_do_municipio
            line[111:116].strip(), # codigo_da_area_de_tarifacao
            line[116:123].strip(), # prefixo
            line[123:153].strip(), # prestadora
            line[153:157].strip(), # numero_da_faixa_inicial
            line[157:161].strip(), # numero_da_faixa_final
            '', '', '', # latitude, hemisferio, longitude
            line[161:164].strip() # sigla_cnl_da_area_local
        )
        return processed_line

    def process_line(self, line):
        """
        Verifica o tamanho da linha e encaminha para o método adequado.
        """
        if len(line) > 167:
            return self.process_complete_line(line)
        else:
            return self.process_incomplete_line(line)

    def process_coordinate(self, coordinate):
        """
        Latitude e Longitude foram alterados para o formato GGMMSSCC, onde:
        GG = Grau,
        MM = Minuto,
        SS = Segundo e
        CC = Centésimos de segundo.
        Estamos ignorando centésimos de segundo e retornando GG.MMSS (float).
        """
        return '%s.%s' % (coordinate[:2], coordinate[2:6])

    def eval_number(self, target_number):
        """Searchs for target number in the base which is stored in memory."""
        prefix = target_number[:-4]
        c = self.conn.cursor()

        number_info = c.execute(
            """SELECT * FROM open_cnl WHERE prefixo = ?;""", (prefix,)).fetchone()

        if number_info[5] == self.number_info[5]:
            return 'VC1'
        elif number_info[5][0] == self.number_info[5][0]:
            return 'VC2'
        else:
            return 'VC3'
