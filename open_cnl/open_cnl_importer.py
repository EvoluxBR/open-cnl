# -*- coding: utf-8 -*-
import io
import os
import requests
import sqlite3
import sys
import zipfile


class OpenCNLImporter(object):
    """
    Essa classe é responsável por baixar uma base atualizada diretamente da
    ANATEL e convertê-la para um banco de dados SQLite3.
    """

    def __init__(self, caminho_da_base):
        """
        Armazena informações sobre o caminho da base e o caminho do banco.
        """
        self.caminho_da_base = caminho_da_base

    def baixar_base_atualizada(self):
        """
        Baixa a base de dados atualizada diretamente do site da ANATEL em
        formato ZIP, contendo a base (TXT) e um arquivo guia (DOC).
        """
        url = 'http://sistemas.anatel.gov.br/areaarea/N_Download/Tela.asp'
        form = {'varTIPO': 'CentralCNL', 'varCENTRAL': 'F', 'acao': 'c'}
        resposta = requests.get(url, form, stream=True, verify=False)
        arquivo_zip = io.BytesIO(resposta.content)
        return arquivo_zip

    def extrair_base_do_arquivo_zip(self, arquivo_zip):
        """
        Recebe um conjunto de bytes representando o arquivo ZIP disponibilizado
        pela ANATEL contendo a base (TXT) e um arquivo guia (DOC) e retorna o
        conteúdo do arquivo TXT.
        """
        with zipfile.ZipFile(arquivo_zip) as zf:
            for f in zf.namelist():
                if 'TXT' in f:
                    arquivo_txt = io.BytesIO(zf.read(f))

        return arquivo_txt

    def criar_banco_de_dados(self):
        self.conn = sqlite3.connect(self.caminho_da_base)
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

        c.execute("""
            CREATE INDEX `ix_localidade` ON `open_cnl` (
                prefixo, numero_da_faixa_inicial, numero_da_faixa_inicial
            );
        """)

    def gravar_linha_no_banco(self, linha_processada):
        """
        Grava uma linha processada no banco de dados SQLite3.
        """
        c = self.conn.cursor()
        c.execute("""
            INSERT INTO open_cnl VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            );
        """, linha_processada)

    def fechar_conexao_com_o_banco(self):
        """
        Grava alterações e fecha o banco de dados SQLite3.
        """
        self.conn.commit()
        self.conn.close()

    def importar_base(self):
        """
        Lê o arquivo da base e guarda no banco de dados SQLite3.
        """
        try:
            self.criar_banco_de_dados()
        except Exception:
            raise ErroAoCriarBancoDeDados

        try:
            arquivo_zip = self.baixar_base_atualizada()
        except Exception:
            raise ErroAoBaixarBaseDaANATEL

        try:
            arquivo_txt = self.extrair_base_do_arquivo_zip(arquivo_zip)
        except Exception:
            raise ErroAoExtrairBaseDaANATEL

        for linha in arquivo_txt.readlines():
            try:
                linha_processada = self.processar_linha(linha)
            except Exception:
                raise ErroAoProcessarBaseDaANATEL

            try:
                self.gravar_linha_no_banco(linha_processada)
            except Exception:
                raise ErroAoInserirDadosNoBanco

        self.fechar_conexao_com_o_banco()

    def processar_linha(self, linha):
        """
        Processa uma linha completa (com coordenadas) em uma tupla de acordo com
        as especificações.
        """
        linha = linha.decode('latin-1')
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
        )

        if len(linha) > 167:
            # Linha completa com corrdenadas
            linha_processada = linha_processada + (
                self.processar_coordenada(linha[161:169].strip()), # latitude
                linha[169:174].strip(), # hemisferio
                self.processar_coordenada(linha[174:182].strip()), # longitude
                linha[182:186].strip() # sigla_cnl_da_area_local
            )
        else:
            # Linha incompleta sem coordenadas
            linha_processada = linha_processada + (
                '', '', '', # latitude, hemisferio, longitude
                linha[161:164].strip() # sigla_cnl_da_area_local
            )

        return linha_processada

    def processar_coordenada(self, coordenada):
        """
        Latitude e Longitude foram alterados para o formato GGMMSSCC, onde:
        GG = Grau,
        MM = Minuto,
        SS = Segundo e
        CC = Centésimos de segundo.
        """
        # TODO: Transformar em um formato mais portável.
        return coordenada[:8]


class ErroAoCriarBancoDeDados(Exception):
    pass


class ErroAoBaixarBaseDaANATEL(Exception):
    pass


class ErroAoExtrairBaseDaANATEL(Exception):
    pass


class ErroAoProcessarBaseDaANATEL(Exception):
    pass


class ErroAoInserirDadosNoBanco(Exception):
    pass


def main(argv):
    if not len(argv) == 2:
        print('Utilização: open_cnl_importer <destino.sqlite3>')
        return

    arquivo_de_destino = argv[1]
    if os.path.exists(arquivo_de_destino):
        print('Arquivo de destino já existe: %s' % arquivo_de_destino)
        return

    open_cnl_importer = OpenCNLImporter(arquivo_de_destino)
    try:
        open_cnl_importer.importar_base()
    except ErroAoCriarBancoDeDados:
        print('Erro ao criar o banco de dados')
    except ErroAoBaixarBaseDaANATEL:
        print('Erro ao baixar a base da ANATEL')
    except ErroAoExtrairBaseDaANATEL:
        print('Erro ao extrair a base da ANATEL')
    except ErroAoProcessarBaseDaANATEL:
        print('Erro ao processar a base da ANATEL')
    except ErroAoInserirDadosNoBanco:
        print('Erro ao inserir dados no banco')

if __name__ == "__main__":
    main(sys.argv)
