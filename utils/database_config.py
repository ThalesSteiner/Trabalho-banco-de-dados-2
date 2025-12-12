"""
Configuração de conexão com o banco de dados PostgreSQL
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import psycopg2

DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'banco_dados')
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_connection():
    """
    Retorna uma conexão direta usando psycopg2.
    """
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        return None

def fetch_table(query):
    """
    Consulta uma tabela e retorna os resultados.
    Exemplo de uso:
        fetch_table("SELECT * FROM minha_tabela")
    """
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            return results
    except Exception as e:
        print(f"Erro ao buscar tabela: {e}")
        return None
    finally:
        conn.close()

def execute_procedure(query):
    """
    Executa uma stored procedure no banco de dados.
    Exemplo de uso:
        execute_procedure("SELECT * FROM minha_tabela")
    """
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()
            if cursor.description:
                result = cursor.fetchall()
                return result
            return None
    except Exception as e:
        print(f"Erro ao executar procedure: {e}")
        return None
    finally:
        conn.close()

def execute_function(query):
    """
    Executa uma função do banco de dados e retorna o resultado.
    Exemplo de uso:
        execute_function('SELECT * FROM minha_tabela')
    """
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cursor:
            sql = f"{query};"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(f"Erro ao executar função: {e}")
        return None
    finally:
        conn.close()

def execute_multiple_statements(sql_text: str, cursor) -> None:
    """
    GAMBIARRA PARA EXECUTAR MULTIPLOS COMANDOS SQL SEPARADOS POR PONTO E VÍRGULA.
    PARA QUE O FLUXO DE DADOS POSSA SER POPULADO VIA ARQUIVO PRECISAMOS ADAPTAR PARA QUE A QUERY POSSA SER LIDA E INSERIDA CORRETAMENTE.
    """
    sql_cleaned = sql_text
    commands = []
    current_command = []
    i = 0
    in_dollar_quote = False
    dollar_tag = None
    
    while i < len(sql_cleaned):
        char = sql_cleaned[i]
        
        if char == '$' and not in_dollar_quote:
            tag_start = i
            i += 1
            while i < len(sql_cleaned) and sql_cleaned[i] != '$':
                i += 1
            if i < len(sql_cleaned):
                i += 1
                dollar_tag = sql_cleaned[tag_start:i]
                in_dollar_quote = True
                current_command.append(dollar_tag)
                continue
        
        # Detecta fim de dollar-quoted string
        elif char == '$' and in_dollar_quote:
            tag_start = i
            j = i + 1
            while j < len(sql_cleaned) and sql_cleaned[j] != '$':
                j += 1
            if j < len(sql_cleaned):
                j += 1
                closing_tag = sql_cleaned[tag_start:j]
                if closing_tag == dollar_tag:
                    current_command.append(closing_tag)
                    in_dollar_quote = False
                    dollar_tag = None
                    i = j
                    continue
            
            current_command.append(char)
            i += 1
            continue
        
        current_command.append(char)
        
        if not in_dollar_quote and char == ';':
            command = ''.join(current_command).strip()
            if command:
                commands.append(command)
            current_command = []
        
        i += 1
    
    if current_command:
        command = ''.join(current_command).strip()
        if command:
            commands.append(command)
    
    for command in commands:
        if command:
            cursor.execute(command)


def test_connection():
    """
    Testa a conexão com o banco de dados
    """
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print("Conexão bem-sucedida!")
            print(f"Versão do PostgreSQL: {version}")
            return True
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    print("Testando conexão com o banco de dados...")
    test_connection()

