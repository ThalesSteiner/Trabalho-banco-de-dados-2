"""
Script para criar uma tabela de teste no banco de dados PostgreSQL
"""
import utils.database_config as db_config

def create_test_table():
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        idade INTEGER,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    conn = db_config.get_connection()
    if not conn:
        print("Erro ao conectar ao banco de dados")
        return False
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(create_table_sql)
            conn.commit()
            print("Tabela 'usuarios' criada com sucesso!")
            return True
    except Exception as e:
        conn.rollback()
        print(f"Erro ao criar tabela: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    create_test_table()
