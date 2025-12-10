import pyodbc
from typing import Optional

SERVER = 'mednat.ieeta.pt\\SQLSERVER,8101'  
DATABASE = 'p2g4'
USERNAME = 'p2g4' 
PASSWORD = 'Sim@oxuta2025'

ODBC_DRIVER = '{ODBC Driver 17 for SQL Server}' 

CONNECTION_STRING = (
    f'DRIVER={ODBC_DRIVER};'
    f'SERVER={SERVER};'
    f'DATABASE={DATABASE};'
    f'UID={USERNAME};'
    f'PWD={PASSWORD};'
)


def get_db_connection() -> Optional[pyodbc.Connection]:
    """
    Tenta estabelecer a conexão com o MSSQL usando as variáveis de ambiente.
    Retorna o objeto de conexão (pyodbc.Connection) ou None em caso de falha.
    """
    try:
        cnxn = pyodbc.connect(CONNECTION_STRING)
        return cnxn
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"\n--- ERRO CRÍTICO DE CONEXÃO COM MSSQL ---")
        print(f"Falha na conexão! Verifique Firewall e Credenciais.")
        print(f"SQLSTATE: {sqlstate}")
        print(f"Detalhe: {ex.args[1]}")
        print("-------------------------------------------\n")
        return None