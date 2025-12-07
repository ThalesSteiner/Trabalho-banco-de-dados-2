"""
Cria as tabelas normalizadas (schema n) e popula a partir de o.Tabelona.
Use as variáveis de ambiente DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME.
"""
import argparse
import os
from pathlib import Path

from loguru import logger

import utils.database_config as db_config


def create_normalized_tables(ddl_path: str) -> bool:
    """
    Cria o schema n e as tabelas normalizadas conforme o arquivo SQL fornecido.
    """
    conn = db_config.get_connection()
    if not conn:
        logger.error("Erro ao conectar ao banco de dados")
        return False

    try:
        ddl_file_path = Path(ddl_path)
        if not ddl_file_path.exists():
            raise FileNotFoundError(f"DDL não encontrado em {ddl_file_path}")

        with open(ddl_file_path, "r", encoding="utf-8") as ddl_file:
            ddl_sql = ddl_file.read()

        with conn.cursor() as cursor:
            cursor.execute(ddl_sql)
        conn.commit()
        logger.info("Tabelas normalizadas criadas com sucesso")
        return True
    except Exception as e:
        conn.rollback()
        logger.error(f"Erro ao criar tabelas normalizadas: {e}")
        return False
    finally:
        conn.close()


def populate_normalized_tables(dml_path: str) -> bool:
    """
    Popula as tabelas normalizadas a partir de o.Tabelona usando o arquivo DML fornecido.
    """
    conn = db_config.get_connection()
    if not conn:
        logger.error("Erro ao conectar ao banco de dados")
        return False

    try:
        dml_file_path = Path(dml_path)
        if not dml_file_path.exists():
            raise FileNotFoundError(f"DML não encontrado em {dml_file_path}")

        with open(dml_file_path, "r", encoding="utf-8") as dml_file:
            dml_sql = dml_file.read()

        with conn.cursor() as cursor:
            cursor.execute(dml_sql)
        conn.commit()
        logger.info("Tabelas normalizadas populadas com sucesso")
        return True
    except Exception as e:
        conn.rollback()
        logger.error(f"Erro ao popular tabelas normalizadas: {e}")
        return False
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="Cria o schema n e popula as tabelas normalizadas a partir de o.Tabelona."
    )
    parser.add_argument(
        "--ddl-path",
        default=os.path.join("scripts", "sql", "DDL1.sql"),
        help="Caminho do DDL .sql das tabelas normalizadas (default: scripts/sql/DDL1.sql)",
    )
    parser.add_argument(
        "--dml-path",
        default=os.path.join("scripts", "sql", "DML1.sql"),
        help="Caminho do DML .sql para popular as tabelas (default: scripts/sql/DML1.sql)",
    )
    parser.add_argument(
        "--create-only",
        action="store_true",
        help="Somente cria as tabelas, sem popular.",
    )
    args = parser.parse_args()

    created = create_normalized_tables(args.ddl_path)
    if not created or args.create_only:
        return

    populate_normalized_tables(args.dml_path)


if __name__ == "__main__":
    main()

