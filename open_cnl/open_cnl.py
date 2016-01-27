# -*- coding: utf-8 -*-
import sqlite3


class OpenCNL(object):
    """
    Biblioteca para ler e consultar banco de dados CNL (Código Nacional de
    Localidade) seguindo especificações da ANATEL (Agência Nacional de
    Telecomunicações).
    """

    def __init__(self, caminho_da_base, prefixo_de_referencia):
        """
        Lê o arquivo da base e guarda na memória. Realiza uma pesquisa pelo
        prefixo de referência e salva o número para futuras comparações, caso
        ele tenha sido especificado.
        """
        self.conn = sqlite3.connect(':memory:')
        # self.conn = sqlite3.connect('banco.db')
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

        arquivo_da_base = open(caminho_da_base, 'r')
        for linha in arquivo_da_base.readlines():
            linha_processada = self.processar_linha(linha.decode('latin-1'))
            c.execute("""
                INSERT INTO open_cnl VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                );
            """, linha_processada)

        arquivo_da_base.close()
        self.prefixo_de_referencia = c.execute(
            """SELECT * FROM open_cnl WHERE prefixo = ?;""",
            (prefixo_de_referencia,)).fetchone()

    def processar_linha_completa(self, linha):
        """
        Processa uma linha completa (com coordenadas) em uma tupla de acordo com
        as especificações.
        """
        linha_processada = (
            linha[:2].strip(), # sigla_uf
            linha[2:6].strip(), # sigla_cnl
            linha[6:11].strip(), # codigo_cnl
            linha[11:61].strip().replace('  ', ''), # nome_da_localidade
            linha[61:111].strip(), # nome_do_municipio
            linha[111:116].strip(), # codigo_da_area_de_tarifacao
            linha[116:123].strip(), # prefixo
            linha[123:153].strip(), # prestadora
            linha[153:157].strip(), # numero_da_faixa_inicial
            linha[157:161].strip(), # numero_da_faixa_final
            self.processar_coordenada(linha[161:169].strip()), # latitude
            linha[169:174].strip(), # hemisferio
            self.processar_coordenada(linha[174:182].strip()), # longitude
            linha[182:186].strip() # sigla_cnl_da_area_local
        )
        return linha_processada

    def processar_linha_incompleta(self, linha):
        """
        Processa uma linha incompleta (sem coordenadas) em uma tupla de acordo
        com as especificações.
        """
        linha_processada = (
            linha[:2].strip(), # sigla_uf
            linha[2:6].strip(), # sigla_cnl
            linha[6:11].strip(), # codigo_cnl
            linha[11:61].strip().replace('  ', ''), # nome_da_localidade
            linha[61:111].strip(), # nome_do_municipio
            linha[111:116].strip(), # codigo_da_area_de_tarifacao
            linha[116:123].strip(), # prefixo
            linha[123:153].strip(), # prestadora
            linha[153:157].strip(), # numero_da_faixa_inicial
            linha[157:161].strip(), # numero_da_faixa_final
            '', '', '', # latitude, hemisferio, longitude
            linha[161:164].strip() # sigla_cnl_da_area_local
        )
        return linha_processada

    def processar_linha(self, linha):
        """
        Verifica o tamanho da linha e encaminha para o método adequado.
        """
        if len(linha) > 167:
            return self.processar_linha_completa(linha)
        else:
            return self.processar_linha_incompleta(linha)

    def processar_coordenada(self, coordenada):
        """
        Latitude e Longitude foram alterados para o formato GGMMSSCC, onde:
        GG = Grau,
        MM = Minuto,
        SS = Segundo e
        CC = Centésimos de segundo.
        Estamos ignorando centésimos de segundo e retornando GG.MMSS (float).
        """
        return '%s.%s' % (coordenada[:2], coordenada[2:6])

    def buscar_prefixo(self, prefixo, prefixo_de_referencia=None):
        """
        Procura pelo prefixo de um número na base e retorna a tarifação, que
        pode ser dos tipos: VC1, VC2 e VC3.
        """
        c = self.conn.cursor()

        if not prefixo_de_referencia:
            # Utilizar prefixo de referência especificado na inicialização
            # da classe.
            prefixo_de_referencia = self.prefixo_de_referencia
        else:
            # Utilizar prefixo de referência especificado na chamada do método.
            prefixo_de_referencia = c.execute(
                """SELECT * FROM open_cnl WHERE prefixo = ?;""",
                (prefixo_de_referencia,)).fetchone()

        # Buscar prefixo para comparação.
        prefixo = c.execute(
            """SELECT * FROM open_cnl WHERE prefixo = ?;""",
            (prefixo,)).fetchone()

        if prefixo[5] == prefixo_de_referencia[5]:
            # Código Nacional de Localidade igual em ambos os prefixos.
            return 'VC1'
        elif prefixo[5][0] == prefixo_de_referencia[5][0]:
            # Código Nacional de Localidade diferente entre os prefixos, mas
            # o primeiro dígito é comum aos dois.
            return 'VC2'
        else:
            # Código Nacional de Localidade diferente entre os prefixos.
            return 'VC3'
