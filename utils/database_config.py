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

