# -*- coding: utf-8 -*-
import io
import json
import sqlite3


class OpenCNL(object):
    """
    Essa classe é responsável por consultar o banco de dados SQLite3 com os
    dados da ANATEL gerado pelo OpenCNLImporter.
    """

    def __init__(self, caminho_da_base):
        """
        Lê o arquivo da base de um banco SQLite3, previamente importado.
        """
        try:
            self.conn = sqlite3.connect(caminho_da_base)
        except Exception:
            raise ErroAoConectarComBancoDeDados

    def pesquisar_localidade(self, prefixo, sufixo, as_json=False):
        """
        Procura pelo por um número cujo prefixo e o sufixo (com DDD) esteja na
        base e retorna os resultados encontrados.
        """

        # Pesquisa a localidade no banco de dados.
        try:
            localidade = self._pesquisar_localidade(prefixo, sufixo)
        except LocalidadeNaoEncontrada:
            if as_json:
                # Se a opção estiver ativa, retornar como JSON
                return json.dumps(None)

            return None

        localidade = dict(
            sigla_uf=localidade[0],
            sigla_cnl=localidade[1],
            codigo_cnl=localidade[2],
            nome_da_localidade=localidade[3],
            nome_do_municipio=localidade[4],
            codigo_da_area_de_tarifacao=localidade[5],
            prefixo=localidade[6],
            prestadora=localidade[7],
            numero_da_faixa_inicial=localidade[8],
            numero_da_faixa_final=localidade[9],
            latitude=localidade[10],
            hemisferio=localidade[11],
            longitude=localidade[12],
            sigla_cnl_da_area_local=localidade[13],
        )

        if as_json:
            # Se a opção estiver ativa, retornar como JSON
            return json.dumps(localidade)

        return localidade

    def _pesquisar_localidade(self, prefixo, sufixo):
        """Função auxiliar para pesquisar número no banco de dados."""
        try:
            c = self.conn.cursor()
            localidade = c.execute("""
                SELECT
                    `sigla_uf`,
                    `sigla_cnl`,
                    `codigo_cnl`,
                    `nome_da_localidade`,
                    `nome_do_municipio`,
                    `codigo_da_area_de_tarifacao`,
                    `prefixo`,
                    `prestadora`,
                    `numero_da_faixa_inicial`,
                    `numero_da_faixa_final`,
                    `latitude`,
                    `hemisferio`,
                    `longitude`,
                    `sigla_cnl_da_area_local`
                FROM `open_cnl`
                WHERE `prefixo` = ?
                AND CAST(`numero_da_faixa_inicial` as INTEGER) <= ?
                AND CAST(`numero_da_faixa_final` as INTEGER) >= ?;
            """, (prefixo, int(sufixo), int(sufixo))).fetchone()
        except Exception:
            raise ErroAoLerDoBancoDeDados

        if not localidade:
            raise LocalidadeNaoEncontrada

        return localidade


class LocalidadeNaoEncontrada(Exception):
    pass


class ErroAoLerDoBancoDeDados(Exception):
    pass


class ErroAoConectarComBancoDeDados(Exception):
    pass
