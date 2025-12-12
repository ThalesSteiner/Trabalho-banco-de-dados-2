"""
Cria as tabelas do Data Warehouse (schema dw) e popula a partir das tabelas normalizadas (schema n).
Use as variáveis de ambiente DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME.
"""
import argparse
import os
from pathlib import Path

from loguru import logger

import utils.database_config as db_config


def create_dw_tables(ddl_path: str) -> bool:
    """
    Cria o schema dw e as tabelas do Data Warehouse conforme o arquivo SQL fornecido.
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
            db_config.execute_multiple_statements(ddl_sql, cursor)
        conn.commit()
        logger.info("Tabelas do Data Warehouse criadas com sucesso")
        return True
    except Exception as e:
        conn.rollback()
        logger.error(f"Erro ao criar tabelas do Data Warehouse: {e}")
        return False
    finally:
        conn.close()


def populate_dw_tables(dml_path: str) -> bool:
    """
    Popula as tabelas do Data Warehouse a partir das tabelas normalizadas usando o arquivo DML fornecido.
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
            db_config.execute_multiple_statements(dml_sql, cursor)
        conn.commit()
        logger.info("Tabelas do Data Warehouse populadas com sucesso")
        return True
    except Exception as e:
        conn.rollback()
        logger.error(f"Erro ao popular tabelas do Data Warehouse: {e}")
        return False
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="Cria o schema dw e popula as tabelas do Data Warehouse a partir das tabelas normalizadas."
    )
    parser.add_argument(
        "--ddl-path",
        default=os.path.join("DW", "DDL.sql"),
        help="Caminho do DDL .sql das tabelas do Data Warehouse (default: DW/DDL.sql)",
    )
    parser.add_argument(
        "--dml-path",
        default=os.path.join("DW", "DML.sql"),
        help="Caminho do DML .sql para popular as tabelas (default: DW/DML.sql)",
    )
    parser.add_argument(
        "--create-only",
        action="store_true",
        help="Somente cria as tabelas, sem popular.",
    )
    args = parser.parse_args()

    created = create_dw_tables(args.ddl_path)
    if not created or args.create_only:
        return

    populate_dw_tables(args.dml_path)


if __name__ == "__main__":
    main()

