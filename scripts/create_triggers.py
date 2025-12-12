"""
Cria os triggers do banco de dados a partir dos arquivos SQL.
Use as variáveis de ambiente DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME.
"""
import argparse
import os
from pathlib import Path

from loguru import logger

import utils.database_config as db_config


def create_triggers(triggers_path: str) -> bool:
    """
    Cria os triggers a partir de um arquivo SQL.
    """
    conn = db_config.get_connection()
    if not conn:
        logger.error("Erro ao conectar ao banco de dados")
        return False

    try:
        triggers_file_path = Path(triggers_path)
        if not triggers_file_path.exists():
            raise FileNotFoundError(f"Arquivo de triggers não encontrado em {triggers_file_path}")

        with open(triggers_file_path, "r", encoding="utf-8") as triggers_file:
            triggers_sql = triggers_file.read()

        with conn.cursor() as cursor:
            db_config.execute_multiple_statements(triggers_sql, cursor)
        conn.commit()
        logger.info("Triggers criados com sucesso")
        return True
    except Exception as e:
        conn.rollback()
        logger.error(f"Erro ao criar triggers: {e}")
        return False
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="Cria os triggers do banco de dados a partir do arquivo SQL."
    )
    parser.add_argument(
        "--triggers-path",
        default=os.path.join("objetos", "Triggers.sql"),
        help="Caminho do arquivo SQL com os triggers (default: objetos/Triggers.sql)",
    )
    args = parser.parse_args()

    create_triggers(args.triggers_path)


if __name__ == "__main__":
    main()

