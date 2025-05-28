# db_utils.py
# Este arquivo contém funções utilitárias para interagir com o banco de dados.

import mysql.connector
from mysql.connector import errorcode
from db_config import DB_CONFIG # Importa as configurações do banco

def conectar_db():
    """
    Estabelece uma conexão com o banco de dados MySQL.

    Returns:
        mysql.connector.connection_cext.CMySQLConnection or None:
        Objeto de conexão se sucesso, None caso contrário.
    """
    try:
        conexao = mysql.connector.connect(**DB_CONFIG)
        return conexao
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erro de acesso (db_utils): Usuário ou senha do banco incorretos.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"Banco de dados '{DB_CONFIG.get('database', 'N/A')}' não existe (db_utils).")
        else:
            print(f"Erro ao conectar ao MySQL (db_utils): {err}")
        return None

def executar_query(conexao, query, params=None, commit=False, fetch_one=False, fetch_all=False):
    """
    Executa uma query SQL no banco de dados.

    Args:
        conexao: Objeto de conexão com o banco.
        query (str): A query SQL a ser executada.
        params (tuple, optional): Parâmetros para a query. Defaults to None.
        commit (bool, optional): True para realizar commit (INSERT, UPDATE, DELETE). Defaults to False.
        fetch_one (bool, optional): True para buscar um único resultado (SELECT). Defaults to False.
        fetch_all (bool, optional): True para buscar todos os resultados (SELECT). Defaults to False.

    Returns:
        int or dict or list or None:
        - ID da linha inserida (para INSERT com commit=True e lastrowid).
        - Dicionário (para fetch_one=True).
        - Lista de dicionários (para fetch_all=True).
        - rowcount (para UPDATE/DELETE com commit=True).
        - None se a query não retorna resultado (e não é commit), ou em caso de erro.
    """
    if conexao is None or not conexao.is_connected():
        print("Erro: Conexão com o banco de dados não está ativa.")
        return None

    cursor = None
    try:
        # Usar dictionary=True para que os resultados sejam dicionários (acesso por nome da coluna)
        cursor = conexao.cursor(dictionary=True)
        cursor.execute(query, params)

        if commit:
            conexao.commit()
            # Para INSERT, retorna o ID da última linha inserida
            if query.strip().upper().startswith("INSERT"):
                return cursor.lastrowid
            # Para UPDATE/DELETE, retorna o número de linhas afetadas
            return cursor.rowcount

        if fetch_one:
            return cursor.fetchone()
        if fetch_all:
            return cursor.fetchall()

        return None # Caso padrão (ex: SELECT sem fetch, ou DDL)

    except mysql.connector.Error as err:
        print(f"Erro ao executar query: {err}")
        # Em caso de erro em uma transação, realizar rollback
        if conexao and conexao.is_connected() and commit:
            try:
                conexao.rollback()
                print("Rollback realizado devido a erro.")
            except mysql.connector.Error as rollback_err:
                print(f"Erro durante o rollback: {rollback_err}")
        return None
    finally:
        if cursor:
            cursor.close()