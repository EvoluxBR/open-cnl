# -*- coding: utf-8 -*-
import sqlite3
import io


class OpenCNL(object):
    """
    Biblioteca para ler e consultar banco de dados CNL (Código Nacional de
    Localidade) seguindo especificações da ANATEL (Agência Nacional de
    Telecomunicações).
    """

    def __init__(self, caminho_da_base, prefixo_de_referencia,
                 sufixo_de_referencia):
        """
        Lê o arquivo da base de um banco SQLite3, previamente importado.
        Realiza uma pesquisa pelo prefixo de referência e salva o número para
        futuras comparações, caso ele tenha sido especificado.
        """
        self.conn = sqlite3.connect(caminho_da_base)
        self.localidade_de_referencia = self._buscar_localidade(
            prefixo_de_referencia, sufixo_de_referencia)

    def buscar_localidade(self, prefixo, sufixo, prefixo_de_referencia=None,
                          sufixo_de_referencia=None):
        """
        Procura pelo prefixo de um número na base e retorna a tarifação, que
        pode ser dos tipos: VC1, VC2 e VC3.
        """
        if not prefixo_de_referencia or not sufixo_de_referencia:
            # Utilizar localidade de referência especificado na inicialização
            # da classe.
            localidade_de_referencia = self.localidade_de_referencia
        else:
            # Utilizar localidade de referência especificado na chamada do
            # método.
            localidade_de_referencia = self._buscar_localidade(
                prefixo_de_referencia, sufixo_de_referencia)

        if not localidade_de_referencia:
            return None

        # Buscar localidade para comparação.
        localidade = self._buscar_localidade(prefixo, sufixo)
        if not localidade:
            return None

        if localidade[5] == localidade_de_referencia[5]:
            # Código Nacional de Localidade igual em ambas as localidades.
            return 'VC1'
        elif localidade[5][0] == localidade_de_referencia[5][0]:
            # Código Nacional de Localidade diferente entre as localidades, mas
            # o primeiro dígito é comum às duas.
            return 'VC2'
        else:
            # Código Nacional de Localidade diferente entre as localidades.
            return 'VC3'

    def _buscar_localidade(self, prefixo, sufixo):
        """Função de busca auxiliar para prefixo no banco de dados."""
        c = self.conn.cursor()
        localidade = c.execute("""
            SELECT * FROM open_cnl
            WHERE prefixo = ?
            AND CAST(numero_da_faixa_inicial as INTEGER) <= ?
            AND CAST(numero_da_faixa_final as INTEGER) >= ?;
        """, (prefixo, int(sufixo), int(sufixo))).fetchone()
        return localidade


class OpenCNLImporter(object):
    """
    Biblioteca para ler e consultar banco de dados CNL (Código Nacional de
    Localidade) seguindo especificações da ANATEL (Agência Nacional de
    Telecomunicações).
    """

    def __init__(self, caminho_da_base, caminho_do_banco):
        """
        Armazena informações sobre o caminho da base e o caminho do banco.
        """
        self.caminho_da_base = caminho_da_base
        self.caminho_do_banco = caminho_do_banco

    def importar_base(self):
        """
        Lê o arquivo da base e guarda no banco de dados SQLite3.
        """
        self.conn = sqlite3.connect(self.caminho_do_banco)
        c = self.conn.cursor()
        try:
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
        except Exception:
            print('Ocorreu um erro ao importar a base.')
            print('Verifique se o banco já existe.')
            self.conn.close()
            return

        arquivo_da_base = io.open(self.caminho_da_base, 'r', encoding='latin-1')
        for linha in arquivo_da_base.readlines():
            linha_processada = self.processar_linha(linha)
            c.execute("""
                INSERT INTO open_cnl VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                );
            """, linha_processada)

        arquivo_da_base.close()
        self.conn.commit()
        self.conn.close()

    def processar_linha(self, linha):
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
        Estamos ignorando centésimos de segundo e retornando GGMMSS.
        """
        # FIXME: Transformar em graus com os dados recebidos.
        return coordenada[:6]
