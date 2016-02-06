# -*- coding: utf-8 -*-
import io
import sqlite3


class OpenCNL(object):
    """
    Essa classe é responsável por consultar o banco de dados SQLite3 com os
    dados da ANATEL gerado pelo OpenCNLImporter.
    """

    def __init__(self, caminho_da_base, prefixo_de_referencia,
                 sufixo_de_referencia):
        """
        Lê o arquivo da base de um banco SQLite3, previamente importado.
        Realiza uma pesquisa pelo prefixo de referência e salva o número para
        futuras comparações (centro de custo), caso ele tenha sido especificado.
        """
        try:
            self.conn = sqlite3.connect(caminho_da_base)
        except Exception:
            raise ErroAoConectarComBancoDeDados

        self.localidade_de_referencia = self._buscar_localidade(
            prefixo_de_referencia, sufixo_de_referencia)

    def buscar_localidade(self, prefixo, sufixo, prefixo_de_referencia=None,
                          sufixo_de_referencia=None):
        """
        Procura pelo prefixo de um número na base e retorna a tarifação, que
        pode ser dos tipos: VC1, VC2 e VC3. Por padrão utiliza o centro de custo
        definido na inicialização da classe, caso novos prefixo e sufixo não
        tenham sido definidos.
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

        # Buscar localidade para comparação.
        localidade = self._buscar_localidade(prefixo, sufixo)

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
        try:
            c = self.conn.cursor()
            localidade = c.execute("""
                SELECT * FROM open_cnl
                WHERE prefixo = ?
                AND CAST(numero_da_faixa_inicial as INTEGER) <= ?
                AND CAST(numero_da_faixa_final as INTEGER) >= ?;
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
