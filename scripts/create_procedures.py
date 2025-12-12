"""
Cria as procedures do banco de dados a partir dos arquivos SQL.
Use as variáveis de ambiente DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME.
"""
import argparse
import os
from pathlib import Path

from loguru import logger

import utils.database_config as db_config


def create_procedures(procedures_path: str) -> bool:
    """
    Cria as procedures a partir de um arquivo SQL.
    """
    conn = db_config.get_connection()
    if not conn:
        logger.error("Erro ao conectar ao banco de dados")
        return False

    try:
        procedures_file_path = Path(procedures_path)
        if not procedures_file_path.exists():
            raise FileNotFoundError(f"Arquivo de procedures não encontrado em {procedures_file_path}")

        with open(procedures_file_path, "r", encoding="utf-8") as procedures_file:
            procedures_sql = procedures_file.read()

        with conn.cursor() as cursor:
            db_config.execute_multiple_statements(procedures_sql, cursor)
        conn.commit()
        logger.info("Procedures criadas com sucesso")
        return True
    except Exception as e:
        conn.rollback()
        logger.error(f"Erro ao criar procedures: {e}")
        return False
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="Cria as procedures do banco de dados a partir do arquivo SQL."
    )
    parser.add_argument(
        "--procedures-path",
        default=os.path.join("objetos", "Procedure.sql"),
        help="Caminho do arquivo SQL com as procedures (default: objetos/Procedure.sql)",
    )
    args = parser.parse_args()

    create_procedures(args.procedures_path)


if __name__ == "__main__":
    main()

