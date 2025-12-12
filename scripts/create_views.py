"""
Cria as views do banco de dados a partir dos arquivos SQL.
Use as variáveis de ambiente DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME.
"""
import argparse
import os
from pathlib import Path

from loguru import logger

import utils.database_config as db_config


def create_views(views_path: str) -> bool:
    """
    Cria as views a partir de um arquivo SQL.
    """
    conn = db_config.get_connection()
    if not conn:
        logger.error("Erro ao conectar ao banco de dados")
        return False

    try:
        views_file_path = Path(views_path)
        if not views_file_path.exists():
            raise FileNotFoundError(f"Arquivo de views não encontrado em {views_file_path}")

        with open(views_file_path, "r", encoding="utf-8") as views_file:
            views_sql = views_file.read()

        with conn.cursor() as cursor:
            db_config.execute_multiple_statements(views_sql, cursor)
        conn.commit()
        logger.info("Views criadas com sucesso")
        return True
    except Exception as e:
        conn.rollback()
        logger.error(f"Erro ao criar views: {e}")
        return False
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="Cria as views do banco de dados a partir do arquivo SQL."
    )
    parser.add_argument(
        "--views-path",
        default=os.path.join("objetos", "Views.sql"),
        help="Caminho do arquivo SQL com as views (default: objetos/Views.sql)",
    )
    args = parser.parse_args()

    create_views(args.views_path)


if __name__ == "__main__":
    main()

